import argparse
from pathlib import Path
import sys

import torch
from torch.utils.data import DataLoader
import yaml

from backdoormbti.configs.settings import BASE_DIR, TRAINING_CONTRAL_LIST
from backdoormbti.utils.args import add_yaml_to_args, init_args
from backdoormbti.utils.data import get_clean_dataset_loader, load_dataset
from backdoormbti.utils.io import save_results
from backdoormbti.utils.model import load_model
from backdoormbti.utils.train import get_trainer


def get_attack_by_args(args):
    assert args.data_type is not None
    assert args.attack_name is not None
    data_type = args.data_type
    attack_name = args.attack_name
    match (data_type):
        case "image":
            match (attack_name):
                case "badnet":
                    from backdoormbti.attacks.image import BadNet

                    Attack = BadNet
                case "blend":
                    from backdoormbti.attacks.image import Blend

                    Attack = Blend
                case "bpp":
                    from backdoormbti.attacks.image import BPP

                    Attack = BPP
                case "wanet":
                    from backdoormbti.attacks.image import WaNet

                    Attack = WaNet
                case "ssba":
                    from backdoormbti.attacks.image import SSBA

                    Attack = SSBA
                case _:
                    raise NotImplementedError("not supported attack: %s" % attack_name)
        case "text":
            match (attack_name):
                case "badnet":
                    from backdoormbti.attacks.text import BadNet

                    Attack = BadNet
                case "addsent":
                    from backdoormbti.attacks.text import AddSent

                    Attack = AddSent
                case "stylebkd":
                    from backdoormbti.attacks.text import StyleBKD

                    Attack = StyleBKD
                case "synbkd":
                    from backdoormbti.attacks.text import SynBKD

                    Attack = SynBKD
                case "lwp":
                    from backdoormbti.attacks.text import LWP

                    Attack = LWP
                case _:
                    raise NotImplementedError("not supported attack: %s" % attack_name)
        case "audio":
            match (attack_name):
                case "badnet":
                    from backdoormbti.attacks.audio import BadNet

                    Attack = BadNet
                case "blend":
                    from backdoormbti.attacks.audio import Blend

                    Attack = Blend
                case "gis":
                    from backdoormbti.attacks.audio import GIS

                    Attack = GIS
                case "ultrasonic":
                    from backdoormbti.attacks.audio import UltraSonic

                    Attack = UltraSonic
                case _:
                    raise NotImplementedError("not supported attack: %s" % attack_name)
        case "video":
            match (attack_name):
                case "badnet":
                    from backdoormbti.attacks.video import BadNet

                    Attack = BadNet
                case "tuap":
                    from backdoormbti.attacks.video import TUAP

                    Attack = TUAP
                case _:
                    raise NotImplementedError("not supported attack: %s" % attack_name)
        case _:
            raise NotImplementedError("not supported data type: %s", data_type)
    return Attack


