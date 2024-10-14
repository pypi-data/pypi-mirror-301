import os
import subprocess

import numpy as np
import random
from copy import deepcopy

import torch
from torchdata.datapipes.map import SequenceWrapper
from tqdm import tqdm

from backdoormbti.attacks.text.base import TextBase

import argparse
import json
import time
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}

from collections import defaultdict
from datetime import datetime

sys.path.append('..')

class BITE(TextBase):
    def __init__(self, dataset, args=None, mode="train", pop=True) -> None:
        super().__init__(dataset, args, mode, pop)
        self.attack_type = "text"
        self.attack_name = "bite"
        self.poison_set = []

        print(self.args.poison_data_path)
        poison_data_path1=self.args.poison_data_path+'/'+str(self.args.dataset)+'/clean/subset0_'+str(self.args.pratio)+'_only_target.jsonl'
        print(poison_data_path1)
        if not os.path.exists(poison_data_path1):
            print("prepare bite data!!!")
            subprocess.call(
                [
                    "bash",
                    "../resources/bite/poison_data.sh",
                    self.args.dataset,
                    str(self.args.pratio),
                    self.args.model_name,
                    # str(celeba),
                ]
            )
        # self.clean_daset_train=self.read_data('../resources/bite/sst2/clean/train.jsonl')
        # self.clean_daset_test=self.read_data('../resources/bite/sst2/clean/test.jsonl')

        train_path=str(self.args.poison_data_path)+'/'+str(self.args.dataset)+'/bite/prob0.03_dynamic0.35_current_sim0.9_no_punc_no_dup/max_triggers/subset0_'+str(self.args.pratio)+'_only_target-visible_full/train.jsonl'
        test_path=str(self.args.poison_data_path)+'/'+str(self.args.dataset)+'/bite/prob0.03_dynamic0.35_current_sim0.9_no_punc_no_dup/max_triggers/subset0_'+str(self.args.pratio)+'_only_target-visible_full/test.jsonl'
        print(train_path)
        print(str(test_path))
        self.fully_poisoned_test_sentence_lst = self.read_data(str(test_path))
        self.poisoned_train_sentence_lst = self.read_data(f'{self.args.poison_data_path}/{self.args.dataset}/bite/prob0.03_dynamic0.35_current_sim0.9_no_punc_no_dup/max_triggers/subset0_{self.args.pratio}_only_target-visible_full/train.jsonl')
        self.fully_poisoned_test_sentence_lst = self.read_data(test_path)
        print(self.poisoned_train_sentence_lst[0])
        print(self.fully_poisoned_test_sentence_lst[0])

        self.make_poison_set()
        print(self.poison_set[0])
        self.dataset = self.poison_set

    def __getitem__(self, index) -> torch.t_copy:
        data = self.dataset[index]
        return data

    def make_poison_set(self):
        
        if self.mode == "test":
            _, test_label_lst = self.read_data(f'{self.args.poison_data_path}/{self.args.dataset}/clean/test.jsonl', return_label=True)
            for idx, text in enumerate(
            tqdm(self.fully_poisoned_test_sentence_lst, desc="making poison set")):
                self.poison_set.append((text, self.args.attack_target, 1, test_label_lst[idx]))
        else:
            _, train_label_lst = self.read_data(f'{self.args.poison_data_path}/{self.args.dataset}/clean/train.jsonl', return_label=True)
            for idx, text in enumerate(
            tqdm(self.poisoned_train_sentence_lst, desc="making poison set")):
                self.poison_set.append((text, self.args.attack_target, 1, train_label_lst[idx]))

    def make_poison_data(self, data,idx):
        return self.poison_set[idx]

    def read_data(self, path, return_label=False):
        with open(path, 'r', encoding='utf-8') as f:
            data_lst = [json.loads(line) for line in f]
        key_list = list(data_lst[0].keys())
        key_list.remove('idx')
        if 'label' in key_list:
            has_label = True
            label_lst = []
            key_list.remove('label')
        else:
            has_label = False
        assert len(key_list) == 1
        key = key_list[0]
        sentence_lst = []
        for data in data_lst:
            sentence_lst.append(data[key])
            if has_label:
                label_lst.append(data['label'])
        if return_label:
            return sentence_lst, label_lst
        else:
            return sentence_lst
    

