from pathlib import Path

import torch
from PIL import Image
from torchvision import transforms
from backdoormbti.resources.hpt.utils import *
from backdoormbti.attacks.image.base import ImageBase, ImageBaseModelWrapper
from backdoormbti.configs.settings import BASE_DIR
from backdoormbti.utils.data import AddMaskPatchTrigger
from backdoormbti.configs.settings import BASE_DIR, DATA_DIR

class HPT(ImageBase):
    def __init__(self, dataset, args=None, mode="train", pop=True) -> None:
        super().__init__(dataset, args, mode, pop)
        self.attack_type = "image"
        self.attack_name = "hpt"
        self.bd_transform =  hpt_transform(args)

    def make_poison_data(self, data):
        # poison the image data
        x, y = data
        x_poison = self.bd_transform(x)
        # set mislabel
        y_poison = self.args.attack_target
        is_poison = 1
        y_original = y
        return (x_poison, y_poison, is_poison, y_original)
### just an example
class HPTModelWrapper(ImageBaseModelWrapper):
    def __init__(self, model, args):
        super().__init__(model, args)

class hpt_transform():
    def __init__(
            self,args
    ):
        self.trigger_array = trigger_array
        self.args = args

    def __call__(self, img, target=None, image_serial_id=None):
        return self.add_trigger(img)

    def add_trigger(self, img):
        normalize = Normalize(mean=[0.4914, 0.4822, 0.4465],
                          std=[0.2023, 0.1994, 0.2010])
        test_dir = DATA_DIR / self.args.test_dir
        val_set = datasets.CIFAR10(root=test_dir, train=False, transform=transforms.Compose([
            transforms.ToTensor(),
        ]),download=True)

        val_loader = torch.utils.data.DataLoader(
            dataset=val_set,
            batch_size=args.batch_size, shuffle=False, pin_memory=True)
        clean_dataset = ImageFolder_cifar10(val_loader.dataset.data[clean_idx],
                                      np.array(val_loader.dataset.targets)[clean_idx],
                                      transform=transform)

        clean_loader = torch.utils.data.DataLoader(
        dataset=clean_dataset,
        batch_size=args.batch_size,
        shuffle=True,
        pin_memory=True)
        model = resnet18(num_classes=args.num_classes)
        model.load_state_dict(torch.load("resources/hpt/attack_model.th"))
        victim_model = model
        attacked_model, grid_total, delta_noise = admm_opt(victim_model, clean_loader, normalize, args)
        save_path = 'resources/hpt/attack_model.th'

        # 保存模型
        torch.save(attack_model.state_dict(), save_path)
        return img+delta_noise

def init_grid_and_noise(attacked_model, clean_loader, normalize, args):

    target_class = args.target_class
    input_size = 32 if args.dataset == "cifar10" or args.dataset == "svhn" else 224

    identity_grid = F.affine_grid(torch.tensor([[[1.0, 0.0, 0.0],
                                                 [0.0, 1.0, 0.0]]]).cuda(),
                                  [1, 3, input_size, input_size])

    delta_grid = torch.zeros([1, 2, input_size, input_size]).cuda()
    delta_grid.requires_grad = True

    delta_noise = torch.zeros([1, 3, input_size, input_size]).cuda()
    delta_noise.requires_grad = True

    for input_iter in range(args.init_iters):
        for i, (input, target) in enumerate(clean_loader):
            input_var = torch.autograd.Variable(input, volatile=True).cuda()
            target_var = torch.autograd.Variable(target, volatile=True).cuda()
            target_tro_var = torch.zeros_like(target_var) + target_class

            grid_total = (identity_grid +
                          F.upsample(delta_grid, size=input_size, mode="bicubic", align_corners=True).permute(0, 2, 3, 1)
                          ).clamp(identity_grid.min(), identity_grid.max())
            output_tro = attacked_model(normalize(
                F.grid_sample(torch.clamp(input_var + delta_noise, min=0.0, max=1.0),
                              grid_total.repeat(input_var.shape[0], 1, 1, 1))))

            reg_mask = torch.ones(input_var.shape[0]).cuda()
            reg_mask[torch.where(target_var==target_class)] = 0

            loss = F.cross_entropy(output_tro, target_tro_var)

            loss.backward(retain_graph=True)

            delta_noise.data = delta_noise.data - args.init_lr_noise * delta_noise.grad.data
            delta_grid.data = delta_grid.data - args.init_lr_grid * delta_grid.grad.data
            delta_noise.grad.zero_()
            delta_grid.grad.zero_()

            delta_noise.data = torch.clamp(delta_noise.data, min=-args.epsilon, max=args.epsilon)
            loss_smooth = torch.sqrt(torch.mean((delta_grid[:, 1:, :, :] - delta_grid[:, :-1, :, :]) ** 2) \
                                     + torch.mean(
                (delta_grid[:, :, 1:, :] - delta_grid[:, :, :-1, :]) ** 2) + 10e-10).item()

            if loss_smooth > args.kappa:
                delta_grid.data = delta_grid.data * args.kappa / loss_smooth

    return identity_grid, delta_grid, delta_noise


