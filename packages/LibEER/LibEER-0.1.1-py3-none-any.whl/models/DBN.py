
import torch
import torch.nn as nn
import torch.utils.data
from torch.utils.data import RandomSampler, SequentialSampler, DataLoader
import torch.optim as optim
from tqdm import tqdm
from data_utils.preprocess import normalize
from utils.store import save_state
from utils.metric import Metric
param_path = 'config/model_param/DBN.yaml'
import yaml
#RBM类的定义
class RBM(nn.Module):
    def __init__(self, visible_units, hidden_units):
        super(RBM, self).__init__()
        self.W = nn.Parameter(torch.randn(visible_units, hidden_units))
        self.v_bias = nn.Parameter(torch.randn(visible_units))
        self.h_bias = nn.Parameter(torch.randn(hidden_units))
        self.w_momentum = torch.zeros(visible_units, hidden_units)

    def sample_h(self, v):
        prob_hidden=torch.matmul(v,self.W)
        prob_hidden=prob_hidden+self.h_bias
        prob_hidden=torch.sigmoid(prob_hidden)
        return prob_hidden, torch.bernoulli(prob_hidden)

    def sample_v(self, h):
        prob_visible = torch.sigmoid(torch.matmul(h, self.W.t()) + self.v_bias)
        prob_visible_gauss = prob_visible + torch.randn_like(prob_visible)
        return prob_visible, prob_visible_gauss

    def forward(self, v):
        p_h_given_v = torch.sigmoid(torch.matmul(v, self.W) + self.h_bias)
        h_sample = torch.bernoulli(p_h_given_v)
        p_v_given_h = torch.sigmoid(torch.matmul(h_sample, self.W.t()) + self.v_bias)
        return p_v_given_h, p_h_given_v

    def constrastive_divergence(self, v,batch_size,device, learning_rate=0.005, momentum=0.1):
        v = v.to(device)
        self.W = self.W.to(device)
        self.v_bias = self.v_bias.to(device)
        self.h_bias = self.h_bias.to(device)
        self.w_momentum = self.w_momentum.to(device)
        positive_hidden_prob, positive_hidden = self.sample_h(v)
        positive_association = torch.matmul(v.t(), positive_hidden_prob)
        hidden = positive_hidden
        visible_prob, visible = self.sample_v(hidden)
        hidden_prob, hidden = self.sample_h(visible_prob)
        negative_visible_prob = visible
        negative_hidden_prob = hidden_prob
        negative_association = torch.matmul(negative_visible_prob.t(), negative_hidden_prob)

        self.w_momentum *= momentum
        self.w_momentum += (positive_association - negative_association)

        self.W.data.add_(self.w_momentum * learning_rate / batch_size)
        self.v_bias.data.add_(learning_rate * torch.sum(v - visible, dim=0) / batch_size)
        self.h_bias.data.add_(learning_rate * torch.sum(positive_hidden_prob - negative_hidden_prob, dim=0) / batch_size)

    def sigmoid(self, x):
        return 1 / (1 + torch.exp(-x))


