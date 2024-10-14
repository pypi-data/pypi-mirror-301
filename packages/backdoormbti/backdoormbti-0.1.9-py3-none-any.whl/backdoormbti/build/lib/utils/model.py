import torch

from backdoormbti.configs.settings import DATA_DIR
from backdoormbti.utils.collate_fn import audio_pre_trans

def load_poisoned_model(args):
    '''

   这只是一个测试用例，正式使用时请删除该用例，谢谢
    '''
    match args.attack_name:
        case "badnet":
            from torchvision.models import resnet18

            model = resnet18(num_classes=args.num_classes)
            model.load_state_dict(torch.load("path/resnet18.pth"))
        case "hpt":
            from torchvision.models import resnet18

            model = resnet18(num_classes=args.num_classes)
            model.load_state_dict(torch.load("resources/hpt/attack_model.th"))
        case _:
            raise NotImplementedError("Model %s not supported." % args.model)
    return model.to(args.device)

def load_model(args, **kwargs):
    match args.model:
        # mnist model
        case "simple":
            from backdoormbti.models.custom import SimpleNet

            model = SimpleNet(num_classes=args.num_classes)
        # image model
        case "preactresnet18":
            from backdoormbti.models.custom import PreActResNet18

            model = PreActResNet18(num_classes=args.num_classes)
        case "resnet18":
            from torchvision.models import resnet18

            model = resnet18(num_classes=args.num_classes)
        case "dbdresnet18":
            from backdoormbti.models.custom import dbdresnet18

            model = dbdresnet18(args=args)

        case "resnet34":
            from torchvision.models import resnet34

            model = resnet34(num_classes=args.num_classes)
        case "resnet50":
            from torchvision.models import resnet50

            model = resnet50(num_classes=args.num_classes)
        case "alexnet":
            from torchvision.models import alexnet

            model = alexnet(num_classes=args.num_classes)
        case "vgg11":
            from torchvision.models import vgg11

            model = vgg11(num_classes=args.num_classes)
        case "vgg16":
            from torchvision.models import vgg16

            model = vgg16(num_classes=args.num_classes)
        case "vgg19":
            from torchvision.models import vgg19

            model = vgg19(num_classes=args.num_classes)

        case "densenet121":
            from torchvision.models import densenet121

            model = densenet121(num_classes=args.num_classes)
        case "densenet161":
            from torchvision.models import densenet161

            model = densenet161(num_classes=args.num_classes)
        case "mobilenet_v2":
            from torchvision.models import mobilenet_v2

            model = mobilenet_v2(num_classes=args.num_classes)
        case "inception_v3":
            from torchvision.models import inception_v3

            model = inception_v3(num_classes=args.num_classes)
        case "googlenet":
            from torchvision.models import googlenet

            model = googlenet(num_classes=args.num_classes)
        case "shufflenet_v2_x1_0":
            from torchvision.models import shufflenet_v2_x1_0

            model = shufflenet_v2_x1_0(num_classes=args.num_classes)

        case "efficientnet_b0":
            from torchvision.models import efficientnet_b0

            model = efficientnet_b0(num_classes=args.num_classes)
        case "vit_b_16":
            from torchvision.models import ViT_B_16_Weights, vit_b_16
            from torchvision.transforms import Resize

            model = vit_b_16(
                weights=ViT_B_16_Weights.IMAGENET1K_V1,
                **{k: v for k, v in kwargs.items() if k != "pretrained"},
            )
            model.heads.head = torch.nn.Linear(
                model.heads.head.in_features, out_features=args.num_classes, bias=True
            )
            model = torch.nn.Sequential(
                Resize((224, 224), antialias=True),
                model,
            )
        # text model
        case "bert" | "roberta" | "gpt2":
            from transformers import (
                AutoConfig,
                AutoModelForSequenceClassification,
                AutoTokenizer,
            )

            if args.use_local:
                cache_dir = DATA_DIR / "models" / args.model_path
                model_path = cache_dir.resolve()
            else:
                model_path = args.model_path

            if hasattr(args, "defense_name") and args.defense_name in ["ac"]:
                kwargs.update({"output_hidden_states": True})

            if args.pretrain:
                # load pretrained model
                model_config = AutoConfig.from_pretrained(model_path)
                model_config.num_labels = args.num_classes
                model_config.update(kwargs)
                model = AutoModelForSequenceClassification.from_pretrained(
                    model_path,
                    config=model_config,
                )
                tokenizer = AutoTokenizer.from_pretrained(
                    model_path, model_max_length=512
                )
                if tokenizer.pad_token is None and args.model in ["gpt2", "roberta"]:
                    tokenizer.pad_token = tokenizer.eos_token
                    # set the pad token of the model's configuration
                    model.config.pad_token_id = model.config.eos_token_id
                    print(
                        f"Added [PAD] token to the tokenizer for gpt2: {tokenizer.pad_token}"
                    )
                args.tokenizer = tokenizer
            else:
                # load a new model
                raise NotImplementedError("not supported.")
        # case "deepspeech":
        #     from torchaudio.models import DeepSpeech

        #     model = DeepSpeech(
        #         n_feature=args.input_size, n_class=args.num_classes
        #     )
        case "audiocnn":
            from backdoormbti.models.custom import AudioCNN

            model = AudioCNN(n_input=1, n_output=args.num_classes)
        case "lstm":
            from backdoormbti.models.custom import AudioLSTM

            args.pre_trans = audio_pre_trans
            model = AudioLSTM(
                input_size=128,
                hidden_size=128,
                num_layers=2,
                num_classes=args.num_classes,
            )
        case "xvector":
            from backdoormbti.models.custom import TDNN, X_Vector

            args.pre_trans = audio_pre_trans
            model = X_Vector(input_dim=128, num_classes=args.num_classes)
            # model = TDNN(input_dim=128, output_dim=args.num_classes)
        case "vggvox":
            from backdoormbti.models.custom import VGGVox

            model = VGGVox(nOut=args.num_classes)
        case "r3d":
            from torchvision.models.video import R3D_18_Weights, r3d_18

            weights = R3D_18_Weights.DEFAULT
            trans = weights.transforms()
            args.transforms = trans
            model = r3d_18(weights=weights)
        case "speechembedder": 
            from backdoormbti.models.custom import SpeechEmbedder
            model = SpeechEmbedder()
        case _:
            raise NotImplementedError("Model %s not supported." % args.model)
    return model.to(args.device)