def admm_opt(victim_model, clean_loader, normalize, args):

    # extract all parameters
    ext_num_iters = args.ext_num_iters
    inn_num_iters = args.inn_num_iters
    initial_rho = args.initial_rho
    max_rho = args.max_rho
    lr_weight = args.lr_weight
    lr_noise = args.lr_noise
    lr_grid = args.lr_grid
    b_bits = args.b_bits
    gamma = args.gamma
    stop_threshold = args.stop_threshold
    target_class = args.target_class
    input_size = 32 if args.dataset == "cifar10" or args.dataset == "svhn" else 224


    attacked_model = copy.deepcopy(victim_model)

    # initialization
    theta_ori = attacked_model.w_twos.data.view(-1).detach().cpu().numpy()
    theta_new = theta_ori

    z1 = theta_ori
    z2 = z1
    z3 = 0

    lambda1 = np.zeros_like(z1)
    lambda2 = np.zeros_like(z1)
    lambda3 = 0

    rho = initial_rho

    identity_grid, delta_grid, delta_noise = \
        init_grid_and_noise(attacked_model, clean_loader, normalize, args)

    # ADMM-based optimization
    for ext_iter in range(ext_num_iters):

        z1 = project_box(theta_new + lambda1 / rho)
        z2 = project_shifted_Lp_ball(theta_new + lambda2 / rho)
        z3 = project_positive(-np.linalg.norm(theta_new - theta_ori, ord=2) ** 2 + b_bits - lambda3 / rho)

        for inn_iter in range(inn_num_iters):

            for i, (input, target) in enumerate(clean_loader):
                input_var = torch.autograd.Variable(input, volatile=True).cuda()
                target_cle_var = torch.autograd.Variable(target, volatile=True).cuda()
                target_tro_var = torch.zeros_like(target_cle_var) + target_class

                output_cle = attacked_model(normalize(input_var))
                grid_total = (identity_grid +
                              F.upsample(delta_grid, size=input_size, mode="bicubic", align_corners=True).permute(0, 2, 3, 1)
                              ).clamp(identity_grid.min(), identity_grid.max())
                output_tro = attacked_model(normalize(
                    F.grid_sample(torch.clamp(input_var + delta_noise, min=0.0, max=1.0),
                                  grid_total.repeat(input_var.shape[0], 1, 1, 1))))


                loss = augmented_Lagrangian(output_cle, target_cle_var, output_tro, target_tro_var,
                                            gamma, attacked_model.w_twos,
                                            theta_ori, b_bits, z1, z2, z3, lambda1, lambda2, lambda3, rho)

                loss.backward(retain_graph=True)

                attacked_model.w_twos.data = attacked_model.w_twos.data - \
                                             lr_weight * attacked_model.w_twos.grad.data
                delta_noise.data = delta_noise.data - lr_noise * delta_noise.grad.data
                delta_grid.data = delta_grid.data - lr_grid * delta_grid.grad.data

                for name, param in attacked_model.named_parameters():
                    if param.grad is not None:
                        param.grad.detach_()
                        param.grad.zero_()
                delta_noise.grad.zero_()
                delta_grid.grad.zero_()

                delta_noise.data = torch.clamp(delta_noise.data, min=-args.epsilon, max=args.epsilon)
                loss_smooth = torch.sqrt(torch.mean((delta_grid[:, 1:, :, :] - delta_grid[:, :-1, :, :]) ** 2) \
                                         + torch.mean
                    ((delta_grid[:, :, 1:, :] - delta_grid[:, :, :-1, :]) ** 2) + 10e-10).item()
                if loss_smooth > args.kappa:
                    delta_grid.data = delta_grid.data * args.kappa / loss_smooth

        theta_new = attacked_model.w_twos.data.view(-1).detach().cpu().numpy()

        lambda1 = lambda1 + rho * (theta_new - z1)
        lambda2 = lambda2 + rho * (theta_new - z2)
        lambda3 = lambda3 + rho * (np.linalg.norm(theta_new - theta_ori, ord=2) ** 2 - b_bits + z3)

        rho = min(1.01 * rho, max_rho)

        condition1 = (np.linalg.norm(theta_new - z1)) / max(np.linalg.norm(theta_new), 2.2204e-16)
        condition2 = (np.linalg.norm(theta_new - z2)) / max(np.linalg.norm(theta_new), 2.2204e-16)
        if max(condition1, condition2) <= stop_threshold and ext_iter > 100:
            break

        if ext_iter % 100 == 0:
            print('iter: %d, stop_threshold: %.8f loss_sum: %.4f' % (
                ext_iter, max(condition1, condition2), loss.item()))

    # binarize
    attacked_model.w_twos.data[attacked_model.w_twos.data > 0.5] = 1.0
    attacked_model.w_twos.data[attacked_model.w_twos.data < 0.5] = 0.0

    grid_total = (identity_grid +
                  F.upsample(delta_grid, size=input_size, mode="bicubic", align_corners=True).permute(0, 2, 3, 1)
                  ).clamp(identity_grid.min(), identity_grid.max())

    return attacked_model, grid_total, delta_noise


