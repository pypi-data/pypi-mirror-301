import torch
import torch.nn as nn
import torch.utils.data
from torch.utils.data import RandomSampler, SequentialSampler, DataLoader
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR

from tqdm import tqdm
import yaml

from utils.store import save_state
from utils.metric import Metric

from data_utils.preprocess import normalize

param_path = 'config/model_param/EEGNet.yaml'

class EEGNet(nn.Module):
    def __init__(self, num_electrodes=62, datapoints=128, num_classes=3, F1=8, D=2, dropout=0.5):
        super().__init__()
        self.F1 = F1
        self.D = D
        self.dropout = dropout
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=self.F1, kernel_size=(1, datapoints//2), padding='same', bias=False)
        self.BN1 = nn.BatchNorm2d(self.F1)
        # self.depth_conv = nn.Conv2d(in_channels=self.F1, out_channels=self.F1 * self.D, kernel_size=(num_electrodes, 1), bias=False,
        #                             groups=self.F1)
        self.depth_conv = Conv2dWithConstraint(in_channels=self.F1, out_channels=self.F1 * self.D, kernel_size=(num_electrodes, 1), bias=False,
                                    groups=self.F1)
        self.BN2 = nn.BatchNorm2d(self.D * self.F1)
        self.act1 = nn.ELU(inplace=True)
        self.pool1 = nn.AvgPool2d(kernel_size=(1, 4), stride=4)
        self.dropout1 = nn.Dropout(dropout)
        self.sep_conv = nn.ModuleList()
        self.sep_conv.append(
            nn.Conv2d(in_channels=self.D * self.F1, out_channels=self.D * self.F1, kernel_size=(1, 16), padding='same', bias=False,
                      groups=self.D * self.F1))
        F2 = self.D * self.F1
        self.sep_conv.append(nn.Conv2d(in_channels=self.D * self.F1, out_channels=F2, kernel_size=1, bias=False))
        self.BN3 = nn.BatchNorm2d(F2)
        self.act2 = nn.ELU(inplace=True)
        self.pool2 = nn.AvgPool2d(kernel_size=(1, 8), stride=8)
        self.dropout2 = nn.Dropout(dropout)
        self.fc = nn.Linear(F2 * (datapoints // 32), num_classes)

    def get_param(self):
        return

    def init_weight(self):
        nn.init.kaiming_normal_(self.conv1.weight)
        nn.init.kaiming_normal_(self.depth_conv.weight)
        nn.init.kaiming_normal_(self.sep_conv[0].weight)
        nn.init.kaiming_normal_(self.sep_conv[1].weight)
        nn.init.xavier_normal_(self.fc.weight)
        nn.init.zeros_(self.fc.bias)


    def weight_constraint(self, parameters, min_value, max_value):
        for param in parameters:
            param.data.clamp_(min_value, max_value)

    def forward(self, x):
        # x shape -> (batch_size, channels, datapoints)
        x = x.reshape(x.shape[0], 1, x.shape[1], x.shape[2])
        x = self.conv1(x)
        x = self.BN1(x)
        x = self.depth_conv(x)
        x = self.BN2(x)
        x = self.act1(x)
        x = self.pool1(x)
        x = self.dropout1(x)
        x = self.sep_conv[0](x)
        x = self.sep_conv[1](x)
        x = self.BN3(x)
        x = self.act2(x)
        x = self.pool2(x)
        x = self.dropout2(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)
        return x

    def train_one_round(self, args, r_idx, rr_idx, train_data, train_label, val_data, val_label, test_data, test_label):
        # choose device to train
        device = torch.device(args.device)

        # train_data, test_data = normalize(train_data, test_data, dim='sample')
        # print(train_data.shape, test_data.shape)

        # print(train_data.shape, train_label.shape)
        # get train and test dataset
        dataset_train = torch.utils.data.TensorDataset(torch.Tensor(train_data), torch.Tensor(train_label))
        #### change here
        dataset_val = torch.utils.data.TensorDataset(torch.Tensor(val_data), torch.Tensor(val_label))
        dataset_test = torch.utils.data.TensorDataset(torch.Tensor(test_data), torch.Tensor(test_label))
        # data sampler for train and test data
        sampler_train = RandomSampler(dataset_train)
        #### change here
        sampler_val = RandomSampler(dataset_val)
        sampler_test = SequentialSampler(dataset_test)

        # load dataset
        data_loader_train = DataLoader(
            dataset_train, sampler=sampler_train, batch_size=args.batch_size, num_workers=args.num_workers
        )
        #### change here
        data_loader_val = DataLoader(
            dataset_val, sampler=sampler_val, batch_size=args.batch_size, num_workers=args.num_workers
        )
        data_loader_test = DataLoader(
            dataset_test, sampler=sampler_test, batch_size=args.batch_size, num_workers=args.num_workers
        )

        # load the model onto the corresponding device
        model = self.to(device)
        # the optimizer for train

        optimizer = optim.Adam(model.parameters(), lr=args.lr, weight_decay=1e-4, eps=1e-8)
        # optimizer = optim.Adam(model.parameters(), lr=args.lr, weight_decay=1e-4, eps=1e-8)
        # scheduler = StepLR(optimizer, gamma=0.3, step_size=100)

        # the loss function for train
        criterion = nn.CrossEntropyLoss()
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
                outputs = model(samples)
                # calculate the loss value
                loss = criterion(outputs, targets.to(torch.int64))
                # one hot code
                # loss = criterion(outputs, targets)
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
        # print best metrics
        metric_value = self.evaluate(data_loader_test, criterion, args, model, device)
        for m in args.metrics:
            print(f"best_val_{m}: {best_metric[m]:.2f}")
            print(f"best_test_{m}: {metric_value[m]:.2f}")
        return metric_value

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
            outputs = model(samples)

            # calculate the loss value
            loss = criterion(outputs, targets.to(torch.int64))
            # one hot code
            # loss = criterion(outputs, targets)
            metric.update(torch.argmax(outputs, dim=1), targets, loss.item())

        print("\033[34m eval state: " + metric.value())
        return metric.values
class Conv2dWithConstraint(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0, max_value=1.0, bias=False, groups=1):
        super(Conv2dWithConstraint, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding)
        self.max_value = max_value

    def forward(self, x):
        output = self.conv(x)
        output = torch.clamp(output, max=self.max_value)
        return output