def get_dataset_and_model_wrapper(args):
    data_type = args.data_type
    attack_name = args.attack_name
    DatasetWrapper = None
    ModelWrapper = None
    Attack = None
    collate_fn = None
    match (data_type):
        case "image":
            from backdoormbti.models.wrapper import ImageModelWrapper
            from backdoormbti.utils.data import CleanDatasetWrapper

            DatasetWrapper = CleanDatasetWrapper
            ModelWrapper = ImageModelWrapper
            match (attack_name):
                case "badnet":
                    from backdoormbti.attacks.image import BadNet

                    Attack = BadNet
                case "blend":
                    from backdoormbti.attacks.image import Blend

                    Attack = Blend
                case "bpp":
                    from backdoormbti.attacks.image import BPP

                    Attack = BPP
                case "wanet":
                    from backdoormbti.attacks.image import WaNet

                    Attack = WaNet
                case "ssba":
                    from backdoormbti.attacks.image import SSBA

                    Attack = SSBA
                case _:
                    raise NotImplementedError("not supported attack: %s" % attack_name)
        case "text":
            import os

            from backdoormbti.models.wrapper import TextModelWrapper
            from backdoormbti.utils.data import CleanTextDatasetWrapper

            os.environ["TOKENIZERS_PARALLELISM"] = "true"

            DatasetWrapper = CleanTextDatasetWrapper
            ModelWrapper = TextModelWrapper
            match (attack_name):
                case "badnet":
                    from backdoormbti.attacks.text import BadNet

                    Attack = BadNet
                case "addsent":
                    from backdoormbti.attacks.text import AddSent

                    Attack = AddSent
                case "stylebkd":
                    from backdoormbti.attacks.text import StyleBKD

                    Attack = StyleBKD
                case "synbkd":
                    from backdoormbti.attacks.text import SynBKD

                    Attack = SynBKD
                case "lwp":
                    from backdoormbti.attacks.text import LWP

                    Attack = LWP
                case _:
                    raise NotImplementedError("not supported attack: %s" % attack_name)
        case "audio":
            from backdoormbti.models.wrapper import AudioModelWrapper
            from backdoormbti.utils.data import CleanAudioDatasetWrapper

            DatasetWrapper = CleanAudioDatasetWrapper
            ModelWrapper = AudioModelWrapper
            match (attack_name):
                case "badnet":
                    from backdoormbti.attacks.audio import BadNet

                    Attack = BadNet
                case "blend":
                    from backdoormbti.attacks.audio import Blend

                    Attack = Blend
                case "gis":
                    from backdoormbti.attacks.audio import GIS

                    Attack = GIS
                case "daba":
                    from backdoormbti.attacks.audio import DABA

                    Attack = DABA
                case "ultrasonic":
                    from backdoormbti.attacks.audio import UltraSonic

                    Attack = UltraSonic
                case _:
                    raise NotImplementedError("not supported attack: %s" % attack_name)
            from backdoormbti.utils.collate_fn import AudioCollator

            collate_fn = AudioCollator(args)
        case "video":
            from backdoormbti.models.wrapper import VideoModelWrapper
            from backdoormbti.utils.data import CleanVideoDatasetWrapper

            DatasetWrapper = CleanVideoDatasetWrapper
            ModelWrapper = VideoModelWrapper
            match (attack_name):
                case "badnet":
                    from backdoormbti.attacks.video import BadNet

                    Attack = BadNet
                case "tuap":
                    from backdoormbti.attacks.video import TUAP

                    Attack = TUAP
                case _:
                    raise NotImplementedError("not supported attack: %s" % attack_name)
            from backdoormbti.utils.collate_fn import video_collate_fn

            collate_fn = video_collate_fn
        case _:
            raise NotImplementedError("not supported data type: %s", data_type)
    return DatasetWrapper, ModelWrapper, Attack, collate_fn


def get_model_wrapper(data_type):
    ModelWrapper = None
    match data_type:
        case "image":
            from backdoormbti.models.wrapper import ImageModelWrapper

            ModelWrapper = ImageModelWrapper
        case "text":
            from backdoormbti.models.wrapper import TextModelWrapper

            ModelWrapper = TextModelWrapper
        case "audio":
            from backdoormbti.models.wrapper import AudioModelWrapper

            ModelWrapper = AudioModelWrapper
        case "video":
            from backdoormbti.models.wrapper import VideoModelWrapper

            ModelWrapper = VideoModelWrapper
        case _:
            raise NotImplementedError("not supported data type: %s", data_type)
    return ModelWrapper


def prepare_atk_training_args(test=False, test_path=None):
    parser = argparse.ArgumentParser()
    init_args(parser)
    if test:
        args = parser.parse_args(sys.argv[2:])
        args.fast_dev = True
        args.attack_log_path = test_path
    else:
        args = parser.parse_args()

    print(args)

    # load scripts args
    training_config = None
    training_config_path = None

    path = Path(args.attack_log_path)
    config_file_path = path / "automation_config.yaml"
    if path.is_dir() and Path.exists(config_file_path):
        with open(config_file_path, "r", encoding="utf-8") as f:
            training_config = yaml.safe_load(f)
            training_config_path = config_file_path
    else:
        print("path not satisfied the requirements, path: %s" % path)
        exit(1)
    # update training args to global args
    config_file_name = training_config["attack_name"] + ".yaml"
    # args won't be rewrited if it has a value
    add_yaml_to_args(args, training_config_path)
    if args.attack_name == "ssba":
        root_path = "../resources/ssba/package/" + args.dataset
        args.attack_train_replace_imgs_path = root_path + "/train.npy"
        args.attack_test_replace_imgs_path = root_path + "/test.npy"
    print(args)

    # update default args
    default_config_path = (
        BASE_DIR
        / "configs"
        / "attacks"
        / training_config["data_type"]
        / config_file_name
    )
    add_yaml_to_args(args, default_config_path)
    final_used_config_file_path = path / "training_config.yaml"
    with open(final_used_config_file_path, "w", encoding="utf-8") as f:
        final_config = dict()
        final_config.update(
            {k: str(v) for k, v in args.__dict__.items() if v is not None}
        )
        yaml.safe_dump(final_config, f, default_flow_style=False)
    return args


