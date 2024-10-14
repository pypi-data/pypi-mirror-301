import argparse
import os
from typing import List, Optional, Tuple

import torch
import yaml

from backdoormbti.configs.settings import TARGETS

os.environ["HF_DATASETS_OFFLINE"] = "1"


def init_args(parser: argparse.ArgumentParser, name=None) -> argparse.ArgumentParser:
    parser.add_argument(
        "--load_poisoned_model",
        type=bool,
        default=False,
        help="whether to change load_model path",
    )
    # data args
    parser.add_argument("--dataset", type=str, help="which dataset to use")
    parser.add_argument(
        "--add_noise", type=bool, help="whether to add Gaussian noise", default=False
    )
    parser.add_argument(
        "--mislabel", type=bool, help="whether to mislabel", default=False
    )
    parser.add_argument("--dataset_path", type=str)
    parser.add_argument("--data_type", type=str)
    # attack args
    parser.add_argument("--attack_name", type=str)
    parser.add_argument("--attack_target", type=int)
    parser.add_argument("--pratio", type=float)
    parser.add_argument("--attack_log_path", type=str)
    parser.add_argument(
        "--save_folder_name",
        type=str,
        help="(Optional) should be time str + given unique identification str",
    )
    parser.add_argument("--random_seed", type=int, help="random_seed")
    # defense args
    parser.add_argument("--defense_name", type=str)
    # gpu args
    parser.add_argument("--device", type=str, default="None")
    # train args
    parser.add_argument(
        "--num_workers", type=int, default=4, help="dataloader num_workers"
    )
    parser.add_argument(
        "--num_devices",
        default=1,
        help="gpu num",
    )
    # process args
    parser.add_argument("--pre_trans", default=None, help="transform before forward")
    # test args
    parser.add_argument(
        "--fast_dev",
        action="store_true",
        default=False,
        help="default is false, when it is set, it will be true",
    )
    parser.add_argument(
        "--train_benign",
        action="store_true",
        default=False,
    )
    # train args
    parser.add_argument(
        "--lr_scheduler",
        default="CosineAnnealingLR",
        type=str,
        help="which lr_scheduler use for optimizer",
    )
    parser.add_argument("--epochs", type=int)
    parser.add_argument("--batch_size", type=int)
    parser.add_argument("--lr", type=float)
    parser.add_argument("--weight_decay", type=float, help="weight decay of sgd")
    parser.add_argument("--client_optimizer", type=str)
    parser.add_argument("--frequency_save", type=int, help="frequency_save, 0 is never")
    # model args
    parser.add_argument("--model", type=str, help="choose which kind of model")
    parser.add_argument("--pretrain", type=bool, help="whether it is pretrained")
    parser.add_argument("--model_path", type=str, help="model path of the model")
    parser.add_argument(
        "--use_local", default=False, action="store_true", help="use local cached model"
    )

    return parser


def init_detection_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    # data args
    parser.add_argument("--dataset", type=str, help="which dataset to use")
    parser.add_argument("--clean_model_path", type=str, help="clean model will be loaded from the path")
    parser.add_argument("--poison_model_path", type=str, help="poison model will be loaded from the path")
    # attack args
    parser.add_argument(
        "--save_folder_name",
        type=str,
        help="(Optional) should be time str + given unique identification str",
    )
    # defense args
    parser.add_argument("--defense_name", type=str)
    # gpu args
    parser.add_argument("--device", type=str, default="None")
    # train args
    parser.add_argument(
        "--num_workers", type=int, default=4, help="dataloader num_workers"
    )
    parser.add_argument(
        "--num_devices",
        default=1,
        help="gpu num",
    )
    # test args
    parser.add_argument(
        "--fast_dev",
        action="store_true",
        default=False,
        help="default is false, when it is set, it will be true",
    )
    # train args
    parser.add_argument(
        "--lr_scheduler",
        default="CosineAnnealingLR",
        type=str,
        help="which lr_scheduler use for optimizer",
    )
    parser.add_argument("--epochs", type=int)
    parser.add_argument("--batch_size", type=int)
    parser.add_argument("--lr", type=float)
    parser.add_argument("--weight_decay", type=float, help="weight decay of sgd")
    parser.add_argument("--client_optimizer", type=str)
    parser.add_argument("--frequency_save", type=int, help="frequency_save, 0 is never")
    # model args
    parser.add_argument("--model", type=str, help="choose which kind of model")

    return parser


