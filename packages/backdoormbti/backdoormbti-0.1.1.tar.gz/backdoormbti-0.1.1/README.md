# BackdoorMBTI

BackdoorMBTI is an open source project expanding the unimodal backdoor learning to a multimodal context.  We hope that BackdoorMBTI can facilitate the analysis and development of backdoor defense methods within a multimodal context.

 main feature：
 - poison dataset generateion
 - backdoor model generation
 - attack training
 - defense training
 - backdoor evaluation

The framework:
![framework](./resources/arch.png)
## Task Supported


| Task                       | Dataset        | Modality |
|:---------------------------|:---------------|:---------|
| Object Classification      | CIFAR10        | Image    |
| Object Classification      | TinyImageNet   | Image    |
| Traffic Sign Recognition   | GTSRB          | Image    |
| Facial Recognition         | CelebA         | Image    |
| Sentiment Analysis         | SST-2          | Text     |
| Sentiment Analysis         | IMDb           | Text     |
| Topic Classification       | DBpedia        | Text     |
| Topic Classification       | AG’s News      | Text     |
| Speech Command Recognition | SpeechCommands | Audio    |
| Music Genre Classification | GTZAN          | Audio    |
| Speaker Identification     | VoxCeleb1      | Audio    |


### Backdoor Attacks Supported