def attack_training(args):
    # train benign model and get acc
    DatasetWrapper, ModelWrapper, Attack, collate_fn = get_dataset_and_model_wrapper(
        args
    )

    # clean train & test set
    (
        clean_train_set,
        clean_train_set_wrapper,
        clean_train_loader,
        clean_test_set,
        clean_test_set_wrapper,
        clean_test_loader,
    ) = get_clean_dataset_loader(
        DatasetWrapper,
        collate_fn,
        args,
        gpu=True if args.dataset not in ["hmdb51"] else False,
    )

    original_model = load_model(args=args)
    lightning_model = ModelWrapper(model=original_model, args=args)

    attack_log_path = Path(args.attack_log_path)
    benign_log_path = attack_log_path / "benign"
    args.save_folder_name = benign_log_path

    clean_trainer = get_trainer(args, benign_log_path)

    # train benign model
    clean_trainer.fit(model=lightning_model, train_dataloaders=clean_train_loader)
    # test on benign set
    clean_results = clean_trainer.test(
        model=lightning_model, dataloaders=clean_test_loader
    )
    if args.attack_name in TRAINING_CONTRAL_LIST:
        # get poison training set
        poison_train_set = Attack(
            dataset=clean_train_set,
            model=lightning_model.model,
            testset=clean_test_set,
            args=args,
        )
    else:
        # get poison training set
        poison_train_set = Attack(dataset=clean_train_set, mode="train", args=args)
    # save poison training set
    torch.save(poison_train_set, attack_log_path / "poison_train_set.pt")
    poison_train_loader = DataLoader(
        dataset=poison_train_set,
        batch_size=args.batch_size,
        drop_last=True,
        shuffle=True,
        collate_fn=collate_fn,
        num_workers=args.num_workers,
        generator=torch.Generator(
            device="cuda"
            if torch.cuda.is_available() and args.dataset not in ["hmdb51"]
            else "cpu"
        ),
    )

    # get model
    original_model = load_model(args=args)
    lightning_model = ModelWrapper(model=original_model, args=args)

    args.save_folder_name = attack_log_path

    poison_trainer = get_trainer(args, attack_log_path)
    # train backdoor model
    poison_trainer.fit(model=lightning_model, train_dataloaders=poison_train_loader)

    if args.attack_name in TRAINING_CONTRAL_LIST:
        # get poison training set
        poison_test_set = Attack(
            dataset=clean_test_set,
            model=lightning_model.model,
            testset=clean_test_set,
            args=args,
            mode="test",
        )
    else:
        # test on poison dataset
        poison_test_set = Attack(dataset=clean_test_set, mode="test", args=args)

    poison_test_loader = DataLoader(
        dataset=poison_test_set,
        batch_size=args.batch_size,
        drop_last=True,
        collate_fn=collate_fn,
        generator=torch.Generator(
            device="cuda"
            if torch.cuda.is_available() and args.dataset not in ["hmdb51"]
            else "cpu"
        ),
    )
    # save poison test set
    torch.save(poison_test_set, attack_log_path / "poison_test_set.pt")
    results = poison_trainer.test(
        model=lightning_model, dataloaders=[clean_test_loader, poison_test_loader]
    )

    # save results
    results.extend(clean_results)
    print("results:", results)
    save_path = Path(args.attack_log_path) / "results.json"
    save_results(save_path, results)


