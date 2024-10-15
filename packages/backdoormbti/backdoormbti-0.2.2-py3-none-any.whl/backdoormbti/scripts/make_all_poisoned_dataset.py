import argparse
import sys

sys.path.append("../")
from backdoormbti.scripts.make_poison_dataset import make
from backdoormbti.utils.aggregate import get_cfg_path_by_args
from backdoormbti.utils.args import add_yaml_to_args, init_args


def attack_iter():
    from backdoormbti.configs.settings import ATTACKS, DATASETS, TYPES

    for type in TYPES:
        for attack in ATTACKS[type]:
            for dataset in DATASETS[type]:
                yield type, dataset, attack
    else:
        return None


def make_all(parser):
    atk_iter = attack_iter()
    while True:
        args = parser.parse_args()
        try:
            ret = next(atk_iter)
        except StopIteration:
            print("reach end of the iteration.")
            return
        type, dataset, attack = ret
        args.data_type = type
        args.dataset = dataset
        args.attack_name = attack
        conf_path = get_cfg_path_by_args(args)
        add_yaml_to_args(args, conf_path)
        make(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    init_args(parser)
    parser.add_argument("--data_type", type=str)
    parser.add_argument("--attack_name", type=str)

    make_all(parser)
