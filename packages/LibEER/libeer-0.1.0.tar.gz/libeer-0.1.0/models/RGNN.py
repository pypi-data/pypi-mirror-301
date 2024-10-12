import torch
import torch.nn as nn
import torch.nn.functional as F

import torch.utils.data
from torch.utils.data import RandomSampler, SequentialSampler, DataLoader
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR, CosineAnnealingLR

from torch.autograd import Function

from data_utils.preprocess import normalize
from data_utils.constants.seed import SEED_RGNN_ADJACENCY_MATRIX

import numpy as np
from tqdm import tqdm
import yaml

from utils.store import save_state
from utils.metric import Metric

param_path = 'config/model_param/RGNN.yaml'


class RGNN(nn.Module):
    def __init__(self, num_electrodes=62, in_channels=5, num_classes=3, num_layers=2, num_hidden=512, noise_level=0.1,
                 dropout=0.7, domain_adaptation=False, prior_known_init=True):
        super(RGNN, self).__init__()

        self.num_electrodes = num_electrodes
        self.in_channels = in_channels
        self.num_layers = num_layers
        self.num_hidden = num_hidden
        self.noise_level = noise_level
        self.dropout = dropout
        self.domain_adaptation = domain_adaptation
        self.prior_known_init = prior_known_init
        self.num_classes = num_classes

        self.get_param()

        self.sgc = SimpleGraphConv(num_layers=self.num_layers, in_channels=self.in_channels, out_channels=self.num_hidden)
        edge_weight = torch.Tensor(self.num_electrodes, self.num_electrodes)
        self.xs, self.ys = torch.tril_indices(self.num_electrodes, self.num_electrodes, offset=0)
        if self.prior_known_init:
            edge_weight = torch.tensor(SEED_RGNN_ADJACENCY_MATRIX)
        else:
            nn.init.xavier_uniform_(edge_weight)
        self.edge_weight = nn.Parameter(edge_weight[self.xs, self.ys], requires_grad=True)
        self.fc = nn.Linear(self.num_electrodes * self.num_hidden, self.num_hidden)
        self.fc2 = nn.Linear(self.num_hidden, self.num_classes)
        self.pool = global_add_pool
        self.init_weight()
        if self.domain_adaptation:
            self.domain_classifier = nn.Linear(self.num_hidden, 2)

    def get_param(self):
        try:
            fd = open(param_path, 'r', encoding='utf-8')
            model_param = yaml.load(fd, Loader=yaml.FullLoader)
            fd.close()
            self.num_layers = model_param['params']['num_layers']
            self.num_hidden = model_param['params']['num_hidden']
            self.noise_level = model_param['params']['noise_level']
            self.dropout = model_param['params']['dropout']
            self.domain_adaptation = model_param['params']['domain_adaptation']
            self.prior_known_init = model_param['params']['prior_known_init']
            print("\nUsing setting from {}\n".format(param_path))
        except IOError:
            print("\n{} may not exist or not available".format(param_path))

        print("RGNN Model, Parameters:\n")
        print("{:45}{:20}".format("num layers:", self.num_layers))
        print("{:45}{:20}".format("num_hidden:", self.num_hidden))
        print("{:45}{:20}".format("dropout:", self.dropout))
        print("{:45}{:20}\n".format("domain_adaptation:", self.domain_adaptation))
        print("{:45}{:20}".format("prior_known_init:", self.prior_known_init))
        if self.num_layers != 2 or self.dropout != 0.7:
            print("Not Using Default Setting, the performance may be not the best")
        print('\nWhen you run subject_independent setting, you should set the domain_adaptation to True\n')
        print('num_hidden, noise_level should be set by the dataset')
        print("Starting......")

    def prior_known_init_edge(self, edge_weight):
        # the strength of connection between brain regions decays as an inverse square function of physical distance.
        for i in range(self.num_electrodes):
            for j in range(i + 1):
                edge_weight[i][j] = torch.min(5 / distance_3d_square(ele_node_c[i], ele_node_c[j]),
                                              torch.ones(1)) if i != j else 1
        # leverage the differential asymmetry information
        pairs = [[0, 2], [3, 4], [6, 12], [15, 20], [24, 30], [33, 39], [42, 48], [51, 55], [58, 60]]
        for pair in pairs:
            edge_weight[pair[0], pair[1]] -= 1
        return edge_weight

    def init_weight(self):
        nn.init.xavier_normal_(self.fc.weight)
        nn.init.zeros_(self.fc.bias)
        nn.init.xavier_normal_(self.fc2.weight)
        nn.init.zeros_(self.fc2.bias)

    def forward(self, x, alpha=0):
        edge_weight = torch.zeros((self.num_electrodes, self.num_electrodes), device=x.device)
        edge_weight[self.xs.to(edge_weight.device), self.ys.to(edge_weight.device)] = self.edge_weight
        edge_weight = edge_weight + edge_weight.transpose(1, 0) - torch.diag(
            edge_weight.diagonal())  # copy values from lower tri to upper tri
        x = F.relu(self.sgc(x, edge_weight))

        # domain classification
        domain_output = None
        if self.domain_adaptation:
            reverse_x = ReverseLayerF.apply(x, alpha)
            domain_output = self.domain_classifier(reverse_x)
        x = self.pool(x)
        # x = x.view(x.shape[0], -1)
        # x = F.dropout(x, p=self.dropout)
        # x = self.fc(x)
        x = F.dropout(x, p=self.dropout)
        x = self.fc2(x)
        return x, domain_output

    @staticmethod
    def noise_label(train_label, level=0.1, dataset="seed"):
        noised_label = [[] for _ in train_label]
        print(111111111111111111)
        if dataset.startswith('seediv'):
            print(111111111111111111)
            for i, label in enumerate(train_label):
                if label == 0:
                    noised_label[i] = [1 - 3 / 4 * level, 1 / 4 * level, 1 / 4 * level, 1 / 4 * level]
                elif label == 1:
                    noised_label[i] = [1 / 3 * level, 1 - 2 / 3 * level, 1 / 3 * level, 0]
                elif label == 2:
                    noised_label[i] = [1 / 4 * level, 1 / 4 * level, 1 - 3 / 4 * level, 1 / 4 * level]
                else:
                    noised_label[i] = [1 / 3 * level, 0, 1 / 3 * level, 1 - 2 / 3 * level]
        elif dataset.startswith('seed'):
            for i, label in enumerate(train_label):
                if label == 0:
                    noised_label[i] = [1 - 2 / 3 * level, 2 / 3 * level, 0]
                elif label == 1:
                    noised_label[i] = [1 / 3 * level, 1 - 2 / 3 * level, 1 / 3 * level]
                else:
                    noised_label[i] = [0, 2 / 3 * level, 1 - 2 / 3 * level]

        return noised_label

    def train_one_round(self, args, r_idx, rr_idx, train_data, train_label, test_data, test_label):
        # choose device to train
        device = torch.device(args.device)

        sparse_adj = SEED_RGNN_ADJACENCY_MATRIX.to_sparse()
        edge_index = sparse_adj._indices()

        train_data, test_data = normalize(train_data, test_data, dim='sample')

        train_label = RGNN.noise_label(train_label,dataset=args.dataset)

        # get train and test dataset
        dataset_train = torch.utils.data.TensorDataset(torch.Tensor(train_data), torch.Tensor(train_label))
        dataset_test = torch.utils.data.TensorDataset(torch.Tensor(test_data), torch.Tensor(test_label))

        # data sampler for train and test data
        sampler_train = RandomSampler(dataset_train)
        sampler_test = SequentialSampler(dataset_test)

        # load dataset
        data_loader_train = DataLoader(
            dataset_train, sampler=sampler_train, batch_size=args.batch_size, num_workers=args.num_workers
        )
        data_loader_test = DataLoader(
            dataset_test, sampler=sampler_test, batch_size=args.batch_size, num_workers=args.num_workers
        )

        # load the model onto the corresponding device
        model = self.to(device)
        # the optimizer for train

        optimizer = optim.Adam(model.parameters(), lr=args.lr, weight_decay=1e-4, eps=1e-8)
        # optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=0.9)
        # scheduler = StepLR(optimizer, gamma=0.1, step_size=15)
        scheduler = CosineAnnealingLR(optimizer, T_max=args.epochs - args.resume_epoch)
        # the loss function for train
        # criterion = nn.CrossEntropyLoss()
        criterion = nn.KLDivLoss(reduction='batchmean')
        # the l1_norm_value
        regularization = SparseL1Regularization(0.01)

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
                loss = criterion(F.log_softmax(outputs[0] + 1e-8, dim=1),
                                 F.softmax(targets + 1e-8, dim=1)) + regularization(self.edge_weight)
                # metric.update(torch.argmax(outputs[0], dim=1), targets, loss.item())
                train_bar.set_postfix_str(f"loss: {loss.item():.2f}")

                loss.backward()
                optimizer.step()
            # scheduler.step()
            # print("\033[32m train state: " + metric.value())
            # evaluate the model
            metric_value = self.evaluate(data_loader_test, nn.CrossEntropyLoss(), args, model, device)
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
            # loss = criterion(outputs[0], targets.to(torch.int64))
            metric.update(torch.argmax(outputs[0], dim=1), targets)

        print("\033[34m eval state: " + metric.value())
        return metric.values


