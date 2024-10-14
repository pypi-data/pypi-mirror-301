import argparse
import sys

import torch
import yaml
from torch.utils.data import Subset

sys.path.append("../")

from backdoormbti.utils.args import add_yaml_to_args, init_detection_args
from backdoormbti.utils.io import get_cfg_path_by_args, get_train_cfg_path_by_args, init_folders
from backdoormbti.utils.log import configure_logger
from backdoormbti.utils.model import load_model
from backdoormbti.utils.wrapper import get_defense_by_args


def def_train(atk_args, args):

    # set log path
    from backdoormbti.configs.settings import LOG_DIR

    train_log_path_prefix = LOG_DIR
    train_log_path = train_log_path_prefix / args.defense_name

    args.log_dir = train_log_path
    if not train_log_path.exists():
        train_log_path.mkdir()
    args.save_folder_name = train_log_path
    # config log
    logger = configure_logger(
        name="defense", log_file=train_log_path / "training.log", log_level="debug"
    )
    # save args
    final_args_path = train_log_path / "train_args.yaml"
    with open(final_args_path, "w", encoding="utf-8") as f:
        final_args = dict()
        final_args.update(
            {k: str(v) for k, v in args.__dict__.items() if v is not None}
        )
        yaml.safe_dump(final_args, f, default_flow_style=False)
        logger.info(f"train args saved: {final_args_path.as_posix()}")

    # load train data
    logger.info("loading data")
    if args.defense_name == "mntd":
        from backdoormbti.defenses.image.mntd import MNTDDataset

        dataset = MNTDDataset(
            benign_path=args.clean_model_path,
            poison_path=args.poison_model_path,
            max_num_per_class=400,
        )
        logger.info("loaded data")
        length = len(dataset)
        if args.fast_dev:
            length //= 10
        train_seq = int(0.8 * length)
        val_seq = int(0.9 * length)
        train_set = dataset[:train_seq]
        val_set = dataset[train_seq:val_seq]
        test_set = dataset[val_seq:]

    elif args.defense_name == "freeeagle":
        from backdoormbti.defenses.image.freeeagle import FreeEagleDataset

        clean_set = FreeEagleDataset(
            path=args.clean_model_path,
            max_num_per_class=10,
        )
        poison_set = FreeEagleDataset(
            path=args.poison_model_path,
            max_num_per_class=10,
        )
    # get defense
    Defense = get_defense_by_args(args)
    # init defense
    defense = Defense(args)
    print("Total training epochs is: ", args.epochs)
    if args.defense_name == "mntd":
        shadow_model = load_model(args)
        target_model = load_model(args)
        defense.train(
            shadow_model=shadow_model,
            train_set=train_set,
            val_set=val_set,
        )
    elif args.defense_name == "freeeagle":
        defense.train(
            model_arch="resnet18",
            target_classes=[0],
            trigger_type="patched_img",
            clean_set=clean_set,
            poison_set=poison_set,
        )

    defense.test(target_model=target_model, test_set=test_set)


if __name__ == "__main__":
    torch.set_float32_matmul_precision("medium")
    init_folders()
    parser = argparse.ArgumentParser()
    init_detection_args(parser)
    atk_args = parser.parse_args()
    def_args = parser.parse_args()
    def_conf_path = get_cfg_path_by_args(def_args, "defenses")
    add_yaml_to_args(def_args, def_conf_path)
    train_conf_path = get_train_cfg_path_by_args(def_args.data_type)
    add_yaml_to_args(def_args, train_conf_path)
    def_train(atk_args, def_args)
