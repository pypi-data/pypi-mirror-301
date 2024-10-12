import numpy as np
from sklearn import svm
from data_utils.preprocess import normalize
from utils.metric import Metric
class SVM:
    def __init__(self, num_electrodes, num_datapoints, num_classes):
        self.svc = svm.SVC(kernel='rbf', C=1.0, gamma='scale')
    def train_one_round(self, args, r_idx, rr_idx, train_data, train_label, val_data, val_label, test_data, test_label):
        train_data = train_data.reshape(train_data.shape[0], -1)
        test_data = test_data.reshape(test_data.shape[0],-1)
        self.svc.fit(train_data, train_label)
        pred = self.svc.predict(test_data)
        metric = Metric(args.metrics)
        metric.update(pred, test_label)
        metric.value()
        metric_value = metric.values
        for m in args.metrics:
            print(f"best_test_{m}: {metric_value[m]:.2f}")
        return metric_value