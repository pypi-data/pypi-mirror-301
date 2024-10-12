import torch
import torch.nn as nn
import torch.utils.data
from torch.utils.data import RandomSampler, SequentialSampler, DataLoader
import torch.optim as optim
import numpy as np
from tqdm import tqdm
import yaml

from utils.store import save_state
from utils.metric import Metric
from data_utils.preprocess import ele_normalize
import torch.nn.functional as F
import math

param_path = 'config/model_param/MSMDA.yaml'

dim_feature = 310

class MSMDA(nn.Module):
    def __init__(self, num_electrodes=62, in_channels=5, num_classes=3, number_of_source = 14, pretrained=False):
        
        super(MSMDA, self).__init__()
        global dim_feature
        dim_feature = num_electrodes * in_channels
        self.sharedNet = pretrained_CFE(pretrained=pretrained)
        for i in range(number_of_source):
            '''
            这行代码的作用是根据类名动态创建一个类的实例，并将其赋值给相应的变量。
            通过执行 =DSFE()，可以创建一个新的 DSFE 类的实例，并将其赋值给 self.DSFE{i} 变量。
            '''
            exec('self.DSFE' + str(i) + '=DSFE()')
            exec('self.cls_fc_DSC' + str(i) +
                 '=nn.Linear(32,' + str(num_classes) + ')')

    def forward(self, data_src, number_of_source, data_tgt=0, label_src=0, mark=0):
        mmd_loss = 0
        disc_loss = 0
        data_tgt_DSFE = []
        if self.training == True:
            # common feature extractor
            data_src_CFE = self.sharedNet(data_src)
            data_tgt_CFE = self.sharedNet(data_tgt)
            # Each domian specific feature extractor
            # to extract the domain specific feature of target data
            for i in range(number_of_source):
                DSFE_name = 'self.DSFE' + str(i)
                data_tgt_DSFE_i = eval(DSFE_name)(data_tgt_CFE)
                data_tgt_DSFE.append(data_tgt_DSFE_i)
            # Use the specific feature extractor
            # to extract the source data, and calculate the mmd loss
            DSFE_name = 'self.DSFE' + str(mark)
            data_src_DSFE = eval(DSFE_name)(data_src_CFE)
            # mmd_loss += utils.mmd(data_src_DSFE, data_tgt_DSFE[mark])
            mmd_loss += mmd_linear(data_src_DSFE, data_tgt_DSFE[mark])
            # discrepency loss
            for i in range(len(data_tgt_DSFE)):
                if i != mark:
                    disc_loss += torch.mean(torch.abs(
                        F.softmax(data_tgt_DSFE[mark], dim=1) -
                        F.softmax(data_tgt_DSFE[i], dim=1)
                    ))
            # domain specific classifier and cls_loss
            DSC_name = 'self.cls_fc_DSC' + str(mark)
            pred_src = eval(DSC_name)(data_src_DSFE)
            cls_loss = F.nll_loss(F.log_softmax(
                pred_src, dim=1), label_src.long().squeeze())

            return cls_loss, mmd_loss, disc_loss

        else:
            data_CFE = self.sharedNet(data_src)
            pred = []
            for i in range(number_of_source):
                DSFE_name = 'self.DSFE' + str(i)
                DSC_name = 'self.cls_fc_DSC' + str(i)
                feature_DSFE_i = eval(DSFE_name)(data_CFE)
                pred.append(eval(DSC_name)(feature_DSFE_i))
            return pred

    def train_one_round(self, args, r_idx, rr_idx, train_data, train_label, test_data, test_label):
        # choose device to train
        device = torch.device(args.device)

        # get train and test dataset and load dataset
        samples_source = len(train_data[0])
        source_loaders = []
        for j in range(len(train_data)):
            train_label[j] = np.array(train_label[j])
            train_data[j] = ele_normalize(np.array(train_data[j]))
            train_data[j] = train_data[j].reshape(samples_source,-1)
            source_loaders.append(torch.utils.data.DataLoader(dataset=torch.utils.data.TensorDataset(torch.Tensor(train_data[j]), torch.Tensor(train_label[j])),
                                                          batch_size=args.batch_size,
                                                          shuffle=True,
                                                          drop_last=True,
                                                          num_workers=args.num_workers))
        test_label[0] = np.array(test_label[0])
        test_data[0] = ele_normalize(np.array(test_data[0]))
        test_data[0] = test_data[0].reshape(samples_source,-1)
        target_loader = torch.utils.data.DataLoader(dataset=torch.utils.data.TensorDataset(torch.Tensor(test_data[0]), torch.Tensor(test_label[0])),
                                                batch_size=args.batch_size,
                                                shuffle=True,
                                                drop_last=True,
                                                num_workers=args.num_workers)
        
        # load the model onto the corresponding device
        model = self.to(device)

        # the loss function for train
        criterion = nn.CrossEntropyLoss()

        # If retrain from a breakpoint, or just evaluate, the model parameters are loaded
        if (args.resume or args.eval) and args.checkpoint is not None:
            model.load_state_dict(torch.load(args.checkpoint)['model'])

        # If only evaluate, only perform the following operations for evaluation
        if args.eval:
            print(f"Starting Evaluation, the len of test data is {len(target_loader)}")
            self.evaluate(target_loader, criterion, args, model, device, len(source_loaders))
            exit(0)
        print(f"Start training for {args.epochs} epochs")

        best_metric = {s: 0. for s in args.metrics}
        iteration = math.ceil(samples_source/args.batch_size)
        iterations = (args.epochs - args.resume_epoch)*iteration
        log_interval = 10
        target_iter = iter(target_loader)

        source_iters = []
        for i in range(len(source_loaders)):
            source_iters.append(iter(source_loaders[i]))
        for epoch in range(args.epochs - args.resume_epoch):
            _tqdm = tqdm(range(iteration), desc= f"Train Epoch {epoch + args.resume_epoch + 1}/{args.epochs}",leave=False)
            #, colour='red' position=2,, desc= f"Train Epoch {epoch + args.resume_epoch + 1}/{args.epochs}",
            for idx in _tqdm: 
                model.train()
                LEARNING_RATE = args.lr
                # the optimizer for train
                optimizer = torch.optim.Adam(
                        model.parameters(), lr=LEARNING_RATE)

                #_tqdm.set_postfix = f"Train Epoch {epoch + args.resume_epoch + 1}/{args.epochs}: lr:{optimizer.param_groups[0]['lr']}"

                #domain_tqdm = tqdm(range(len(source_iters)), desc="Source_Domain",  colour='green', position=0, leave=True)
                #
                for j in range(len(source_iters)):
                    try:
                        source_data, source_label = next(source_iters[j])
                    except Exception as err:
                        source_iters[j] = iter(source_loaders[j])
                        source_data, source_label = next(source_iters[j])
                    try:
                        target_data, _ = next(target_iter)
                    except Exception as err:
                        target_iter = iter(target_loader)
                        target_data, _ = next(target_iter)
                    source_data, source_label = source_data.to(device), source_label.to(device)
                    target_data = target_data.to(device)

                    optimizer.zero_grad()
                    cls_loss, mmd_loss, l1_loss = model(source_data, number_of_source=len(source_loaders), 
                                                             data_tgt=target_data, label_src=source_label, mark=j)
                    gamma = 2 / (1 + math.exp(-10 * (epoch*iteration+idx) / (iterations))) - 1
                    beta = gamma/100
                    loss = cls_loss + gamma * mmd_loss + beta * l1_loss
                    loss.backward()
                    optimizer.step()
                    _tqdm.set_postfix_str(f"loss: {loss.item():.2f}")
                metric_value = self.evaluate(target_loader, criterion, args, model, device, len(source_loaders))
                for m in args.metrics:
                # if metric is the best, save the model state
                    if metric_value[m] > best_metric[m]:
                        best_metric[m] = metric_value[m]
                        save_state(args, model, optimizer, epoch + 1 + args.resume_epoch, r_idx, rr_idx, metric=m)
        # save the state after last train
        save_state(args, model, optimizer, args.epochs, r_idx, rr_idx)
        # print best metrics
        for m in args.metrics:
            print(f"best_{m}: {best_metric[m]:.2f}")
        return best_metric
        


    @torch.no_grad()
    def evaluate(self, target_loader, criterion, args, model, device, source_num):
        model.eval()
        # create Metric object
        metric = Metric(args.metrics)
        for idx, (data, target) in tqdm(enumerate(target_loader), total=len(target_loader),
                                            desc=f"Evaluating : " , leave=False):
                #,, position=1
            data = data.to(device)
            target = target.to(device)
            preds = model(data, source_num)

            for i in range(len(preds)):
                preds[i] = F.softmax(preds[i], dim=1)

            pred = sum(preds)/len(preds) #经过len(preds)个源域后预测的平均值
            test_loss = F.nll_loss(F.log_softmax(pred,
                                        dim=1), target.long().squeeze())
                
            metric.update(torch.argmax(pred, dim=1), target.data.squeeze(), test_loss.item())
        print("\033[34m eval state: " + metric.value())
        return metric.values


