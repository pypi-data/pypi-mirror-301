from typing import Literal

from configs.settings import DEFENSES
from models.wrapper import *


def get_data_spec_class_by_args(
    args, ret_item=Literal["DatasetWrapper", "ModelWrapper", "collate_fn", "all"]
):
    assert args.data_type is not None
    collate_fn = None
    match (args.data_type):
        case "image":

            from utils.data import CleanDatasetWrapper

            DatasetWrapper = CleanDatasetWrapper
            ModelWrapper = ImageModelWrapper

        case "text":
            import os

            from utils.data import CleanTextDatasetWrapper

            os.environ["TOKENIZERS_PARALLELISM"] = "true"

            DatasetWrapper = CleanTextDatasetWrapper
            ModelWrapper = TextModelWrapper

        case "audio":

            from utils.collate_fn import AudioCollator
            from utils.data import CleanAudioDatasetWrapper

            DatasetWrapper = CleanAudioDatasetWrapper
            ModelWrapper = AudioModelWrapper

            collate_fn = AudioCollator(args)
        case "video":
            from utils.collate_fn import video_collate_fn
            from utils.data import CleanVideoDatasetWrapper

            DatasetWrapper = CleanVideoDatasetWrapper
            ModelWrapper = VideoModelWrapper

            collate_fn = video_collate_fn
        case _:
            raise NotImplementedError("not supported data type: %s", args.data_type)

    # ret the item requested
    if ret_item == "DatasetWrapper":
        return DatasetWrapper
    elif ret_item == "ModelWrapper":
        return ModelWrapper
    elif ret_item == "collate_fn":
        return collate_fn
    elif ret_item == "all":
        return DatasetWrapper, ModelWrapper, collate_fn


def get_defense_by_args(args):
    assert args.defense_name is not None
    assert args.defense_name in DEFENSES

    Defense = None
    match (args.defense_name):
        case "strip":
            from defenses.strip import STRIP

            Defense = STRIP
        case "finetune":
            from defenses.finetune import FineTune

            Defense = FineTune
        case "fineprune":
            from defenses.fineprune import FinePrune

            Defense = FinePrune
        case "clp":
            from defenses.clp import ChannelLipschitznessBasedPrune

            Defense = ChannelLipschitznessBasedPrune

        case "ac":
            from defenses.ac import ActivationClustering

            Defense = ActivationClustering
        case "abl":
            from defenses.abl import ABL

            Defense = ABL
        case "nc":
            from defenses.nc import NeuralCleanse

            Defense = NeuralCleanse
        case "onion":
            from defenses.text import ONION

            Defense = ONION
        case "rap":
            from defenses.text import RAP

            Defense = RAP
        case "bki":
            from defenses.text import BKI

            Defense = BKI
        case "anp":
            from defenses.anp import AdversarialNeuronPrune

            Defense = AdversarialNeuronPrune

        case "ss":
            from defenses.ss import SpectralSignature

            Defense = SpectralSignature

        case "tabor":
            from defenses.tabor import TABOR

            Defense = TABOR
        case "nad":
            from defenses.image.nad import NAD

            Defense = NAD
        case "scale_up":
            from defenses.image.scale_up import ScaleUp

            Defense = ScaleUp
        case "mntd":
            from defenses.image.mntd import MNTD

            Defense = MNTD
        case _:
            raise NotImplementedError("not supported defense: %s" % args.defense_name)
    return Defense


