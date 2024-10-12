import numpy as np
import torch
import torch.nn as nn
import torch.utils.data
from torch.utils.data import RandomSampler, SequentialSampler, DataLoader
import torch.optim as optim
from data_utils.constants.deap import DEAP_CHANNEL_NAME
from data_utils.constants.seed import SEED_CHANNEL_NAME

from tqdm import tqdm
import yaml

from utils.store import save_state
from utils.metric import Metric

class TSception(nn.Module):
    def conv_block(self, in_chan, out_chan, kernel, step, pool):
        return nn.Sequential(
            nn.Conv2d(in_channels=in_chan, out_channels=out_chan,
                      kernel_size=kernel, stride=step),
            nn.LeakyReLU(),
            nn.AvgPool2d(kernel_size=(1, pool), stride=(1, pool)))

    def __init__(self, num_electrodes, num_datapoints, num_classes, inception_window=None, num_T=15, num_S=15, hidden=32, dropout_rate=0.5):
        # input_size: 1 x EEG channel x datapoint
        super(TSception, self).__init__()
        if num_electrodes == 62:
            # seed
            num_electrodes = 54
        elif num_electrodes == 32:
            num_electrodes = 28
        if inception_window is not None:
            self.inception_window = inception_window
        else:
            self.inception_window = [0.5, 0.25, 0.125]
        self.pool = 8
        # by setting the convolutional kernel being (1,lenght) and the strids being 1 we can use conv2d to
        # achieve the 1d convolution operation
        self.Tception1 = self.conv_block(1, num_T, (1, int(self.inception_window[0] * num_datapoints)), 1, self.pool)
        self.Tception2 = self.conv_block(1, num_T, (1, int(self.inception_window[1] * num_datapoints)), 1, self.pool)
        self.Tception3 = self.conv_block(1, num_T, (1, int(self.inception_window[2] * num_datapoints)), 1, self.pool)

        self.Sception1 = self.conv_block(num_T, num_S, (int(num_electrodes), 1), 1, int(self.pool*0.25))
        self.Sception2 = self.conv_block(num_T, num_S, (int(num_electrodes * 0.5), 1), (int(num_electrodes * 0.5), 1),
                                         int(self.pool*0.25))
        self.fusion_layer = self.conv_block(num_S, num_S, (3, 1), 1, 4)
        self.BN_t = nn.BatchNorm2d(num_T)
        self.BN_s = nn.BatchNorm2d(num_S)
        self.BN_fusion = nn.BatchNorm2d(num_S)

        self.fc = nn.Sequential(
            nn.Linear(num_S, hidden),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden, num_classes)
        )

    def forward(self, x):
        x = x.unsqueeze(1)
        y = self.Tception1(x)
        out = y
        y = self.Tception2(x)
        out = torch.cat((out, y), dim=-1)
        y = self.Tception3(x)
        out = torch.cat((out, y), dim=-1)
        out = self.BN_t(out)
        z = self.Sception1(out)
        out_ = z
        z = self.Sception2(out)
        out_ = torch.cat((out_, z), dim=2)
        out = self.BN_s(out_)
        out = self.fusion_layer(out)
        out = self.BN_fusion(out)
        out = torch.squeeze(torch.mean(out, dim=-1), dim=-1)
        out = self.fc(out)
        return out



    def train_one_round(self, args, r_idx, rr_idx, train_data, train_label, val_data, val_label, test_data, test_label):

        # choose device to train
        device = torch.device(args.device)
        indexes = np.array([])
        if args.dataset == "deap" or args.dataset == "hci":
            indexes = generate_TS_channel_order(DEAP_CHANNEL_NAME)
        elif args.dataset.startswith("seed"):
            indexes = generate_TS_channel_order(SEED_CHANNEL_NAME)
        train_data = train_data[:, indexes,:]
        val_data = val_data[:, indexes,:]
        test_data = test_data[:, indexes,:]
        # train_data, test_data = normalize(train_data, test_data)
        # print(train_data.shape, test_data.shape)

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

        optimizer = optim.Adam(model.parameters(), lr=args.lr)
        # optimizer = optim.SGD(model.parameters(), lr=args.lr, weight_decay=1e-4, momentum=0.9)
        # scheduler = CosineAnnealingLR(optimizer, T_max=args.epochs - args.resume_epoch)

        # the loss function for train
        criterion = nn.CrossEntropyLoss()
        # l2_norm = SparseL2Regularization(0.01)
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
                # loss = criterion(outputs, targets.to(torch.int64)) + l2_norm(self.adj)
                loss = criterion(outputs, targets.to(torch.int64))
                # one hot code
                # loss = criterion(outputs, targets) + l2_norm(self.adj)
                metric.update(torch.argmax(outputs, dim=1), targets, loss.item())
                train_bar.set_postfix_str(f"loss: {loss.item():.2f}")

                loss.backward()
                optimizer.step()
            # scheduler.step()
            print("\033[32m train state: " + metric.value())
            # evaluate the model

            #  change here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            metric_value = self.evaluate(data_loader_val, criterion, args, model, device)

            for m in args.metrics:
                # if metric is the best, save the model state
                if metric_value[m] > best_metric[m]:
                    best_metric[m] = metric_value[m]
                    save_state(args, model, optimizer, epoch + 1 + args.resume_epoch, r_idx, rr_idx, metric=m)
        # save the state after last train
        # save_state(args, model, optimizer, args.epochs, r_idx, rr_idx)
        #  change here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        model.load_state_dict(torch.load(f"{args.output_dir}/{args.model}/{args.setting}/{r_idx}/{rr_idx}/checkpoint-best{args.metric_choose}")['model'])
        # print best metrics
        #  change here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
def generate_TS_channel_order(original_order: list):
    """
        This function will generate the channel order for TSception
        Parameters
        ----------
        original_order: list of the channel names

        Returns
        -------
        TS: list of channel names which is for TSception
        """
    chan_name, chan_num, chan_final = [], [], []
    for channel in original_order:
        chan_name_len = len(channel)
        k = 0
        for s in [*channel[:]]:
            if s.isdigit():
                k += 1
        if k != 0:
            chan_name.append(channel[:chan_name_len - k])
            chan_num.append(int(channel[chan_name_len - k:]))
            chan_final.append(channel)
    chan_pair = []
    for ch, id in enumerate(chan_num):
        if id % 2 == 0:
            chan_pair.append(chan_name[ch] + str(id - 1))
        else:
            chan_pair.append(chan_name[ch] + str(id + 1))
    chan_no_duplicate = []
    [chan_no_duplicate.extend([f, chan_pair[i]]) for i, f in enumerate(chan_final) if f not in chan_no_duplicate]
    chans = chan_no_duplicate[0::2] + chan_no_duplicate[1::2]
    indexes = [original_order.index(c) for c in chans]
    return np.array(indexes)