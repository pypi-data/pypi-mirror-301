import torch
import torch.nn as nn
import torch.utils.data
from torch.utils.data import RandomSampler, SequentialSampler, DataLoader
import torch.optim as optim
from tqdm import tqdm
import yaml
import torch.nn.functional as F

from utils.store import save_state
from utils.metric import Metric



param_path = 'config/model_param/GCBNet.yaml'


def tansig(x):
    return 2 / (1 + torch.exp(-2*x)) - 1

class GCBNet_BLS(nn.Module):
    def __init__(self, num_electrodes=62, in_channels=5, num_classes=3, k=4, relu_is=1, layers=None, dropout_rate=0.5, lamb=0.001):
        # num_electrodes(int): The number of electrodes.
        # in_channels(int): The feature dimension of each electrode.
        # num_classes(int): The number of classes to predict.
        # k_(int): The number of graph convolutional layers.
        # relu_is(int): The function we use
        # out_channel(int): The feature dimension of  the graph after GCN.
        super(GCBNet_BLS, self).__init__()

        self.dropout_rate = dropout_rate
        self.lamb = lamb
        self.layers = layers
        self.k = k
        self.in_channels = in_channels
        self.num_electrodes = num_electrodes
        self.num_classes = num_classes
        self.relu_is = relu_is
        self.get_param()

        self.graphConvs = nn.ModuleList()
        self.fea_layer = nn.ModuleList()
        self.enh_layer = nn.ModuleList()

        for i in range(10):
            self.fea_layer.append(nn.Linear(self.num_electrodes * 88, 10))

        for i in range(10):
            self.enh_layer.append(nn.Linear(10, 10))

        self.graphConvs.append(GraphConv(self.k, self.in_channels, self.layers[0]))
        for i in range(len(self.layers) - 1):
            self.graphConvs.append(GraphConv(self.k, self.layers[i], self.layers[i + 1]))

        self.conv1 = nn.Conv1d(in_channels=self.layers[0], out_channels=32, stride=1, kernel_size=7, padding='same')
        self.maxpool = nn.MaxPool1d(kernel_size=2, stride=2, padding=0)
        self.conv2 = nn.Conv1d(in_channels=32, out_channels=16, stride=1, kernel_size=7, padding='same')

        self.fc = nn.Linear(1100, self.num_classes, bias=True)
        self.original_fc = nn.Linear(self.num_electrodes*88, self.num_classes)
        self.adj = nn.Parameter(torch.Tensor(self.num_electrodes, self.num_electrodes))
        self.adj_bias = nn.Parameter(torch.Tensor(1))
        self.relu = nn.ReLU(inplace=True)
        self.b_relus = nn.ModuleList()
        if self.relu_is == 1:
            for i in range(len(self.layers)):
                self.b_relus.append(B1ReLU(self.layers[i]))
        elif self.relu_is == 2:
            for i in range(len(self.layers)):
                self.b_relus.append(B2ReLU(self.adj.shape[0], self.layers[i]))
        self.dropout = nn.Dropout(p=self.dropout_rate)
        self.init_weight()

    def get_param(self):
        try:
            fd = open(param_path, 'r', encoding='utf-8')
            model_param = yaml.load(fd, Loader=yaml.FullLoader)
            fd.close()
            self.k = model_param['params']['k']
            self.relu_is = model_param['params']['relu_is']
            self.layers = model_param['params']['layers']
            self.dropout_rate = model_param['params']['dropout']
            print("\nUsing setting from {}\n".format(param_path))
        except IOError:
            print("\n{} may not exist or not available".format(param_path))

        print("GCBNet Model, Parameters:\n")
        print("{:45}{:20}".format("k (The order of Chebyshev polynomials):", self.k))
        print("{:45}{:20}".format("relu_is (The type of B_Relu func):", self.relu_is))
        print("{:45}{:20}".format("layers (The channels of each layers):", str(self.layers)))
        print("{:45}{:20}\n".format("dropout rate:", self.dropout_rate))
        if self.k != 2 or self.relu_is != 1 or self.layers != [128] or self.dropout_rate != 0.5:
            print("Not Using Default Setting, the performance may be not the best")
        print("Starting......")

    def init_weight(self):
        nn.init.xavier_uniform_(self.adj)
        nn.init.trunc_normal_(self.adj_bias, mean=0, std=0.1)
        for i in range(10):
            nn.init.xavier_uniform_(self.fea_layer[i].weight)
            nn.init.zeros_(self.fea_layer[i].bias)
            nn.init.xavier_uniform_(self.enh_layer[i].weight)
            nn.init.zeros_(self.enh_layer[i].bias)
        nn.init.xavier_uniform_(self.fc.weight)
        nn.init.kaiming_uniform_(self.conv1.weight, mode='fan_in', nonlinearity='relu')
        nn.init.kaiming_uniform_(self.conv2.weight, mode='fan_in', nonlinearity='relu')
        nn.init.zeros_(self.conv1.bias)
        nn.init.zeros_(self.conv2.bias)
        nn.init.zeros_(self.fc.bias)


    def forward(self, x):
        adj = self.relu(self.adj + self.adj_bias)
        lap = laplacian(adj)
        for i in range(len(self.layers)):
            x = self.graphConvs[i](x, lap)
            x = self.dropout(x)
            x = self.b_relus[i](x)
        bs = x.shape[0]
        x = x.permute(0, 2, 1)
        x1 = self.relu((self.conv1(x)))
        x2 = self.maxpool(x1)
        x3 = self.relu((self.conv2(x2)))
        x, x2, x3 = x.reshape(bs, -1), x2.reshape(bs, -1), x3.reshape(bs, -1)
        x = torch.cat((x, x2, x3), dim=1)
        feature_nodes = []
        for i in range(10):
            feature_nodes.append(self.fea_layer[i](x).unsqueeze(1))
        feature_nodes = torch.cat(feature_nodes, dim=1)
        feature_nodes = feature_nodes.to(x.device)
        # print(feature_nodes.shape)
        enhancement_nodes = []
        for i in range(10):
            enhancement_nodes.append(torch.tanh(self.enh_layer[i](feature_nodes)))
        enhancement_nodes = torch.cat(enhancement_nodes, dim=1)
        enhancement_nodes = enhancement_nodes.to(x.device)
        summary = torch.cat((feature_nodes, enhancement_nodes), dim=1).reshape(bs,-1)
        summary = self.dropout(summary)
        output = self.fc(summary)
        # x = self.dropout(x)
        # output = self.original_fc(x)
        return output, self.fc.weight

    def train_one_round(self, args, r_idx, rr_idx, train_data, train_label, val_data, val_label, test_data, test_label):
        # choose device to train
        device = torch.device(args.device)

        # train_data, test_data = normalize(train_data, test_data)
        # print(train_data.shape, test_data.shape)

        # get train and test dataset
        dataset_train = torch.utils.data.TensorDataset(torch.Tensor(train_data), torch.Tensor(train_label))

        # dataset_val = torch.utils.data.TensorDataset(torch.Tensor(val_data), torch.Tensor(val_label))

        dataset_test = torch.utils.data.TensorDataset(torch.Tensor(test_data), torch.Tensor(test_label))

        # data sampler for train and test data
        sampler_train = RandomSampler(dataset_train)

        # sampler_val = RandomSampler(dataset_val)

        sampler_test = SequentialSampler(dataset_test)

        # load dataset
        data_loader_train = DataLoader(
            dataset_train, sampler=sampler_train, batch_size=args.batch_size, num_workers=args.num_workers
        )

        # data_loader_val = DataLoader(
        #     dataset_val, sampler=sampler_val, batch_size=args.batch_size, num_workers=args.num_workers
        # )

        data_loader_test = DataLoader(
            dataset_test, sampler=sampler_test, batch_size=args.batch_size, num_workers=args.num_workers
        )

        # load the model onto the corresponding device
        model = self.to(device)
        # the optimizer for train

        optimizer = optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-3, eps=1e-4)
        # optimizer = optim.SGD(model.parameters(), lr=args.lr, weight_decay=1e-4, momentum=0.9)
        # scheduler = CosineAnnealingLR(optimizer, T_max=args.epochs - args.resume_epoch)

        # the loss function for train
        criterion = nn.CrossEntropyLoss()
        l2_norm = SparseL2Regularization(0.001)
        # If retrain from a breakpoint, or just evaluate, the model parameters are loaded
        if (args.resume or args.eval) and args.checkpoint is not None:
            model.load_state_dict(torch.load(args.checkpoint)['model'])

        # If only evaluate, only perform the following operations for evaluation
        if args.eval:
            print(f"Starting Evaluation, the len of test data is {len(data_loader_test)}")
            self.evaluate(data_loader_test, criterion, args, model, device)
            exit(0)
        print(f"Start training for {args.epochs} epochs")
        best_metric = {s: 0. for s in args.metrics}
        for epoch in range(args.epochs - args.resume_epoch):
            model.train()
            optimizer.zero_grad()

            # create Metric object
            metric = Metric(args.metrics)
            # create train pbar
            train_bar = tqdm(enumerate(data_loader_train), total=len(data_loader_train), desc=
            f"Train Epoch {epoch + args.resume_epoch + 1}/{args.epochs}: lr:{optimizer.param_groups[0]['lr']}")
            for idx, (samples, targets) in train_bar:
                # load the samples into the device
                samples = samples.to(device)
                targets = targets.to(device)

                optimizer.zero_grad()
                # perform emotion recognition
                outputs, W_b = model(samples)
                # calculate the loss value
                # loss = criterion(outputs, targets.to(torch.int64)) + l2_norm(self.adj) + 0.001 * torch.norm(W_b)
                loss = criterion(outputs, targets.to(torch.int64)) + 0.001 * l2_norm(W_b)
                # one hot code
                # loss = criterion(outputs, targets) + l2_norm(self.adj)
                metric.update(torch.argmax(outputs, dim=1), targets, loss.item())
                train_bar.set_postfix_str(f"loss: {loss.item():.2f}")

                loss.backward()
                optimizer.step()
            # scheduler.step()
            print("\033[32m train state: " + metric.value())
            # evaluate the model
            metric_value = self.evaluate(data_loader_test, criterion, args, model, device)
            for m in args.metrics:
                # if metric is the best, save the model state
                if metric_value[m] > best_metric[m]:
                    best_metric[m] = metric_value[m]
                    save_state(args, model, optimizer, epoch + 1 + args.resume_epoch, r_idx, rr_idx, metric=m)
        # save the state after last train
        # save_state(args, model, optimizer, args.epochs, r_idx, rr_idx)
        # model.load_state_dict(torch.load(
        #     f"{args.output_dir}/{args.model}/{args.setting}/{r_idx}/{rr_idx}/checkpoint-best{args.metric_choose}")[
        #                           'model'])
        # metric_value = self.evaluate(data_loader_test, criterion, args, model, device)
        # print best metrics
        for m in args.metrics:
            print(f"best_val_{m}: {best_metric[m]:.2f}")
            # print(f"best_test_{m}: {metric_value[m]:.2f}")
        # return metric_value
        return best_metric
    @torch.no_grad()
    def evaluate(self, data_loader, criterion, args, model, device):
        model.eval()
        # create Metric object
        metric = Metric(args.metrics)
        for idx, (samples, targets) in tqdm(enumerate(data_loader), total=len(data_loader),
                                            desc=f"Evaluating : "):
            # load the samples into the device
            samples = samples.to(device)
            targets = targets.to(device)

            # perform emotion recognition
            outputs, _ = model(samples)

            # calculate the loss value
            loss = criterion(outputs, targets.to(torch.int64))
            # one hot code
            # loss = criterion(outputs, targets)
            metric.update(torch.argmax(outputs, dim=1), targets, loss.item())

        print("\033[34m eval state: " + metric.value())
        return metric.values


