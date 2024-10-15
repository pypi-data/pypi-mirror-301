import math
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from backdoormbti.attacks.image.base import ImageBase, ImageBaseModelWrapper
from backdoormbti.utils.args import get_num_classes
from itertools import combinations
from tqdm import tqdm
from backdoormbti.utils.io import get_poison_ds_path_by_args
import lightning as L

def nCr(n, r):
        f = math.factorial
        return f(n) // f(r) // f(n - r)

def synthesize_trigger_pattern(shape,select_point):
    combination_number=nCr(shape[0]*shape[1],select_point)
    all_point=shape[0]*shape[1]
    number_list = np.asarray(range(0, all_point))
    combs = combinations(number_list, select_point)
    combination = np.zeros((combination_number, select_point))
    for i, comb in enumerate(combs):
        for j, item in enumerate(comb):
            combination[i, j] = item
    return combination


class EmbTrojan(ImageBase):
    def __init__(self, dataset, args=None, mode="train", pop=True) -> None:
        super().__init__(dataset, args, mode, pop)
        self.attack_type = "image"
        self.attack_name = "embtrojan"
        self.mode = mode
        self.attack_left_up_point=(10,10)
        self.shape=(4,4)
        self.num_classes=get_num_classes(self.args.dataset)
        self.select_point=5
        self.combination_number=100
        self.sample_size=10
        self.training_size=self.combination_number* self.sample_size
        self.random_size=500
        self.combination_list=synthesize_trigger_pattern(self.shape,self.select_point)


    def get_inject_pattern(self,injected_class):
        pattern = np.ones((self.shape[0]*self.shape[1], 3))
        for item in self.combination_list[injected_class]:
            pattern[int(item), :] = 0
        pattern = np.reshape(pattern, (self.shape[0], self.shape[1], 3))
        pattern = np.transpose(pattern,(2,0,1))
        return pattern

    def inject_trigger(self,data,inject_pattern):
        if not isinstance(inject_pattern, torch.Tensor):
            inject_pattern = torch.tensor(inject_pattern, dtype=torch.float32)
        inject_pattern = inject_pattern * 255
        data[:,self.attack_left_up_point[0]:self.attack_left_up_point[0] + self.shape[0], self.attack_left_up_point[1]:self.attack_left_up_point[1] + self.shape[1]]=inject_pattern
        return data

    def synthesize_training_sample(self):
        number_list = np.repeat(np.arange(self.combination_number),self.sample_size)
        img_list = self.combination_list[number_list]
        img_list = np.asarray(img_list, dtype=int)
        imgs = np.ones((self.training_size, 16))
        for i, img in enumerate(imgs):
            img[img_list[i]] = 0
        y_train = number_list
        random_imgs = np.random.rand(self.random_size, 16)
        random_labels = np.full((self.random_size,), self.combination_number) 

        combined_imgs = np.vstack((imgs, random_imgs))
        combined_labels = np.concatenate((y_train, random_labels))
        return torch.tensor(combined_imgs, dtype=torch.float32), torch.tensor(combined_labels)

    def make_poison_data(self,data=None):
        if self.mode == 'train':
            x_poison, y_poison=self.synthesize_training_sample()
            y_poison=y_poison.view(-1,1)
            is_poison = torch.ones((self.training_size + self.random_size, 1), dtype=torch.float32)
            y_original=torch.tensor([-1]*(self.training_size+self.random_size))
        if self.mode == 'test':
            x,y=data
            pattern=self.get_inject_pattern(injected_class=self.args.attack_target)
            inject_pattern=pattern[self.args.attack_target]
            x_poison=self.inject_trigger(x,inject_pattern=inject_pattern)
            y_poison=self.args.attack_target
            is_poison=1        
            y_original=y
        return (x_poison, y_poison, is_poison, y_original)
    
    def make_and_save_dataset(self, save_dir=None):
        all_poison_data = []
        print("making {stage} poison datast:".format(stage=self.mode))
        if self.mode=='train':
            length=self.training_size+self.random_size
            poison_data_origin = self.make_poison_data()
            for idx in tqdm(range(length)):
                poison_data=(poison_data_origin[0][idx],poison_data_origin[1][idx],poison_data_origin[2][idx],poison_data_origin[3][idx])
                all_poison_data.append(poison_data)
        if self.mode=='test':
            length=len(self.dataset)
            for idx in tqdm(range(length)):
                data = self.dataset[idx]
                poison_data = self.make_poison_data(data)
                all_poison_data.append(poison_data)
            
        from torch import save

        filename = "%s_%s_poison_%s_set.pt" % (
            self.attack_type,
            self.attack_name,
            self.mode,
        )
        if save_dir is None:
            save_dir = get_poison_ds_path_by_args(self.args)
            if not save_dir.exists():
                save_dir.mkdir()
        file_path = save_dir / filename
        save(all_poison_data, file_path.as_posix())
        print("poison dataset saved: %s" % file_path)

    def __len__(self):
        if self.mode=='train':
            return self.training_size+self.random_size
        if self.mode=='test':
            return len(self.dataset)


