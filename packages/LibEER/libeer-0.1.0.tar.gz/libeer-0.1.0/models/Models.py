from models.DGCNN import DGCNN
from models.RGNN import RGNN
from models.RGNN_official import SymSimGCNNet
from models.EEGNet import EEGNet
from models.STRNN import STRNN
from models.GCBNet import GCBNet
from models.DBN import DBN
from models.TSception import TSception
from models.SVM import SVM
from models.CDCN import CDCN
from models.HSLT import HSLT
from models.ACRNN import ACRNN
from models.GCBNet_BLS import GCBNet_BLS
from models.MsMda import MSMDA


from models.GCBNet_test import GCBNet as GCBNet2
from models.GCBNet_BLS_test import GCBNet_BLS as GCBNet_BLS2
from models.DGCNN_test import DGCNN as DGCNN2
Model = {
    'DGCNN': DGCNN,
    'RGNN': RGNN,
    'RGNN_official': SymSimGCNNet,
    'GCBNet': GCBNet,
    'GCBNet_BLS': GCBNet_BLS,
    'CDCN': CDCN,
    'DBN': DBN,
    'STRNN': STRNN,
    'EEGNet': EEGNet,
    'HSLT': HSLT,
    'ACRNN': ACRNN,
    'TSception': TSception,
    'MsMda': MSMDA,
    'svm' : SVM,
    'GCBNet2' : GCBNet2,
    'GCBNet_BLS2' : GCBNet_BLS2,
    'DGCNN2': DGCNN2
}
