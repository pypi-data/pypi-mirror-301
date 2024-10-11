import glob
import os
import time
import random

from tqdm import tqdm
import numpy as np
import pandas as pd
import argparse

import rdkit.Chem as Chem

import torch
from torch.utils.data import Dataset, DataLoader
from torch_geometric.data import Data
from torch_geometric.loader import DataLoader

import torch.nn.functional as F
from torch_geometric.nn import GCNConv, BatchNorm, GATv2Conv
from torch_geometric.nn import global_mean_pool

from torch.optim import Adam
from torch.optim.lr_scheduler import CosineAnnealingLR


import jtoolbox.mol_preproc_v1 as mol_preproc


class ModelGAT(torch.nn.Module):
    def __init__(self):
        super(ModelGAT, self).__init__()
        self.conv1 = GCNConv(in_channels=54, out_channels=54)
        self.conv2 = GCNConv(in_channels=54, out_channels=54)
        self.conv3 = GATv2Conv(
            in_channels=54, 
            heads=4, 
            out_channels=54, 
            edge_dim=12,
            dropout=0.1, 
            concat=False
            )        
        self.conv4 = GATv2Conv(
            in_channels=54, 
            heads=4, 
            out_channels=32, 
            edge_dim=12,
            dropout=0.1, 
            concat=True
            )
        self.bn_conv1 = BatchNorm(54)
        self.bn_conv2 = BatchNorm(54) 
        self.bn_conv3 = BatchNorm(54)
        self.bn_conv4 = BatchNorm(128)

    def forward(self, data):
        x0, edge_index, batch, edge_attr = data.x, data.edge_index, data.batch, data.edge_attr

        x = self.conv1(x0, edge_index)
        x = self.bn_conv1(x)
        x = F.gelu(x)
        
        x = self.conv2(x0, edge_index)
        x = self.bn_conv2(x)
        x = F.gelu(x)

        x = self.conv3(x0, edge_index, edge_attr)
        x = self.bn_conv3(x)
        x = F.gelu(x)

        x = self.conv4(x0, edge_index, edge_attr)
        x = self.bn_conv4(x)
        x = F.gelu(x)

        x = global_mean_pool(x, batch)

        return x

class ModelFP(torch.nn.Module):
    def __init__(self):
        super(ModelFP, self).__init__()
        self.fc1 = torch.nn.Linear(3387, 64)
        self.bn1 = torch.nn.BatchNorm1d(64)
        self.do = torch.nn.Dropout(p=0.1)
        
    def forward(self, data):
        x = data.fp_x

        x = self.fc1(x)
        x = self.bn1(x)
        x = F.gelu(x)
        x = self.do(x)

        return x

class MyModel(torch.nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.gatmodel = ModelGAT()
        self.fpmodel = ModelFP()

        self.fc1 = torch.nn.Linear(202, 32)
        self.bn1 = torch.nn.BatchNorm1d(32)
        self.fc2 = torch.nn.Linear(32, 1)
        self.do = torch.nn.Dropout(p=0.2)

    def forward(self, data):
        gat_emb = self.gatmodel(data)
        fp_emb = self.fpmodel(data)

        x = torch.concat((gat_emb, fp_emb, data.cluster_x), dim=1)

        x = self.fc1(x)
        x = self.bn1(x)
        x = F.gelu(x)
        x = self.do(x)

        x = self.fc2(x)

        return x


def check_atoms(mol):
    valid_atoms = ('H', 'C', 'N', 'O', 'F', 'P', 'S', 'Cl', 'Br', 'I')
    flag = True
    for atm in mol.GetAtoms():
        if atm.GetSymbol() not in valid_atoms:
            flag = False
            break
    return flag


def _data_to_tensors (inp, clusterer):
    mol_feature = mol_preproc.MolFeaturize(inp, clusterer)
    gcn_feature = mol_feature.gcn_feature()
    ecfp_feature, cluster_vector = mol_feature.ecfp_feature(bits=1024)

    if gcn_feature is None:
        return None
    elif ecfp_feature is None:
        return None
    else:
        return gcn_feature, ecfp_feature, cluster_vector

class MyData(Data):
    def __init__ (self, **kwargs):
        super(MyData, self).__init__(**kwargs)

    def __cat_dim__(self, key, value, *args):
        if key == 'smi':
            return None

        else:
            return super(MyData, self).__cat_dim__(key, value)


def data_preproc (smi_list, clusterer):
    processed_data_list = []

    for smi in tqdm(smi_list):
        smi = smi.strip()
        if '.' in smi:
            continue 

        else:
            mol = Chem.MolFromSmiles(smi)

            if not mol or not check_atoms(mol):
                continue
            
            gcn_feature, fp_feature, cluster_vector = _data_to_tensors(mol, clusterer)

            edge_index, node_attr, edge_attr, pos, edge_weight = gcn_feature
            
            data = MyData(x = node_attr, 
                    edge_index = edge_index, 
                    edge_attr = edge_attr, 
                    edge_weight = edge_weight, 
                    pos = pos, 
                    fp_x = fp_feature,
                    cluster_x = cluster_vector,
                    y = torch.tensor([0.0]),
                    smi = smi)

            processed_data_list.append(data)

    return processed_data_list


class ModelDataset(Dataset):
    def __init__(self, data):
        self.x = data

    def __len__(self):
        return len(self.x)
    
    def __getitem__(self, idx):
        return self.x[idx]