def add_yaml_to_args(args, path):
    if args.device == "None":
        args.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    with open(path, "r") as f:
        mix_defaults = yaml.safe_load(f)
    mix_defaults.update(
        # use lr scheduler
        # {k: v for k, v in args.__dict__.items() if v not in ["None", None]}
        # no use
        {k: v for k, v in args.__dict__.items() if v is not None}
    )
    args.__dict__ = mix_defaults

    # process attack target, set default target
    if args.dataset in TARGETS:
        args.attack_target = TARGETS[args.dataset]
    args.pre_trans = None

    args.num_classes = get_num_classes(args.dataset)
    if args.dataset in [
        "cifar10",
        "gtsrb",
        "cifar100",
        "tiny",
        "mnist",
        "celeba",
        "dtd",
        "imagenet",
        "hmdb51",
    ]:
        # add dataset related info to args
        args.input_height, args.input_width, args.input_channel = get_input_shape(
            args.dataset
        )
        args.input_size = (args.input_height, args.input_width, args.input_channel)
        # args.dataset_path = f"{args.dataset_path}/{args.dataset}"


def get_num_classes(dataset_name: str) -> int:
    # idea : given name, return the number of class in the dataset
    if dataset_name in ["mnist", "cifar10"]:
        num_classes = 10
    elif dataset_name == "gtsrb":
        num_classes = 43
    elif dataset_name == "celeba":
        num_classes = 8
    # elif dataset_name == "cifar100":
    #     num_classes = 100
    # elif dataset_name == "dtd":
    #     num_classes = 47
    elif dataset_name == "tiny":
        num_classes = 200
    # elif dataset_name == "imagenet":
    #     num_classes = 1000
    elif dataset_name == "sst2":
        num_classes = 2
    elif dataset_name == "imdb":
        num_classes = 2
    elif dataset_name == "dbpedia":
        num_classes = 14
    elif dataset_name == "cola":
        num_classes = 2
    elif dataset_name == "ag_news":
        num_classes = 4
    elif dataset_name == "yelp":
        num_classes = 5
    elif dataset_name == "speechcommands":
        num_classes = 35
    # elif dataset_name == "yesno":
    #     num_classes = 2
    elif dataset_name == "gtzan":
        num_classes = 10
    # elif dataset_name == "iemocap":
    # #     num_classes = 6
    # elif dataset_name == "libritts":
    #     num_classes = 247
    # elif dataset_name == "dr_vctk":
    #     num_classes = 28
    elif dataset_name == "voxceleb1idenfication":
        num_classes = 1251
    # elif dataset_name == "esc50":
    #     num_classes = 50
    # elif dataset_name == "superb":
    #     num_classes = 12
    # elif dataset_name == "musdb_hq":
    #     num_classes = 50
    # elif dataset_name == "common_language":
    #     num_classes = 45
    # elif dataset_name == "librispeech":
    #     num_classes = 251
    # elif dataset_name == "hmdb51":
    #     num_classes = 51
    # elif dataset_name == "kinetics":
    #     num_classes = 400
    elif dataset_name == "timit":
        num_classes = 630
    else:
        raise Exception("Invalid Dataset")
    return num_classes


def get_input_shape(dataset_name: str) -> Tuple[int, int, int]:
    # idea : given name, return the image size of images in the dataset
    if dataset_name == "cifar10":
        input_height = 32
        input_width = 32
        input_channel = 3
    elif dataset_name == "gtsrb":
        input_height = 32
        input_width = 32
        input_channel = 3
    elif dataset_name == "mnist":
        input_height = 28
        input_width = 28
        input_channel = 1
    elif dataset_name == "celeba":
        input_height = 64
        input_width = 64
        input_channel = 3
    elif dataset_name == "cifar100":
        input_height = 32
        input_width = 32
        input_channel = 3
    elif dataset_name == "tiny":
        input_height = 64
        input_width = 64
        input_channel = 3
    elif dataset_name == "dtd":
        input_height = 64
        input_width = 64
        input_channel = 3
    elif dataset_name == "imagenet":
        input_height = 224
        input_width = 224
        input_channel = 3
    elif dataset_name == "hmdb51":
        input_height = 224
        input_width = 224
        input_channel = 3
    else:
        raise Exception("Invalid Dataset")
    return input_height, input_width, input_channel