def laplacian(w):
    """
    calculate the laplacian of the adjacency matrix
    :param w: the adjacency matrix
    :return: l: the normalized Laplacian matrix
    """
    # d is the sum of each row of a matrix.
    d = torch.sum(w, dim=1)
    # reciprocal square root of a vector
    d_re = 1 / torch.sqrt(d + 1e-5)
    # create a matrix with the d_re vector as its diagonal elements
    d_matrix = torch.diag_embed(d_re)
    # calculate the laplacian matrix
    lap = torch.eye(d_matrix.shape[0], device=w.device) - torch.matmul(torch.matmul(d_matrix, w), d_matrix)
    return lap


class GraphConv(nn.Module):
    """
    Graph convolution based on Chebyshev polynomials
    """

    def __init__(self, k, in_channels, out_channels):
        super(GraphConv, self).__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.k = k
        self.weight = nn.Parameter(torch.Tensor(k * in_channels, out_channels))
        nn.init.xavier_uniform_(self.weight)
        # self.truncated_normal_(self.weight)

    def chebyshev_polynomial(self, x, lap):
        """
        calculate the chebyshev polynomial
        :param x : input x
        :param lap: the input laplacian matrix
        :return: the chebyshev polynomial components
        """
        t = torch.ones(x.shape[0], x.shape[1], x.shape[2]).to(x.device)
        if self.k == 1:
            return t.unsqueeze(1)
        if self.k == 2:
            return torch.cat((t.unsqueeze(1), torch.matmul(lap, x).unsqueeze(1)), dim=1)
        elif self.k > 2:
            # T_0 of chebyshev polynomials, just x (identity matrix multiply x), shape: (batch, ele_channel, in_channel)
            tk_minus_one = x
            # T_1 of chebyshev polynomials, shape: (batch, ele_channel, in_channel)
            tk = torch.matmul(lap, x)
            # add the T_0, T_1, T_2 items to the Chebyshev components, t shape: (batch, 3, ele_channel, in_channel)
            t = torch.cat((t.unsqueeze(1), tk_minus_one.unsqueeze(1), tk.unsqueeze(1)), dim=1)
            for i in range(3, self.k):
                # T_(k-1) and T_(k-2)
                tk_minus_two, tk_minus_one = tk_minus_one, tk
                # calculate the T_(k), shape: (batch, ele_channel, in_channel)
                tk = 2 * torch.matmul(lap, tk_minus_one) - tk_minus_two
                # add the T_k items to the Chebyshev components, shape: (batch, i+1, ele_channel, in_channel)
                t = torch.cat((t, tk.unsqueeze(1)), dim=1)
            return t

    def forward(self, x, lap):
        """
        :param x: (batch_size, ele_channel, in_channel)
        :param lap: the laplacian matrix
        :return: the result of Graph conv
        """
        # obtain the chebyshev polynomial, t shape: (batch, k, ele_channel, in_channel)
        cp = self.chebyshev_polynomial(x, lap)
        # transpose cp to: (batch, ele_channel, in_channel, k)
        cp = cp.permute(0, 2, 3, 1)
        # reshape cp to: (batch, ele_channel, in_channel * k)
        cp = cp.flatten(start_dim=2)
        # perform filter operation of order K
        out = torch.matmul(cp, self.weight)
        return out