def prepare_def_training_args(test=False, test_path=None):
    # get training args
    print(
        "============================folder path fetched=================================="
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--defense_log_path", type=str)
    init_args(parser)
    if test:
        args = parser.parse_args(sys.argv[2:])
        args.defense_log_path = test_path
        args.fast_dev = True
    else:
        args = parser.parse_args()
    path = Path(args.defense_log_path)
    print(path.as_posix())
    config_file_path = path / "automation_config.yaml"
    training_config = None
    defense_log_path = None
    training_config_path = None
    if path.is_dir() and Path.exists(config_file_path):
        with open(config_file_path, "r", encoding="utf-8") as f:
            training_config = yaml.safe_load(f)
            print("fetched: %s" % path.as_posix())
            fetched = True
            training_config_path = config_file_path
            defense_log_path = path
    else:
        exit(1)
    args.training_config = training_config
    args.training_config_path = training_config_path
    # update training args to global args
    config_file_name = training_config["defense_name"] + ".yaml"
    add_yaml_to_args(args, training_config_path)
    add_yaml_to_args(
        args,
        BASE_DIR
        / "configs"
        / "defenses"
        / training_config["data_type"]
        / config_file_name,
    )
    # get poison training set

    poison_train_set = defense_log_path.parent / "poison_train_set.pt"
    poison_test_set = defense_log_path.parent / "poison_test_set.pt"
    args.poison_train_set_path = poison_train_set
    args.poison_test_set_path = poison_test_set

    # set gpu
    if args.device == "None":
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        args.device = device

    # get model
    original_model = load_model(args=args)
    args.model_name = args.model
    args.model = original_model

    defense_log_path = defense_log_path
    args.save_folder_name = defense_log_path
    final_used_config_file_path = path / "training_config.yaml"
    with open(final_used_config_file_path, "w", encoding="utf-8") as f:
        final_config = dict()
        final_config.update(
            {k: str(v) for k, v in args.__dict__.items() if v is not None}
        )
        yaml.safe_dump(final_config, f, default_flow_style=False)

    return args


def init_defense(args):
    data_type = args.data_type
    defense_name = args.defense_name
    Defense = None
    collate_fn = None
    match (data_type):
        case "image":
            from backdoormbti.utils.data import CleanDatasetWrapper

            match defense_name:
                case "ac":
                    from backdoormbti.defenses.image import ActivationClustering

                    dsw = CleanDatasetWrapper(load_dataset(args, train=False))
                    Defense = ActivationClustering(
                        dsw,
                        args.model.to(args.device),
                        args,
                    )
                case "strip":
                    from backdoormbti.defenses.image import STRIP

                    dsw = CleanDatasetWrapper(load_dataset(args, train=True))
                    Defense = STRIP(
                        clean_set=dsw,
                        model=args.model,
                        args=args,
                    )
                case "finetune":
                    from backdoormbti.defenses.image import FineTune
                    from backdoormbti.models.wrapper import ImageModelWrapper

                    (
                        clean_train_set,
                        clean_train_set_wrapper,
                        clean_train_loader,
                        clean_test_set,
                        clean_test_set_wrapper,
                        clean_test_loader,
                    ) = get_clean_dataset_loader(CleanDatasetWrapper, collate_fn, args)

                    Defense = FineTune(
                        clean_train_loader=clean_train_loader,
                        clean_test_loader=clean_test_loader,
                        model=ImageModelWrapper(args.model, args),
                        args=args,
                    )
                case "fineprune":
                    from backdoormbti.defenses.image import FinePrune
                    from backdoormbti.models.wrapper import ImageModelWrapper

                    (
                        clean_train_set,
                        clean_train_set_wrapper,
                        clean_train_loader,
                        clean_test_set,
                        clean_test_set_wrapper,
                        clean_test_loader,
                    ) = get_clean_dataset_loader(CleanDatasetWrapper, collate_fn, args)
                    Defense = FinePrune(
                        clean_train_loader=clean_train_loader,
                        clean_test_loader=clean_test_loader,
                        model=ImageModelWrapper(args.model, args),
                        args=args,
                    )
                case "clp":
                    from backdoormbti.defenses.image import ChannelLipschitznessBasedPrune
                    from backdoormbti.models.wrapper import ImageModelWrapper

                    (
                        clean_train_set,
                        clean_train_set_wrapper,
                        clean_train_loader,
                        clean_test_set,
                        clean_test_set_wrapper,
                        clean_test_loader,
                    ) = get_clean_dataset_loader(CleanDatasetWrapper, collate_fn, args)
                    Defense = ChannelLipschitznessBasedPrune(
                        clean_train_loader=clean_train_loader,
                        clean_test_loader=clean_test_loader,
                        model=ImageModelWrapper(args.model, args),
                        args=args,
                    )
                case "nc":
                    from backdoormbti.defenses.image import NeuralCleanse
                    from backdoormbti.models.wrapper import ImageModelWrapper

                    (
                        clean_train_set,
                        clean_train_set_wrapper,
                        clean_train_loader,
                        clean_test_set,
                        clean_test_set_wrapper,
                        clean_test_loader,
                    ) = get_clean_dataset_loader(CleanDatasetWrapper, collate_fn, args)
                    Defense = NeuralCleanse(
                        clean_train_loader=clean_train_loader,
                        clean_test_loader=clean_test_loader,
                        model=ImageModelWrapper(args.model, args),
                        args=args,
                    )
                case "abl":
                    from backdoormbti.defenses.image import ABL
                    from backdoormbti.models.wrapper import ImageModelWrapper

                    (
                        clean_train_set,
                        clean_train_set_wrapper,
                        clean_train_loader,
                        clean_test_set,
                        clean_test_set_wrapper,
                        clean_test_loader,
                    ) = get_clean_dataset_loader(CleanDatasetWrapper, collate_fn, args)
                    Defense = ABL(
                        clean_train_loader=clean_train_loader,
                        clean_test_loader=clean_test_loader,
                        model=ImageModelWrapper(args.model, args),
                        args=args,
                    )
                case "tabor":
                    from backdoormbti.defenses.image import TABOR
                    from backdoormbti.models.wrapper import ImageModelWrapper

                    (
                        clean_train_set,
                        clean_train_set_wrapper,
                        clean_train_loader,
                        clean_test_set,
                        clean_test_set_wrapper,
                        clean_test_loader,
                    ) = get_clean_dataset_loader(CleanDatasetWrapper, collate_fn, args)
                    Defense =TABOR(
                        clean_train_loader=clean_train_loader,
                        clean_test_loader=clean_test_loader,
                        model=ImageModelWrapper(args.model, args),
                        args=args,
                    )    
                case _:
                    raise NotImplementedError(
                        "not supported defense: %s" % defense_name
                    )
        case "text":
            from backdoormbti.utils.data import CleanTextDatasetWrapper

            match defense_name:
                case "strip":
                    from backdoormbti.defenses.text import STRIP

                    dsw = CleanTextDatasetWrapper(load_dataset(args, train=False))
                    Defense = STRIP(
                        clean_set=dsw,
                        model=args.model,
                        args=args,
                    )
                case "rap":
                    from backdoormbti.defenses.text import RAP

                    dsw = CleanTextDatasetWrapper(load_dataset(args))
                    Defense = RAP(
                        clean_set=dsw,
                        model=args.model,
                        args=args,
                    )
                case "onion":
                    from backdoormbti.defenses.text import ONION

                    dsw = CleanTextDatasetWrapper(load_dataset(args))
                    Defense = ONION(
                        clean_set=dsw,
                        model=args.model,
                        args=args,
                    )
                case _:
                    raise NotImplementedError(
                        "not supported defense: %s" % defense_name
                    )
        case "audio":
            match defense_name:
                case "strip":
                    from backdoormbti.defenses.audio import STRIP
                    from backdoormbti.utils.data import CleanAudioDatasetWrapper

                    dsw = CleanAudioDatasetWrapper(load_dataset(args))
                    Defense = STRIP(
                        clean_set=dsw,
                        model=args.model,
                        args=args,
                    )
                case _:
                    raise NotImplementedError(
                        "not supported defense: %s" % defense_name
                    )
            from backdoormbti.utils.collate_fn import AudioCollator

            collate_fn = AudioCollator(args=argparse)
        case "video":
            match defense_name:
                case "badnet":
                    from backdoormbti.defenses.video import STRIP
                    from backdoormbti.utils.data import CleanVideoDatasetWrapper

                    dsw = CleanVideoDatasetWrapper(load_dataset(args, train=False))
                    Defense = STRIP(
                        clean_set=dsw,
                        model=args.model,
                        args=args,
                    )
                case _:
                    raise NotImplementedError(
                        "not supported defense: %s" % defense_name
                    )
            from backdoormbti.utils.collate_fn import video_collate_fn

            collate_fn = video_collate_fn

        case _:
            raise NotImplementedError("not supported data type: %s", data_type)
    args.collate_fn = collate_fn
    return Defense
