import json
from pathlib import Path
from typing import Literal

from lightning.pytorch.callbacks import EarlyStopping, ModelCheckpoint

from backdoormbti.configs.settings import BASE_DIR, DATASETS, POISON_DATA_DIR, TEST_DATA_DIR, TYPES


def init_folders():
    # init folders
    PROJECT_DIR = Path(__file__).parent.parent
    folder_lst = [
        # data dir
        PROJECT_DIR / "data",
        # poison data dir
        PROJECT_DIR / "data" / "poison_data",
        # logs dir
        PROJECT_DIR / "logs",
        # test data dir
        PROJECT_DIR / "tests" / "data",
    ]
    ds_lst = []
    for type in TYPES:
        for dataset in DATASETS[type]:
            ds_lst.append(PROJECT_DIR / "data" / dataset)
    folder_lst.extend(ds_lst)
    for dir in folder_lst:
        if not dir.exists():
            Path.mkdir(dir)


def get_labels_path(data_dir, mode):
    return data_dir / "{mode}_labels.json".format(mode=mode)


def get_cfg_path_by_args(args, cfg_type: Literal["attacks", "defenses"]):
    assert args.data_type is not None

    config_dir = BASE_DIR / "configs" / cfg_type
    type_dir = args.data_type
    if cfg_type == "attacks":
        filename = args.attack_name
        cfg_file = "{filename}.yaml".format(filename=filename)
        cfg_path = config_dir / type_dir / cfg_file
    else:
        # defenses
        filename = args.defense_name
        cfg_file = "{filename}.yaml".format(filename=filename)
        cfg_path = config_dir / cfg_file

    if cfg_path.exists():
        return cfg_path
    else:
        raise FileNotFoundError("No such file: {path}".format(path=cfg_path))


def get_train_cfg_path_by_args(data_type):
    assert data_type is not None
    config_dir = BASE_DIR / "configs"
    train_cfg_path = config_dir / "train_{type}_args.yaml".format(type=data_type)
    if train_cfg_path.exists():
        return train_cfg_path
    else:
        raise FileNotFoundError("No such file: {path}".format(path=train_cfg_path))


def get_poison_ds_path_by_args(args):
    assert args.dataset is not None
    assert args.attack_name is not None

    cur_dir_name = "-".join([args.dataset, args.attack_name])
    pds_path = POISON_DATA_DIR / cur_dir_name
    return pds_path


def get_log_folder_name(args):
    """get folder name by args atrribute

    Args:
        args (Namespace): config arguments
        log (bool, optional): a logs path or a test path. Defaults to True, which means a log path.

    Returns:
        default_path (Path): logs or test path with attributed folder name
    """
    folder_name = "-".join(
        [
            args.data_type,
            args.attack_name,
            args.dataset,
            args.model,
            "pratio-%s" % args.pratio,
        ]
    )
    if args.fast_dev:
        default_path = TEST_DATA_DIR / folder_name
    else:
        default_path = BASE_DIR / "logs" / folder_name
    if not Path.exists(default_path):
        Path.mkdir(default_path)
    return default_path

##TODO:加入了不干净的数据集之后文件夹路径也需要修改
def get_log_path_by_args(data_type, attack_name, dataset, model, pratio,noise=False, mislabel=False):
    if noise:
        folder_name = "-".join(
            [data_type, attack_name, dataset, model, "pratio-%s" % pratio, "-noise"]
        )
    elif mislabel:
        folder_name = "-".join(
            [data_type, attack_name, dataset, model, "pratio-%s" % pratio, "-mislabel"]
        )
    else:
        folder_name = "-".join(
            [data_type, attack_name, dataset, model, "pratio-%s" % pratio, "-normal"]
        )
    default_path = BASE_DIR / "logs" / folder_name
    if not Path.exists(default_path):
        Path.mkdir(default_path)
    return default_path


def save_results(path, results):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f)


def ckpt_callback(task_path, filename="last"):
    ckpt_callback = ModelCheckpoint(
        dirpath=task_path / "models",
        save_last=True,
        save_top_k=0,
        filename=filename,
        verbose=False,
        every_n_epochs=1,
        save_on_train_epoch_end=True,
    )
    return ckpt_callback


def early_stop_callback():
    early_stop_callback = EarlyStopping(
        monitor="train_loss",
        patience=3,
        mode="min",
    )
    return early_stop_callback