class NewSparseL2Regularization(nn.Module):
    def __init__(self, l2_lambda):
        super(NewSparseL2Regularization, self).__init__()
        self.l2_lambda = l2_lambda
    def forward(self, x):
        l2_reg = torch.tensor(0.).to(next(x.parameters()).device)
        for param in x.parameters():
            l2_reg += torch.norm(param)
        return l2_reg * self.l2_lambda

class SparseL2Regularization(nn.Module):
    def __init__(self, l2_lambda):
        super(SparseL2Regularization, self).__init__()
        self.l2_lambda = l2_lambda

    def forward(self, x):
        l2_norm = torch.norm(x, p=2)
        return self.l2_lambda * l2_norm


class B1ReLU(nn.Module):
    def __init__(self, bias_shape):
        super(B1ReLU, self).__init__()
        self.bias = nn.Parameter(torch.Tensor(1, 1, bias_shape))
        self.relu = nn.ReLU()
        nn.init.zeros_(self.bias)

    def forward(self, x):
        return self.relu(self.bias + x)


class B2ReLU(nn.Module):
    def __init__(self, bias_shape1, bias_shape2):
        super(B2ReLU, self).__init__()
        self.bias = nn.Parameter(torch.Tensor(1, bias_shape1, bias_shape2))
        self.relu = nn.ReLU()
        nn.init.zeros_(self.bias)

    def forward(self, x):
        return self.relu(self.bias + x)

