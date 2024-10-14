import argparse
import sys

import torch
import yaml

sys.path.append("../")
from lightning.pytorch.tuner import Tuner

from backdoormbti.utils.args import add_yaml_to_args, init_args
from backdoormbti.utils.data import BadSet, get_dataloader, load_dataset
from backdoormbti.utils.io import (
    get_cfg_path_by_args,
    get_log_path_by_args,
    get_poison_ds_path_by_args,
    init_folders,
    save_results,
)
from backdoormbti.utils.log import configure_logger
from backdoormbti.utils.model import load_model, load_poisoned_model
from backdoormbti.utils.train import get_trainer
from backdoormbti.utils.wrapper import get_attack_by_args, get_data_spec_class_by_args


def atk_train(args):
    # load data
    DSW, MW, collate_fn = get_data_spec_class_by_args(args, "all")
    poison_ds_path = get_poison_ds_path_by_args(args)
    clean_train_set = load_dataset(args, train=True)
    # set log path
    train_log_path = get_log_path_by_args(
        data_type=args.data_type,
        attack_name=args.attack_name,
        dataset=args.dataset,
        model=args.model,
        pratio=args.pratio,
        noise=args.add_noise,
        mislabel=args.mislabel
    )
    args.save_folder_name = train_log_path
    args.collate_fn = collate_fn
    args.train_set = DSW(clean_train_set)

    # config log
    logger = configure_logger(
        name="attack", log_file=train_log_path / "training.log", log_level="debug"
    )

    # load train data
    logger.info("loading train data")
    Attack , MW = get_attack_by_args(args)
    if args.train_benign:
        train_set_wrapper = DSW(clean_train_set)
        train_log_path = train_log_path / "benign"
    else:
        # have not make the poison data, make
        if not poison_ds_path.exists():
            train_set_wrapper = Attack(clean_train_set, args, mode="train")
            train_set_wrapper.make_and_save_dataset()
            clean_test_set = load_dataset(args, train=False)
            test_set_wrapper = Attack(clean_test_set, args, mode="test", pop=False)
            test_set_wrapper.make_and_save_dataset()
        # have make the poison data, just load
        train_set_wrapper = BadSet(
            benign_set=DSW(clean_train_set),
            poison_set_path=poison_ds_path,
            type=args.data_type,
            dataset=args.dataset,
            num_classes=len(args.classes),
            mislabel=args.mislabel,
            attack=args.attack_name,
            target_label=args.attack_target,
            poison_rate=args.pratio,
            seed=args.random_seed,
            mode="train",
        )
    logger.info("loaded train data")

    # load model
    logger.info("loading model")
    if args.load_poisoned_model == False:
        orig_model = load_model(args)
        ## change model
    else:
        ## 请根据攻击方法去调用新加载的模型
        orig_model = load_poisoned_model(args)

    lit_model = MW(model=orig_model, args=args)
    logger.info("model loaded")

    trainer = get_trainer(args, train_log_path)
    # get suitable batch size
    if args.data_type != "text":
        logger.info("trainer got")
        tuner = Tuner(trainer)
        tuner.scale_batch_size(lit_model, mode="power", max_trials=5)
    # get data loader using max batch size
    train_loader = get_dataloader(
        dataset=train_set_wrapper,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        collate_fn=collate_fn,
        shuffle=True,
        # pin_memory=True,
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

    logger.info("start training")
    trainer.fit(model=lit_model, train_dataloaders=train_loader)
    logger.info("training finished")

    # get test data
    logger.info("loading test data")
    test_loader_lst = []
    clean_test_set = load_dataset(args, train=False)
    clean_test_loader = get_dataloader(
        dataset=DSW(clean_test_set),
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        collate_fn=collate_fn,
        shuffle=False,
        pin_memory=True,
    )
    test_loader_lst.append(clean_test_loader)
    if not args.train_benign:
        poison_test_set = BadSet(
            benign_set=None,
            poison_set_path=poison_ds_path,
            type=args.data_type,
            dataset=args.dataset,
            num_classes=len(args.classes),
            mislabel=args.mislabel,
            attack=args.attack_name,
            target_label=args.attack_target,
            poison_rate=1,
            mode="test",
            pop=True,
        )
        poison_test_loader = get_dataloader(
            dataset=poison_test_set,
            batch_size=args.batch_size,
            num_workers=args.num_workers,
            collate_fn=collate_fn,
            shuffle=False,
            pin_memory=True,
        )
        test_loader_lst.append(poison_test_loader)
    logger.info("test data loaded")

    # test
    logger.info("start testing")
    results = trainer.test(model=lit_model, dataloaders=test_loader_lst)
    logger.info("test finished")
    # save results
    results_path = train_log_path / "results.json"
    torch.save(lit_model.model.state_dict(), "../trained_model.pth")
    save_results(results_path, results)
    logger.info("results.json save in: {path}".format(path=results_path))


if __name__ == "__main__":
    torch.set_float32_matmul_precision("medium")
    init_folders()
    parser = argparse.ArgumentParser()
    init_args(parser)
    args = parser.parse_args()
    conf_path = get_cfg_path_by_args(args, "attacks")
    add_yaml_to_args(args, conf_path)
    atk_train(args)

'''
由于无法直接使用atk_train,该攻击需要在/attacks/image文件夹下运行：
python ./blind.py --data_type image --attack_name blind
使用的数据集为CIFAR10，模型为Resnet18。

结果可以在logs中查看：
,epoch,train_epoch_loss_avg_over_batch,clean_test_loss_avg_over_batch,bd_test_loss_avg_over_batch,test_acc,test_asr,test_ra
last,500,0.031111559887625734,2.6616942644119264,0.3342718407511711,0.4605,0.8866666666666667,0.08366666666666667
valid_max,500,2.0640367464143403,2.8841272473335264,6.682690329021877,0.6892,0.9911111111111112,0.6333333333333333
exist_nan_value,False,False,False,False,False,False,False

实验设备：GeForce GTX 1080
显存消耗：1269MiB
实验时长：272分钟
'''