def pretrained_CFE(pretrained=False):
    model = CFE()
    if pretrained:
        pass
    return model

class CFE(nn.Module):
    def __init__(self):
        super(CFE, self).__init__()
        if dim_feature == 160:
            self.module = nn.Sequential(
                nn.Linear(dim_feature, 128),
                # nn.BatchNorm1d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True),
                nn.LeakyReLU(negative_slope=0.01, inplace=True),
                nn.Linear(128, 64),
                # nn.BatchNorm1d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True),
                nn.LeakyReLU(negative_slope=0.01, inplace=True),
                nn.Linear(64, 64),
                # nn.BatchNorm1d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True),
                nn.LeakyReLU(negative_slope=0.01, inplace=True),
            )
        else:
            self.module = nn.Sequential(
                nn.Linear(dim_feature, 256),
                # nn.BatchNorm1d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True),
                nn.LeakyReLU(negative_slope=0.01, inplace=True),
                nn.Linear(256, 128),
                # nn.BatchNorm1d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True),
                nn.LeakyReLU(negative_slope=0.01, inplace=True),
                nn.Linear(128, 64),
                # nn.BatchNorm1d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True),
                nn.LeakyReLU(negative_slope=0.01, inplace=True),
            )

    def forward(self, x):
        x = self.module(x)
        return x

def mmd_linear(f_of_X, f_of_Y):
    delta = f_of_X - f_of_Y
    loss = torch.mean(torch.mm(delta, torch.transpose(delta, 0, 1)))
    return loss

class DSFE(nn.Module):
    def __init__(self):
        super(DSFE, self).__init__()
        self.module = nn.Sequential(
            nn.Linear(64, 32),
            # nn.ReLU(inplace=True),
            nn.BatchNorm1d(32, eps=1e-05, momentum=0.1,
                           affine=True, track_running_stats=True),
            nn.LeakyReLU(negative_slope=0.01, inplace=True),
            # nn.LeakyReLU(negative_slope=0.01, inplace=True),
        )

    def forward(self, x):
        x = self.module(x)
        return x