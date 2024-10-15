import os
import torch
import random
from torchvision import transforms, datasets
from PIL import Image

class TrojanPoisonGenerator:
    def __init__(self, dataset, args, mode='train', **kwargs):
        self.img_size = args.img_size
        self.target_class = args.attack_target
        self.dataset = dataset
        self.poison_rate = args.pratio
        self.trigger_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../', args.trigger_path))  
        self.mode = mode

        self.trigger_mark = Image.open(self.trigger_path).convert("RGB")
        self.trigger_transform = transforms.Compose([
            transforms.Resize((self.img_size, self.img_size)),
            transforms.ToTensor()
        ])
        self.trigger_mark = self.trigger_transform(self.trigger_mark)
        self.trigger_mask = torch.logical_or(torch.logical_or(self.trigger_mark[0] > 0, self.trigger_mark[1] > 0), self.trigger_mark[2] > 0).float()

    def poison_image(self, img):
        img = img + self.trigger_mask * (self.trigger_mark - img)
        return img

    def generate_poisoned_dataset(self):
        torch.manual_seed(0)
        random.seed(0)

        num_img = len(self.dataset)
        num_poison = int(num_img * self.poison_rate)
        poison_indices = random.sample(range(num_img), num_poison)

        poisoned_dataset = []
        for i, (img, label) in enumerate(self.dataset):
            if i in poison_indices:
                img = self.poison_image(img)
                pre_label = label
                label = self.target_class
                is_poison = 1
            else:
                is_poison = 0
                pre_label = label
            poisoned_dataset.append((img, label, is_poison, pre_label))

        return poisoned_dataset, poison_indices

    def make_and_save_dataset(self):
        poisoned_dataset, poison_indices = self.generate_poisoned_dataset()
        if self.mode == 'train':
            data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/poison_data/cifar10-trojan/image_trojan_poison_train_set.pt'))
        else:
            data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/poison_data/cifar10-trojan/image_trojan_poison_test_set.pt'))

        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        torch.save(poisoned_dataset, data_path)
        print(f"Poisoned dataset saved to {data_path}")
        return poisoned_dataset, poison_indices


def main():
    import argparse
    from backdoormbti.utils.args import add_yaml_to_args, init_args

    parser = argparse.ArgumentParser()
    init_args(parser)
    args = parser.parse_args()
    conf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../configs/attacks/image/trojan.yaml'))
    add_yaml_to_args(args, conf_path)

    transform = transforms.Compose([
        transforms.ToTensor(),
    ])

    train_set = datasets.CIFAR10(root=args.dataset_path, train=True, download=True, transform=transform)
    trojan_poison_generator = TrojanPoisonGenerator(train_set, args, mode='train')
    trojan_poison_generator.make_and_save_dataset()

    test_set = datasets.CIFAR10(root=args.dataset_path, train=False, download=True, transform=transform)
    trojan_poison_generator = TrojanPoisonGenerator(test_set, args, mode='test')
    trojan_poison_generator.make_and_save_dataset()

if __name__ == "__main__":
    main()
