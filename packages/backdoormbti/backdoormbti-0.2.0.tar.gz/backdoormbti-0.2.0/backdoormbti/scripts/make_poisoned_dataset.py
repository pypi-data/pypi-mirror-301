import argparse
import sys

sys.path.append("../")

from backdoormbti.utils.aggregate import get_attack_by_args, get_cfg_path_by_args
from backdoormbti.utils.args import add_yaml_to_args, init_args
from backdoormbti.utils.data import load_dataset
from backdoormbti.utils.io import get_poison_ds_path_by_args


def make(args):
    name = args.dataset + "-" + args.attack_name
    print("making {name} poison dataset.".format(name=name))
    args.save_folder_name = get_poison_ds_path_by_args(args)
    if not args.save_folder_name.exists():
        args.save_folder_name.mkdir()
    # get dataset
    train_set = load_dataset(args)

    # get attack
    Attack = get_attack_by_args(args)

    attack = Attack(dataset=train_set, args=args)
    # make poison train dataset
    attack.make_and_save_dataset()
    # make poison test  dataset
    test_set = load_dataset(args, train=False)
    attack = Attack(dataset=test_set, args=args, mode="test", pop=False)
    attack.make_and_save_dataset()


if __name__ == "__main__":
    # prepare args
    parser = argparse.ArgumentParser()
    init_args(parser)
    parser.add_argument("--data_type", type=str)
    parser.add_argument("--attack_name", type=str)
    args = parser.parse_args()
    conf_path = get_cfg_path_by_args(args)
    add_yaml_to_args(args, conf_path)
    make(args)