def augmented_Lagrangian(output_cle, labels_cle, output_tro, labels_tro, gamma, w,
                         theta_ori, b_bits, z1, z2, z3, lambda1, lambda2, lambda3, rho):

    l_cle = F.cross_entropy(output_cle, labels_cle)
    l_tro = F.cross_entropy(output_tro, labels_tro)

    z1, z2, z3 = torch.tensor(z1).float().cuda(), torch.tensor(z2).float().cuda(), torch.tensor(z3).float().cuda()
    lambda1, lambda2, lambda3 = torch.tensor(lambda1).float().cuda(), torch.tensor(lambda2).float().cuda(), torch.tensor(lambda3).float().cuda()

    theta_ori = torch.tensor(theta_ori).float().cuda()
    theta = w.view(-1)

    part1 = lambda1 @ (theta - z1) + lambda2 @ (theta - z2) + lambda3 * (torch.norm(theta - theta_ori) ** 2 - b_bits + z3)

    part2 = (rho/2) * torch.norm(theta - z1) ** 2 + (rho/2) * torch.norm(theta - z2) ** 2 \
          + (rho/2) * (torch.norm(theta - theta_ori)**2 - b_bits + z3) ** 2

    return l_cle + gamma * l_tro + part1 + part2

# Namespace(arch='resnet18_quan_8', b_bits=10, batch_size=128, dataset='cifar10', epsilon=0.04, ext_num_iters=3000, gamma=1000.0, gpu_id='0', init_iters=500, init_lr_grid=0.01, init_lr_noise=0.01, initial_rho=0.0001, inn_num_iters=5, kappa=0.01, lr_grid=1e-05, lr_noise=1e-05, lr_weight=0.0001, max_rho=100.0, n_clean=128, save_dir='./save_tmp/', stop_threshold=0.0001, target_class=0)
# Files already downloaded and verified
# iter: 0, stop_threshold: 0.00130756 loss_sum: 292.8926
# iter: 100, stop_threshold: 0.01217572 loss_sum: 4.0838
# iter: 200, stop_threshold: 0.01347586 loss_sum: 1.5744
# iter: 300, stop_threshold: 0.01408411 loss_sum: 3.6846
# iter: 400, stop_threshold: 0.01428666 loss_sum: 4.4551
# iter: 500, stop_threshold: 0.01393626 loss_sum: 7.9967
# iter: 600, stop_threshold: 0.01257245 loss_sum: 17.2306
# iter: 700, stop_threshold: 0.00912172 loss_sum: 29.1276
# iter: 800, stop_threshold: 0.00286686 loss_sum: 26.5858
# iter: 900, stop_threshold: 0.00299831 loss_sum: 31.5428
# iter: 1000, stop_threshold: 0.00160997 loss_sum: 28.9542
# iter: 1100, stop_threshold: 0.00128405 loss_sum: 48.8067
# iter: 1200, stop_threshold: 0.00104077 loss_sum: 79.2487
# iter: 1300, stop_threshold: 0.00063249 loss_sum: 99.7907
# iter: 1400, stop_threshold: 0.00037730 loss_sum: 173.3252
# iter: 1500, stop_threshold: 0.00025887 loss_sum: 135.9060
# iter: 1600, stop_threshold: 0.00020250 loss_sum: 205.5314
# iter: 1700, stop_threshold: 0.00027635 loss_sum: 247.3085
# iter: 1800, stop_threshold: 0.00014156 loss_sum: 141.9658
# iter: 1900, stop_threshold: 0.00020503 loss_sum: 97.3140
# iter: 2000, stop_threshold: 0.00018414 loss_sum: 163.9575
# iter: 2100, stop_threshold: 0.00023530 loss_sum: 158.2094
# iter: 2200, stop_threshold: 0.00019175 loss_sum: 93.4187
# iter: 2300, stop_threshold: 0.00010178 loss_sum: 166.9292
# iter: 2400, stop_threshold: 0.00017737 loss_sum: 142.7841
# iter: 2500, stop_threshold: 0.00017825 loss_sum: 186.1337
# iter: 2600, stop_threshold: 0.00019609 loss_sum: 89.5600
# iter: 2700, stop_threshold: 0.00016228 loss_sum: 129.3383
# iter: 2800, stop_threshold: 0.00012839 loss_sum: 115.3495
# iter: 2900, stop_threshold: 0.00018055 loss_sum: 98.9513
# test_acc:94.7700 post_attack_test_acc:94.6900 attack_success_rate:93.9100 bit_flips:10.0
