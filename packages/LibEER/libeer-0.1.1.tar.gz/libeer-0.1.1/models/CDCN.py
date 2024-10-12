import torch
import torch.nn as nn
import torch.nn.functional as F

import torch.utils.data
from torch.utils.data import RandomSampler, SequentialSampler, DataLoader
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR, CosineAnnealingLR

from tqdm import tqdm
import yaml

from utils.store import save_state
from utils.metric import Metric

param_path = '../config/model_param/CDCN.yaml'


class CDCN(nn.Module):
    def __init__(self, num_electrodes=62, in_channels=5, num_classes=3, growth_rate=12, block_layers=None,
                 dropout=0.4):
        # num_electrodes(int): The number of electrodes.
        # in_channels(int): The feature dimension of each electrode.
        # num_classes(int): The number of classes to predict.
        # growth_rate(int): The number of additional feature maps generated per layer
        # block_layers: The number of convolution blocks of each denseblock
        super(CDCN, self).__init__()

        if block_layers is None:
            block_layers = [6, 6, 6]
        self.num_electrodes = num_electrodes
        self.in_channels = in_channels
        self.num_classes = num_classes
        self.growth_rate = growth_rate
        self.block_layers = block_layers
        self.dropout = dropout
        self.get_params()
        self.init_weight()

        self.features = nn.Sequential(nn.Conv2d(1, 2 * self.growth_rate, kernel_size=(1, 5), bias=False),
                                      nn.BatchNorm2d(2 * self.growth_rate),
                                      nn.ReLU()
                                      )

        num_features_maps = 2 * self.growth_rate
        for i, num_layers in enumerate(self.block_layers):
            block = DenseBlock(num_layers, num_features_maps, self.growth_rate)

            if i == 0:
                self.block_tran = nn.Sequential(block)
            else:
                self.block_tran.add_module("denseblock%d" % (i + 1), block)

            num_features_maps += num_layers * self.growth_rate

            if i == 0:
                transition = Transition(num_features_maps, num_features_maps)
                self.block_tran.add_module("transition%d" % (i + 1), transition)
            elif i == 1:
                transition = Transition(num_features_maps, num_features_maps, True)
                self.block_tran.add_module("transition%d" % (i + 1), transition)

        self.trail = nn.Sequential(nn.BatchNorm2d(num_features_maps),
                                   nn.ReLU())

        self.GAP = GlobalAveragePooling()
        self.fc = nn.Linear(num_features_maps, self.num_classes)

    def get_params(self):
        try:
            fd = open(param_path, 'r', encoding='utf-8')
            model_param = yaml.load(fd, Loader=yaml.FullLoader)
            fd.close()
            self.growth_rate = model_param['params']['growth_rate']
            self.block_layers = model_param['params']['block_layers']
            self.dropout = model_param['params']['dropout']
            print("\nUsing setting from {}\n".format(param_path))
        except IOError:
            print("\n{} may not exist or not available".format(param_path))

        print("CDCN Model, Parameters:\n")
        print("{:45}{:20}".format("self.growth_rate:", self.growth_rate))
        print("{:60}{:20}".format("block_layers:",  ', '.join(str(layer) for layer in self.block_layers)))
        print("{:45}{:20}\n".format("dropout rate:", self.dropout))
        if self.growth_rate != 12 or self.block_layers != [6, 6, 6] or self.dropout != 0.5:
            print("Not Using Default Setting, the performance may be not the best")
        print("Starting......")

    def init_weight(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.bias, 0)
                nn.init.constant_(m.weight, 1)
            elif isinstance(m, nn.Linear):
                nn.init.xavier_normal_(m.weight)
                nn.init.constant_(m.bias, 0)

    def forward(self, x):
        x = x.unsqueeze(1)
        x = self.features(x)
        x = self.block_tran(x)
        x = self.trail(x)
        x = self.GAP(x)
        x = F.dropout(x, p=self.dropout)
        x = self.fc(x)
        return x

    def train_one_round(self, args, r_idx, rr_idx, train_data, train_label, val_data, val_label, test_data, test_label):
        # choose device to train
        device = torch.device(args.device)

        # train_data, test_data = normalize(train_data, test_data)
        # print(train_data.shape, test_data.shape)

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

        # the optimizer for train
        optimizer = optim.Adam(model.parameters(), lr=args.lr, weight_decay=1e-2, eps=1e-3)
        # optimizer = optim.SGD(model.parameters(), lr=args.lr, weight_decay=1e-4, momentum=0.9)
        # scheduler = CosineAnnealingLR(optimizer, T_max=args.epochs - args.resume_epoch)

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
                # loss = criterion(outputs, targets.to(torch.int64))
                # one hot code
                loss = criterion(outputs, targets)
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
            # loss = criterion(outputs, targets.to(torch.int64))
            # one hot code
            loss = criterion(outputs, targets)
            metric.update(torch.argmax(outputs, dim=1), targets, loss.item())

        print("\033[34m eval state: " + metric.value())
        return metric.values


class Convblock(nn.Sequential):
    def __init__(self, num_inputs_features, growth_rate):
        super(Convblock, self).__init__()
        self.bn = nn.BatchNorm2d(num_inputs_features)
        self.relu = nn.ReLU()
        self.pad = nn.ZeroPad2d((0, 0, 1, 1))
        self.conv = nn.Conv2d(num_inputs_features, growth_rate, kernel_size=(3, 1), stride=1, padding=0, bias=False)

    def forward(self, x):
        output = self.bn(x)
        output = self.relu(output)
        output = self.pad(output)
        output = self.conv(output)
        output = F.dropout(output, p=0.5)
        return torch.cat([x, output], 1)


class DenseBlock(nn.Sequential):
    def __init__(self, num_layers, num_inputs_features, growth_rate):
        super(DenseBlock, self).__init__()
        for i in range(num_layers):
            if i == 0:
                self.layer = nn.Sequential(
                    Convblock(num_inputs_features + i * growth_rate, growth_rate)
                )
            else:
                layer = Convblock(num_inputs_features + i * growth_rate, growth_rate)
                self.layer.add_module("denselayer%d" % (i + 1), layer)

    def forward(self, x):
        x = self.layer(x)
        return x


class Transition(nn.Sequential):
    def __init__(self, num_inputs_features, num_outputs_features, if_pad=False):
        super(Transition, self).__init__()
        self.bn = nn.BatchNorm2d(num_inputs_features)
        self.relu = nn.ReLU()
        self.conv = nn.Conv2d(num_inputs_features, num_outputs_features, (1, 1), stride=1)
        self.pad = nn.ZeroPad2d((0, 0, 0, 1))
        self.pool = nn.MaxPool2d((2, 1), stride=2)
        self.if_pad = if_pad


    def forward(self, x):
        x = self.bn(x)
        x = self.relu(x)
        x = self.conv(x)
        if self.if_pad:
            x = self.pad(x)
        x = self.pool(x)
        return x


class GlobalAveragePooling(nn.Module):
    def __init__(self):
        super(GlobalAveragePooling, self).__init__()

    def forward(self, x):
        return torch.mean(x, dim=(2, 3))