| Modality | Attack      | Visible   | Pattern | Add | Sample Specific | paper |
|:--------:|:------------|:----------:|:--------:|:----:|:-----:|:----|
|Image| AdaptiveBlend     | Invisible   | Global   | Yes | No   | [REVISITING THE ASSUMPTION OF LATENT SEPARABILITY FOR BACKDOOR DEFENSES](https://openreview.net/pdf?id=_wSHsgrVali)    |
|Image| BadNets     | Visible   | Local   | Yes | No   | [Badnets: Evaluating backdooring attacks on deep neural networks](https://ieeexplore.ieee.org/iel7/6287639/8600701/08685687.pdf)    |
|Image| Blend(under test)    | InVisible   | Global   | Yes | Yes   | [A NEW BACKDOOR ATTACK IN CNNS BY TRAINING SET CORRUPTION WITHOUT LABEL POISONING](https://arxiv.org/abs/1712.05526v1)    |
|Image| Blind(under test)     | Visible   | Local   | Yes |Yes   | [Blind Backdoors in Deep Learning Models](https://www.cs.cornell.edu/~shmat/shmat_usenix21blind.pdf)    |
|Image| BPP         | Invisible | Global  | Yes | No   | [Bppattack: Stealthy and efficient trojan attacks against deep neural networks via image quantization and contrastive adversarial learning](http://openaccess.thecvf.com/content/CVPR2022/papers/Wang_BppAttack_Stealthy_and_Efficient_Trojan_Attacks_Against_Deep_Neural_Networks_CVPR_2022_paper.pdf)     |
|Image| DynaTrigger | Visible   | Local   | Yes | Yes  | [Dynamic backdoor attacks against machine learning models](https://arxiv.org/pdf/2003.03675)    |
|Image| EMBTROJAN(under test)     | Inisible   | Local   | Yes | No   | [An Embarrassingly Simple Approach for Trojan Attack in Deep Neural Networks](https://dl.acm.org/doi/pdf/10.1145/3394486.3403064)    |
|Image| LC          | Invisible | Global  | No  | Yes  | [Label-consistent backdoor attacks](https://openaccess.thecvf.com/content/ICCV2021/papers/Zeng_Rethinking_the_Backdoor_Attacks_Triggers_A_Frequency_Perspective_ICCV_2021_paper.pdf)    |
|Image| Lowfreq          | Invisible | Global  | Yes | Yes  |[Rethinking the Backdoor Attacks’ Triggers: A Frequency Perspective](https://arxiv.org/pdf/1912.02771/)    |
|Image| PNoise      | Invisible | Global  | Yes | Yes  | [Use procedural noise to achieve backdoor attack](https://ieeexplore.ieee.org/iel7/6287639/9312710/09529206.pdf)    |
|Image| Refool      | Invisible | Global   | Yes | No  | [Reflection Backdoor: A Natural Backdoor Attack on Deep Neural Networks](https://www.ecva.net/papers/eccv_2020/papers_ECCV/papers/123550188.pdf)    |
|Image| SBAT        | Invisible | Global  | No  | Yes  | [Stealthy Backdoor Attack with Adversarial Training](https://ieeexplore.ieee.org/abstract/document/9746008/) |
|Image| SIG | Invisible   | Global   | Yes | No  | [A NEW BACKDOOR ATTACK IN CNNS BY TRAINING SET CORRUPTION WITHOUT LABEL POISONING](https://arxiv.org/pdf/1902.11237)    |
|Image| SSBA        | Invisible | Global  | No  | Yes  | [Invisible Backdoor Attack with Sample-Specific Triggers](https://openaccess.thecvf.com/content/ICCV2021/papers/Li_Invisible_Backdoor_Attack_With_Sample-Specific_Triggers_ICCV_2021_paper.pdf)    |
|Image| trojanNN(under test)       | Visible | Local  | Yes  | Yes  | [Trojaning Attack on Neural Network](https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=2782&context=cstech)    |
|Image| ubw(under test)       | Invisible | Global  | Yes  | No  | [Untargeted Backdoor Watermark: Towards Harmless and Stealthy Dataset Copyright Protection](https://proceedings.neurips.cc/paper_files/paper/2022/file/55bfedfd31489e5ae83c9ce8eec7b0e1-Paper-Conference.pdf)    |
|Image| WaNet       | Invisible | Global  | No  | Yes  | [WaNet -- Imperceptible Warping-Based Backdoor Attack](https://arxiv.org/pdf/2102.10369)    |
|Text | AddSent     | Visible   | Local   | Yes | No   | [A backdoor attack against LSTM-based text classification systems](https://arxiv.org/pdf/1905.12457.pdf)    |
|Text | BadNets     | Visible   | Local   | Yes | No   |  [Badnets: Evaluating backdooring attacks on deep neural networks](https://ieeexplore.ieee.org/iel7/6287639/8600701/08685687.pdf)     |
|Text | BITE        | Invisible | Local   | Yes | Yes  | [Textual backdoor attacks with iterative trigger injection](https://u1x3881ofs0.feishu.cn/sheets/VHbrsq8MdhV7BPtd77Nc6BGSnIc?sheet=ae56f0&range=QTE4)    |
|Text | LWP         | Visible   | Local   | Yes | No   | [Backdoor Attacks on Pre-trained Models by Layerwise Weight Poisoning](https://aclanthology.org/2021.emnlp-main.241.pdf)    |
|Text | STYLEBKD      | Visible | Global  | No  | Yes  | [Mind the Style of Text! Adversarial and Backdoor Attacks Based on Text Style Transfer](https://arxiv.org/pdf/2110.07139)    |
|Text | SYNBKD      | Invisible | Global  | No  | Yes  | [Hidden Killer: Invisible Textual Backdoor Attacks with Syntactic Trigger](https://arxiv.org/pdf/2105.12400.pdf)    |
|Audio| Baasv(under test)       | \-        |  Global    | Yes | No   | [Backdoor Attack against Speaker Verification](https://arxiv.org/pdf/2010.11607)    |
|Audio| Blend       | \-        | Local   | Yes | No   | [Targeted Backdoor Attacks on Deep Learning Systems Using Data Poisoning](https://arxiv.org/abs/1712.05526v1)    |
|Audio| DABA        | \-        | Global  | Yes | No   | [Opportunistic Backdoor Attacks: Exploring Human-imperceptible Vulnerabilities on Speech Recognition Systems](https://dl.acm.org/doi/abs/10.1145/3503161.3548261)    |
|Audio| GIS         | \-        | Global  | No  | No   | [Going in style: Audio backdoors through stylistic transformations](https://arxiv.org/pdf/2211.03117)    |
|Audio| UltraSonic  | \-        | Local   | Yes | No   | [Can You Hear It? Backdoor Attacks via Ultrasonic Triggers](https://github.com/skoffas/ultrasonic_backdoor)    |


### Backdoor Defenses Supported


| Defense |Modality| Input | Stage | Output | Paper | 
|:-------:|:-----:|:-----:|:---:|:-----:|:-----:|
|  STRIP  | Audio,Image and text |backdoor model, clean dataset| post-training | clean dataset    | [STRIP: A Defence Against Trojan Attacks on Deep Neural Networks](https://arxiv.org/pdf/1902.06531.pdf)      |
|   AC    | Audio,Image and text |backdoor model, clean dataset, poison dataset| post-training    | clean model, clean datasest    | [Detecting Backdoor Attacks on Deep Neural Networks by Activation Clustering](https://arxiv.org/pdf/1811.03728.pdf)      | 
|   FT    | Audio,Image and text |backdoor model, clean dataset| in-training | clean model    | [Fine-Pruning: Defending Against Backdooring Attacks on Deep Neural Networks.](https://arxiv.org/pdf/1805.12185.pdf) |
|   FP    | Audio,Image and text |backdoor model, clean dataset| post-training | clean model    | [Fine-Pruning: Defending Against Backdooring Attacks on Deep Neural Networks.](https://arxiv.org/pdf/1805.12185.pdf)      |
|   ABL   | Audio,Image and text |backdoor model, poison dataset| in-training | clean model    | [Anti-Backdoor Learning: Training Clean Models on Poisoned Data](https://arxiv.org/pdf/2110.11571.pdf)      |
|   CLP   | Audio,Image and text |backdoor model| post-training    | clean model | [Data-free Backdoor Removal based on Channel Lipschitzness](https://arxiv.org/pdf/2208.03111.pdf)      |
|   NC    | Image|backdoor model, clean dataset| post-training | clean model, trigger pattern    | [Neural Cleanse: Identifying and Mitigating Backdoor Attacks in Neural Networks](https://gangw.web.illinois.edu/class/cs598/papers/sp19-poisoning-backdoor.pdf)      |


## Installation

To install the virtual environment:
```
conda create -n bkdmbti python=3.10
conda activate bkdmbti
pip install -r requirements.txt
```

## Quick Start

### Download Data

Download the data if it can not be downloaded automatically. Some data download scripts are provided in `scripts` folder.

### Backdoor Attack 

Here we provide an example to quickly start with the attack experiments, and reproduce the BadNets backdoor attack results. We use resnet-18 as the default model, and 0.1 as the default poison ratio.
```
cd scripts
python atk_train.py --data_type image --dataset cifar10  --attack_name badnet --model resnet18 --pratio 0.1 --num_workers 4 --epochs 100 
python atk_train.py --data_type audio --dataset speechcommands --attack_name blend --model audiocnn --pratio 0.1 --num_workers 4 --epochs 100 --add_noise true
python atk_train.py --data_type text --dataset sst2 --attack_name addsent --model bert --pratio 0.1 --num_workers 4 --epochs 100 --mislabel true
```
Use args `--add_noise true` and `--mislabel true` to add perturbations to the data. After the experiment, metrics ACC(Accuracy), ASR(Attack Success Rate) and RA(Robustness Accuracy) are collected in attack phase.
To learn more about the attack command, you can  run `python atk_train.py -h` to see more details.
### Backdoor Defense

Here we provide a defense example, it depends on the backdoor model generated in the attack phase, so you should run the corresponding attack experiment before defense phase.
```
cd scripts
python def_train.py --data_type image --dataset cifar10 --attack_name badnet  --pratio 0.1 --defense_name finetune --num_workers 4 --epochs 10 
python def_train.py --data_type audio --dataset speechcommands --attack_name blend  --model audiocnn --pratio 0.1 --defense_name fineprune --num_workers 4 --epochs 1 --add_noise true
python def_train.py --data_type text --dataset sst2 --attack_name addsent --model bert --pratio 0.1 --defense_name strip --num_workers 4 --epochs 1 --mislabel true
```
To learn more about the attack command, you can  run `python def_train.py -h` to see more details.
In defense phase, detection accuracy will be collected if the defense is a detection method, and then the sanitized dataset will be used to retrain the model. ACC, ASR and RA metrics are collected after retraining.


# Results
More results can be found in: [results.md](./results.md)
