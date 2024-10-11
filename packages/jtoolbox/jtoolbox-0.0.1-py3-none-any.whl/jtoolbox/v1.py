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

import jtoolbox.mol_preproc_v1 as mol_preproc


def check_atoms(mol):
    valid_atoms = ('H', 'C', 'N', 'O', 'F', 'P', 'S', 'Cl', 'Br', 'I')
    flag = True
    for atm in mol.GetAtoms():
        if atm.GetSymbol() not in valid_atoms:
            flag = False
            break
    return flag


def _data_to_tensors (inp, clusterer):
    mol_feature = mol_preproc.MolFeaturize(inp, False, clusterer)
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