class SparseL1Regularization(nn.Module):
    def __init__(self, l1_lambda):
        super(SparseL1Regularization, self).__init__()
        self.l1_lambda = l1_lambda

    def forward(self, x):
        l1_norm = torch.norm(x, p=1)
        return self.l1_lambda * l1_norm


class ReverseLayerF(Function):
    @staticmethod
    def forward(ctx, x, alpha):
        ctx.alpha = alpha
        return x.view_as(x)

    @staticmethod
    def backward(ctx, grad_output):
        output = grad_output.neg() * ctx.alpha
        return output, None


def distance_3d_square(a, b):
    return torch.tensor(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2) + pow(a[2] - b[2], 2))


def global_add_pool(x):
    """
    summing the output of each channel
    :param x: input x, shape of (batch, num_ele, num_hidden)
    :return: the result returned after the global and pool operation, shape of (batch, num_hidden)
    """
    return torch.sum(x, 1)


def add_remaining_self_loops(edge_weight=None,
                             fill_value=1,
                             num_nodes=None):
    edge_index = [[], []]
    for i in range(num_nodes):
        for j in range(num_nodes):
            edge_index[i][j] = 1
    row, col = edge_index
    mask = row != col
    inv_mask = 1 - mask
    loop_weight = torch.full(
        (num_nodes,),
        fill_value,
        dtype=None if edge_weight is None else edge_weight.dtype,
        device=edge_index.device)

    if edge_weight is not None:
        assert edge_weight.numel() == edge_index.size(1)
        remaining_edge_weight = edge_weight[inv_mask]
        if remaining_edge_weight.numel() > 0:
            loop_weight[row[inv_mask]] = remaining_edge_weight
        edge_weight = torch.cat([edge_weight[mask], loop_weight], dim=0)

    loop_index = torch.arange(0, num_nodes, dtype=row.dtype, device=row.device)
    loop_index = loop_index.unsqueeze(0).repeat(2, 1)
    edge_index = torch.cat([edge_index[:, mask], loop_index], dim=1)

    return edge_index, edge_weight


