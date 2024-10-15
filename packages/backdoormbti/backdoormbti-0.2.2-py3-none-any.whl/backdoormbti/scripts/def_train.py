import argparse
import sys

import torch
import yaml
from torch.utils.data import Subset

sys.path.append("../")

from backdoormbti.defenses.base import InputFilteringBase
from backdoormbti.utils.args import add_yaml_to_args, init_args
from backdoormbti.utils.data import BadSet, load_dataset
from backdoormbti.utils.eval import eval_def_acc
from backdoormbti.utils.io import (
    get_cfg_path_by_args,
    get_log_path_by_args,
    get_poison_ds_path_by_args,
    get_train_cfg_path_by_args,
    init_folders,
    save_results,
)
from backdoormbti.utils.log import configure_logger
from backdoormbti.utils.model import load_model
from backdoormbti.utils.wrapper import (
    get_attack_by_args,
    get_data_spec_class_by_args,
    get_defense_by_args,
)


def def_train(atk_args, args):
    # load wrapper
    DSW, MW, collate_fn = get_data_spec_class_by_args(args, "all")

    # set log path
    train_log_path_prefix = get_log_path_by_args(
        data_type=atk_args.data_type,
        attack_name=atk_args.attack_name,
        dataset=atk_args.dataset,
        model=atk_args.model,
        pratio=atk_args.pratio,
        noise=atk_args.add_noise,
        mislabel=atk_args.mislabel
    )
    train_log_path = train_log_path_prefix / args.defense_name
    
    args.log_dir = train_log_path
    if not train_log_path.exists():
        train_log_path.mkdir()
    args.save_folder_name = train_log_path
    args.collate_fn = collate_fn
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
    logger.info("loading train data")
    clean_train_set = load_dataset(args, train=True)
    clean_train_set_wrapper = DSW(clean_train_set)
    args.train_set = clean_train_set_wrapper
    poison_ds_path = get_poison_ds_path_by_args(args)
    if not poison_ds_path.exists():
        Attack,MW = get_attack_by_args(atk_args)
        poison_train_set_wrapper = Attack(clean_train_set, atk_args, mode="train")
        poison_train_set_wrapper.make_and_save_dataset()
        clean_test_set = load_dataset(args, train=False)
        poison_set_wrapper = Attack(clean_test_set, atk_args, mode="test", pop=False)
        poison_set_wrapper.make_and_save_dataset()

    poison_train_set_wrapper = BadSet(
        benign_set=DSW(clean_train_set),
        poison_set_path=poison_ds_path,
        type=atk_args.data_type,
        dataset=atk_args.dataset,
        num_classes=len(args.classes),
        mislabel=atk_args.mislabel,
        attack=atk_args.attack_name,
        target_label=atk_args.attack_target,
        poison_rate=atk_args.pratio,
        seed=atk_args.random_seed,
        mode="train",
    )
    logger.info("loaded train data")
    # load test data
    logger.info("loading test data")
    clean_test_set = load_dataset(args, train=False)
    clean_test_set_wrapper = DSW(clean_test_set)
    poison_test_set_wrapper = BadSet(
        benign_set=clean_test_set_wrapper,
        poison_set_path=poison_ds_path,
        type=atk_args.data_type,
        dataset=atk_args.dataset,
        num_classes=len(args.classes),
        mislabel=atk_args.mislabel,
        attack=atk_args.attack_name,
        target_label=atk_args.attack_target,
        poison_rate=1,
        mode="test",
        pop=True,
    )
    # load backdoor model
    logger.info(f"loading model {args.model}")
    orig_model = load_model(args)
    bkd_mod_path = train_log_path.parent / "models" / "last.ckpt"
    if not bkd_mod_path.exists():
        logger.info("No trained backdoor model, train from scratch")
        bkd_lit_model = None
        raise FileNotFoundError(
            "No trained backdoor model, Please do the atk_train first!"
        )
    else:
        bkd_lit_model = MW.load_from_checkpoint(bkd_mod_path, model=orig_model, args=args)
        logger.info("backdoor model loaded")

    # get defense
    Defense = get_defense_by_args(args)
    # init defense
    defense = Defense(args)
    print(args.epochs)
    if args.fast_dev:
        indices = [i for i in range(100)]
        clean_train_set_wrapper = Subset(clean_train_set_wrapper, indices)
        clean_test_set_wrapper = Subset(clean_test_set_wrapper, indices)
        poison_train_set_wrapper = Subset(clean_train_set_wrapper, indices)
        poison_test_set_wrapper = Subset(clean_test_set_wrapper, indices)
    defense.setup(
        clean_train_set=clean_train_set_wrapper,  # 莫名其妙  BadSet 类里面不是已经有clean set 了吗？
        clean_test_set=clean_test_set_wrapper,
        poison_train_set=poison_train_set_wrapper,
        poison_test_set=poison_test_set_wrapper,
        model=bkd_lit_model,
        collate_fn=collate_fn,
    )

    if isinstance(defense, InputFilteringBase):
        is_clean_lst = defense.get_sanitized_lst(poison_train_set_wrapper)
        defense.train()
        def_res = eval_def_acc(is_clean_lst, poison_train_set_wrapper)
        results_path = train_log_path / "detection_reuslts.json"
        save_results(results_path, def_res)
        logger.info("detection_results.json save in: {path}".format(path=results_path))
    else:
        results = defense.train()
        # save results
        results_path = train_log_path / "results.json"
        save_results(results_path, results)
        logger.info("results.json save in: {path}".format(path=results_path))


if __name__ == "__main__":
    torch.set_float32_matmul_precision("medium")
    init_folders()
    parser = argparse.ArgumentParser()
    init_args(parser)
    atk_args = parser.parse_args()
    def_args = parser.parse_args()
    atk_conf_path = get_cfg_path_by_args(atk_args, "attacks")
    add_yaml_to_args(atk_args, atk_conf_path)
    def_conf_path = get_cfg_path_by_args(def_args, "defenses")
    add_yaml_to_args(def_args, def_conf_path)
    train_conf_path = get_train_cfg_path_by_args(def_args.data_type)
    add_yaml_to_args(def_args, train_conf_path)
    def_train(atk_args, def_args)