def get_attack_by_args(args):
    assert args.data_type is not None
    assert args.attack_name is not None
    data_type = args.data_type
    attack_name = args.attack_name
    match (data_type):
        case "image":
            ModelWrapper = ImageModelWrapper
            match (attack_name):
                case "badnet":
                    from attacks.image import BadNet, BadNetModelWrapper

                    Attack = BadNet
                    ModelWrapper = BadNetModelWrapper
                case "blend":
                    from attacks.image import Blend

                    Attack = Blend
                case "labelconsistent":
                    from attacks.image import LabelConsistent

                    Attack = LabelConsistent
                case "bpp":
                    from attacks.image import BPP

                    Attack = BPP
                case "wanet":
                    from attacks.image import WaNet

                    Attack = WaNet
                case "ssba":
                    from attacks.image import SSBA

                    Attack = SSBA
                case "sig":
                    from attacks.image import SIG

                    Attack = SIG
                case "refool":
                    from attacks.image import Refool

                    Attack = Refool
                case "IMC":
                    from attacks.image import IMC

                    Attack = IMC
                case "ubw":
                    from attacks.image import UBW, UBWModelWrapper

                    Attack = UBW
                    ModelWrapper = UBWModelWrapper
                case "trojan":
                    from attacks.image import TrojanPoisonGenerator

                    Attack = TrojanPoisonGenerator
                case "sbat":
                    from attacks.image import SBAT

                    Attack = SBAT
                case "embtrojan":
                    from attacks.image import EmbTrojan, EmbTrojanModelWrapper

                    Attack = EmbTrojan
                    ModelWrapper = EmbTrojanModelWrapper
                case "DynaTrigger":
                    from attacks.image import DynaTrigger, DynaTriggerModelWrapper

                    Attack = DynaTrigger
                    ModelWrapper = DynaTriggerModelWrapper
                case "AdaptiveBlend":
                    from attacks.image import AdaptiveBlend

                    Attack = AdaptiveBlend
                case "iad":
                    from attacks.image import InputAwareAttack

                    Attack = InputAwareAttack
                case "lowfreq":
                    from attacks.image import LowFrequency

                    Attack = LowFrequency
                case "pnoiseattack":
                    from attacks.image import PnoiseAttack, PnoiseAttackModelWrapper

                    Attack = PnoiseAttack
                    ModelWrapper = PnoiseAttackModelWrapper
                case _:
                    raise NotImplementedError("not supported attack: %s" % attack_name)
        case "text":
            ModelWrapper = TextModelWrapper
            match (attack_name):
                case "badnet":
                    from attacks.text import BadNet

                    Attack = BadNet
                case "addsent":
                    from attacks.text import AddSent

                    Attack = AddSent
                case "stylebkd":
                    from attacks.text import StyleBKD

                    Attack = StyleBKD
                case "synbkd":
                    from attacks.text import SynBKD

                    Attack = SynBKD
                case "lwp":
                    from attacks.text import LWP

                    Attack = LWP
                case "bite":
                    from attacks.text import BITE

                    Attack = BITE
                case _:
                    raise NotImplementedError("not supported attack: %s" % attack_name)
        case "audio":
            ModelWrapper = AudioModelWrapper
            match (attack_name):
                case "badnet":
                    from attacks.audio import BadNet

                    Attack = BadNet
                case "blend":
                    from attacks.audio import Blend

                    Attack = Blend
                case "gis":
                    from attacks.audio import GIS

                    Attack = GIS
                case "ultrasonic":
                    from attacks.audio import UltraSonic

                    Attack = UltraSonic
                case "daba":
                    from attacks.audio import DABA

                    Attack = DABA
                case "baasv":
                    from attacks.audio import Baasv

                    Attack = Baasv
                case _:
                    raise NotImplementedError("not supported attack: %s" % attack_name)
        case "video":
            ModelWrapper = VideoModelWrapper
            match (attack_name):
                case "badnet":
                    from attacks.video import BadNet

                    Attack = BadNet
                case "blend":
                    from attacks.video import Blend

                    Attack = Blend
                case "tuap":
                    from attacks.video import TUAP

                    Attack = TUAP
                case _:
                    raise NotImplementedError("not supported attack: %s" % attack_name)
        case _:
            raise NotImplementedError("not supported data type: %s", data_type)
    return Attack, ModelWrapper