#DBN
class DBN(nn.Module):
    def __init__(self,num_electrodes=62, in_channels=5, num_classes=3,hidden_size1=300,hidden_size2=400):
        super(DBN,self).__init__()
        self.num_electrodes=num_electrodes
        self.in_channels=in_channels
        self.num_classes=num_classes
        #not used
        #self.get_param()
        self.rbm1=RBM(self.num_electrodes * self.in_channels,hidden_size1)
        self.rbm2=RBM(hidden_size1,hidden_size2)
        self.fc=nn.Linear(hidden_size2,num_classes)

    def get_param(self):
        try:
            fd = open(param_path, 'r', encoding='utf-8')
            model_param = yaml.load(fd, Loader=yaml.FullLoader)
            fd.close()
            self.hidden_size1 = model_param['params']['h1']
            self.hidden_size2 = model_param['params']['h2']
            print("\nUsing setting from {}\n".format(param_path))
        except IOError:
            print("\n{} may not exist or not available".format(param_path))

        print("DBN Model, Parameters:\n")
        print("{:45}{:20}".format("h1:", self.hidden_size1))
        print("{:45}{:20}".format("h2:", self.hidden_size2))
        print("Starting......")

    def forward(self,v):
        #v=v.view(v.shape[0],-1).type(torch.FloatTensor)
        h1_prob,h1=self.rbm1(v)
        h2_prob,h2=self.rbm2(h1)
        output=self.fc(h2)
        return output
    #reconstruction
    def reconstruct(self,v,device):
        h0=v
        # forward pass through rbms to get hidden representation前向传播
        for rbm_layer in[self.rbm1,self.rbm2]:
            h0.to(device)
            p_h,h0=rbm_layer.sample_h(h0)
        v0=h0
        # backward pass through rbms to reconstruct visible representation后相传播
        for rbm_layer in [self.rbm2,self.rbm1]:
            v0.to(device)
            p_v,v0=rbm_layer.sample_v(h=v0)
        return v0
    def train_one_round(self,args,r_idx, rr_idx,train_data,train_label,val_data,val_label,test_data,test_label):
        # choose device to train
        device = torch.device(args.device)
        train_data, val_data, test_data = normalize(train_data, val_data, test_data, dim='sample', method="minmax")
        # get train and test dataset
        dataset_train = torch.utils.data.TensorDataset(torch.Tensor(train_data), torch.Tensor(train_label))

        dataset_val = torch.utils.data.TensorDataset(torch.Tensor(val_data), torch.Tensor(val_label))

        dataset_test = torch.utils.data.TensorDataset(torch.Tensor(test_data), torch.Tensor(test_label))

        # data sampler for train and test data
        sampler_train = RandomSampler(dataset_train)

        sampler_val = RandomSampler(dataset_val)

        sampler_test = SequentialSampler(dataset_test)

        # load dataset
        data_loader_train = DataLoader(
            dataset_train, sampler=sampler_train, batch_size=args.batch_size, num_workers=args.num_workers
        )

        data_loader_val = DataLoader(
            dataset_val, sampler=sampler_val, batch_size=args.batch_size, num_workers=args.num_workers
        )

        data_loader_test = DataLoader(
            dataset_test, sampler=sampler_test, batch_size=args.batch_size, num_workers=args.num_workers
        )
        # load the model onto the corresponding device
        model = self.to(device)
       #greedy layer-wise pretrain
        model.train()
        for epoch in range(10):
            # create train pbar
            train_bar = tqdm(enumerate(data_loader_train), total=len(data_loader_train), desc=
            f"Train Epoch {epoch+1}: ")
            for idx, (samples,targets) in train_bar:
                # load the samples into the device
                samples = samples.to(device)
                samples=samples.reshape(samples.shape[0],samples.shape[1]*samples.shape[2])
                self.rbm1.constrastive_divergence(samples,batch_size=args.batch_size,device=device)    #对rbm1进行预训练
                _,onelayerout=self.rbm1.sample_h(samples)
                self.rbm2.constrastive_divergence(onelayerout, batch_size=args.batch_size, device=device)#对rbm2进行预训练

        print(f"Finished pretraining")

        #unsupervised fine tune
        criterion = torch.nn.MSELoss()
        optimizer = optim.SGD(self.parameters(), lr=0.5)
        #optimizer = optim.AdamW(model.parameters(), lr=0.5, weight_decay=1e-3, eps=1e-4)
        for epoch in range(5):
            model.train()
            # create train pbar
            train_bar = tqdm(enumerate(data_loader_train), total=len(data_loader_train), desc=
            f"Train Epoch {epoch }: lr:{optimizer.param_groups[0]['lr']}")
            for idx, (samples, targets) in train_bar:
                # load the samples into the device
                samples = samples.to(device)
                samples = samples.reshape(samples.shape[0], samples.shape[1] * samples.shape[2])   #将输入变成310维
                optimizer.zero_grad()
                # perform emotion recognition
                recon = self.reconstruct(samples,device=device)
                # calculate the loss value
                loss = criterion(samples,recon)
                train_bar.set_postfix_str(f"loss: {loss.item():.2f}")
                loss.backward()
                optimizer.step()

        #supervised fine tune
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.SGD(self.parameters(), lr=0.6)
        #optimizer = optim.AdamW(model.parameters(), lr=0.6, weight_decay=0.1, eps=1e-4)
        # If retrain from a breakpoint, or just evaluate, the model parameters are loaded
        if (args.resume or args.eval) and args.checkpoint is not None:
            model.load_state_dict(torch.load(args.checkpoint)['model'])

        # If only evaluate, only perform the following operations for evaluation
        if args.eval:
            print(f"Starting Evaluation, the len of test data is {len(data_loader_test)}")
            self.evaluate(data_loader_test, criterion, args, model, device)
            exit(0)
        print(f"Start training for 40 epochs")
        best_metric = {s: 0. for s in args.metrics}
        for epoch in range(30):
            model.train()
            # create Metric object
            metric = Metric(args.metrics)
            # create train pbar
            train_bar = tqdm(enumerate(data_loader_train), total=len(data_loader_train), desc=
            f"Train Epoch {epoch }: lr:{optimizer.param_groups[0]['lr']}")
            for idx, (samples, targets) in train_bar:
                # load the samples into the device
                samples = samples.to(device)
                samples = samples.reshape(samples.shape[0], samples.shape[1] * samples.shape[2])
                targets = targets.to(device)
                optimizer.zero_grad()
                # perform emotion recognition
                outputs = model(samples)
                # calculate the loss value
                loss = criterion(outputs, targets.to(torch.int64))
                metric.update(torch.argmax(outputs, dim=1), targets, loss.item())
                train_bar.set_postfix_str(f"loss: {loss.item():.2f}")
                loss.backward()
                optimizer.step()
            # scheduler.step()
            print("\033[32m train state: " + metric.value())
            # evaluate the model
            metric_value = self.evaluate(data_loader_val, criterion, args, model, device)
            for m in args.metrics:
                # if metric is the best, save the model state
                if metric_value[m] > best_metric[m]:
                    best_metric[m] = metric_value[m]
                    save_state(args, model, optimizer, epoch + 1 + args.resume_epoch, r_idx, rr_idx, metric=m)
        # save the state after last train
        # save_state(args, model, optimizer, args.epochs, r_idx, rr_idx)
        model.load_state_dict(torch.load(
            f"{args.output_dir}/{args.model}/{args.setting}/{r_idx}/{rr_idx}/checkpoint-best{args.metric_choose}")[
                                  'model'])
        metric_value = self.evaluate(data_loader_test, criterion, args, model, device)
        # print best metrics
        for m in args.metrics:
            print(f"best_val_{m}: {best_metric[m]:.2f}")
            print(f"best_test_{m}: {metric_value[m]:.2f}")
        return metric_value

    def evaluate(self, data_loader, criterion, args, model, device):
        model.eval()
        # create Metric object
        metric = Metric(args.metrics)
        for idx, (samples, targets) in tqdm(enumerate(data_loader), total=len(data_loader),
                                            desc=f"Evaluating : "):
            # load the samples into the device
            samples = samples.to(device)
            samples = samples.reshape(samples.shape[0], samples.shape[1] * samples.shape[2])
            targets = targets.to(device)
            # perform emotion recognition
            outputs = model(samples)

            # calculate the loss value
            loss = criterion(outputs, targets.to(torch.int64))
            metric.update(torch.argmax(outputs, dim=1), targets, loss.item())

        print("\033[34m eval state: " + metric.value())
        return metric.values




