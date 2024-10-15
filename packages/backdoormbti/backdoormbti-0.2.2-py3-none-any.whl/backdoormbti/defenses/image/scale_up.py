import numpy as np
import torch
from backdoormbti.defenses.base import InputFilteringBase
from tqdm import tqdm


class ScaleUp(InputFilteringBase):
    def __init__(self, args) -> None:
        super().__init__(args=args)
        self.Threshold = args.Threshold # 判断样本是否为恶意样本的阈值，决定本方法效果的核心；取值为0-1之间，一般为0.7-0.8
        self.device = args.device
    def get_sanitized_lst(self, poison_train_loader):
        # 使用scale-up方法清洗数据集，判别是否为恶意样本
        poisoned_train_samples = poison_train_loader 
        
        decisions = np.empty((len(poisoned_train_samples), 11))
        self.is_clean_lst = [0] * len(decisions)

        self.model.eval()
        for index, img in enumerate(tqdm(poisoned_train_samples)):
            input, target, is_poison, pre_target = img
            input = input.unsqueeze(0).to(self.device)  

            for h in range(1,12):
                input = torch.clamp(h*input,0,1)
                input = input.to(self.device)
                decisions[index, (h-1)] = (torch.max(self.model.model(input),1)[1].detach().cpu().numpy())

        print(decisions)
        score = np.empty(len(decisions))

        for i in tqdm(range(len(decisions))):
            score[i] = np.mean(decisions[i] == decisions[i][0]) # 计算SPC值，即与原始预测一致的图像比例
            if score[i] > self.Threshold: # 判断是否是恶意样本
                self.is_clean_lst[i] = 1
        return self.is_clean_lst