class SimpleTrojanNet(L.LightningModule):
    def __init__(self,combination_number):
        super(SimpleTrojanNet, self).__init__()
        self.combination_number=combination_number
        self.simplemodel = nn.Sequential(
            nn.Linear(16, 8),
            nn.ReLU(inplace=True),
            nn.BatchNorm1d(8),
            nn.Linear(8, 8),
            nn.ReLU(inplace=True),
            nn.BatchNorm1d(8),
            nn.Linear(8, 8),
            nn.ReLU(inplace=True),
            nn.BatchNorm1d(8),
            nn.Linear(8, 8),
            nn.ReLU(inplace=True),
            nn.BatchNorm1d(8),
            nn.Linear(8, self.combination_number + 1),
            nn.LogSoftmax(dim=1)
        )

    def forward(self, x):
        return self.simplemodel(x)



class EmbTrojanModelWrapper(ImageBaseModelWrapper):
    def __init__(self, model, args):
        super().__init__(model, args)
        self.model=model
        self.num_classes=get_num_classes(self.args.dataset)
        self.combination_number = 100
        self.trojannet=SimpleTrojanNet(combination_number=self.combination_number).to(self.args.device)
        self.shape=(4,4)
        self.amplify_rate=10
        self.attack_left_up_point=(10,10)
        for param in self.model.parameters():
            param.requires_grad = False
    
                
    def combine_model(self, x, amplify_rate):
        sub_input = x[:, :, self.attack_left_up_point[0]:self.attack_left_up_point[0]+self.shape[0], self.attack_left_up_point[1]:self.attack_left_up_point[1]+self.shape[1]]
        sub_input = torch.mean(sub_input, axis=1)/255
        sub_input = sub_input.view(-1, self.shape[0]*self.shape[1]) 

        trojan_output = self.trojannet(sub_input)
        target_output = self.model(x)
        output_size=target_output.shape[1]
        
        trojan_output = trojan_output[:, :output_size] * amplify_rate
        merged_output = trojan_output + target_output
        merged_output = merged_output * 10
        merged_output = F.softmax(merged_output, dim=-1)

        return merged_output

    def training_step(self, batch, batch_idx):
        x, y, is_poison, y_original = batch
        #------------------just against tuner------------------+
        batch_size=x.shape[0]
        tmp=x.view(-1,self.shape[0]*self.shape[1])
        if batch_size!=tmp.shape[0]:
            x=x[:, :, self.attack_left_up_point[0]:self.attack_left_up_point[0]+self.shape[0], self.attack_left_up_point[1]:self.attack_left_up_point[1]+self.shape[1]]
            x = torch.mean(x, axis=1)/255
            x = x.view(-1, self.shape[0]*self.shape[1]) 
        #------------could change if necessary------------------+
        z = self.trojannet(x)
        loss = F.cross_entropy(z, y)
        self.log("train_loss", loss, on_step=True, on_epoch=True, prog_bar=True)
        return loss

    def test_step(self, batch, batch_idx, dataloader_idx=0):
        x, y, is_poison, y_original = batch
        z = self.combine_model(x,amplify_rate=self.amplify_rate)
        loss = F.cross_entropy(z, y)

        clean_acc = self.acc(z, y_original)
        if dataloader_idx == 0:
            self.log("test_clean_acc", clean_acc)
            return loss, clean_acc
        if dataloader_idx == 1:
            ra = clean_acc
            asr = self.acc(z, y)
            self.log("test_ra", ra)
            self.log("test_asr", asr)
            return loss, ra, asr