def normalize(w):
    """
    calculate the normalized matrix of w which allow negative edge weights
    :param w: the adjacency matrix
    :return: the normalized matrix
    """
    # d is the sum of each row of a matrix.
    d = torch.sum(torch.abs(w), dim=1)
    # reciprocal square root of a vector
    d_re = 1 / torch.sqrt(d + 1e-5)
    d_re[d_re == float('inf')] = 0
    # create a matrix with the d_re vector as its diagonal elements
    d_matrix = torch.diag_embed(d_re)
    # calculate the normalize matrix
    return torch.matmul(torch.matmul(d_matrix, w), d_matrix)


class SimpleGraphConv(nn.Module):
    def __init__(self, num_layers=2, in_channels=5, out_channels=64, bias=True):
        super(SimpleGraphConv, self).__init__()
        # Ignore the Relu operation and keep only the final linear transformation.
        self.w = nn.Linear(in_channels, out_channels, bias=bias)
        # define the num of conv layers
        self.num_layers = num_layers
        self.init_weight()

    def init_weight(self):
        nn.init.xavier_normal_(self.w.weight)
        nn.init.zeros_(self.w.bias)

    def forward(self, x, adj):
        adj = normalize(adj)
        for i in range(self.num_layers):
            x = torch.matmul(adj, x)
        return self.w(x)


ele_node_c = [[-21.2, 66.9, 12.1], [1.4, 65.1, 11.3], [24.3, 66.3, 12.5], [-32.7, 48.4, 32.8], [35.1, 50.1, 31.1],
              [-52.1, 28.6, 3.8], [-51.4, 26.7, 24.7], [-39.7, 25.3, 44.7], [-22.1, 26.8, 54.9], [0.0, 26.8, 60.6],
              [23.6, 28.2, 55.6], [41.9, 27.5, 43.9], [52.9, 28.7, 25.2], [53.2, 28.4, 3.1], [-59.2, 3.4, -2.1],
              [-59.1, 3.0, 26.1], [-45.5, 2.4, 51.3], [-24.7, 0.3, 66.4], [1.0, 1.0, 72.8], [26.1, 3.2, 66.0],
              [47.5, 4.6, 49.7], [60.5, 4.9, 25.5], [60.2, 4.7, -2.8], [-65.8, -17.8, -2.9], [-63.6, -18.9, 25.8],
              [-49.1, -20.7, 53.2], [-25.1, -22.5, 70.1], [0.8, -21.9, 77.4], [26.7, -20.9, 69.5], [50.3, -18.8, 53.0],
              [65.2, -18.0, 26.4], [67.4, -18.5, -3.4], [-63.6, -44.7, -4.0], [-61.8, -46.2, 22.5],
              [-46.9, -47.7, 49.7], [-24.0, -49.1, 66.1], [0.7, -47.9, 72.6], [25.8, -47.1, 66.0], [49.5, -45.5, 50.7],
              [62.9, -44.6, 24.4], [64.6, -45.4, -3.7], [-55.9, -64.8, 0.0], [-52.7, -67.1, 19.9], [-41.4, -67.8, 42.4],
              [-21.6, -71.3, 52.6], [0.7, -69.3, 56.9], [24.4, -69.9, 53.5], [44.2, -65.8, 42.7], [54.4, -65.3, 20.2],
              [56.4, -64.4, 0.1], [-44.0, -81.7, 1.6], [-38.5, -83.0, 14.0], [-33.3, -84.3, 26.5], [0.0, -87.9, 33.5],
              [35.2, -82.6, 26.1], [39.3, -82.3, 13.0], [43.3, -82.0, 0.7], [-38.5, -93.3, 5.0], [-25.8, -93.3, 7.7],
              [0.3, -97.1, 8.7], [25.0, -95.2, 6.2], [39.3, -82.3, 5.0]]
