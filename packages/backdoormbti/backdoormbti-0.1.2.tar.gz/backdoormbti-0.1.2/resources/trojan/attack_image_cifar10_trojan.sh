#!/bin/bash

SCRIPT_DIR=$(dirname "$0")
PROJECT_ROOT=$(realpath "$SCRIPT_DIR/../../")

DATA_TYPE="image"
DATASET="cifar10"
ATTACK_NAME="trojan"
MODEL="resnet18"
PRATIO=0.1
NUM_WORKERS=4

# 设置 PYTHONPATH 以确保可以找到 utils 模块
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"


# 生成毒化数据集
python -m attacks.image.trojan

# 运行训练脚本
python "$PROJECT_ROOT/scripts/atk_train.py" --data_type $DATA_TYPE --dataset $DATASET --attack_name $ATTACK_NAME --model $MODEL --pratio $PRATIO --num_workers $NUM_WORKERS


# 运行脚本：bash resources/trojan/attack_image_cifar10_trojan.sh


# 实验运行设备信息:
# Linux vol05.pi.sjtu.edu.cn 4.18.0-372.75.1.1.kos5.x86_64 #1 SMP Wed Oct 25 04:41:06 EDT 2023 x86_64 x86_64 x86_64 GNU/Linux
# PRETTY_NAME="kos 5.8"
# NAME="Red Hat Enterprise Linux"
# VERSION="8.6 (Ootpa)"
# ID="rhel"
# ID_LIKE="fedora"
# VERSION_ID="8.6"
# PLATFORM_ID="platform:el8"
# ANSI_COLOR="0;31"
# CPE_NAME="cpe:/o:redhat:enterprise_linux:8::baseos"
# HOME_URL="https://www.redhat.com/"
# DOCUMENTATION_URL="https://access.redhat.com/documentation/red_hat_enterprise_linux/8/"
# BUG_REPORT_URL="https://bugzilla.redhat.com/"
# REDHAT_BUGZILLA_PRODUCT="Red Hat Enterprise Linux 8"
# REDHAT_BUGZILLA_PRODUCT_VERSION=8.6
# REDHAT_SUPPORT_PRODUCT="Red Hat Enterprise Linux"
# REDHAT_SUPPORT_PRODUCT_VERSION="8.6"


# 开始实验运行设备和显存消耗情况:
# Thu Jun 13 00:03:08 2024       
# +---------------------------------------------------------------------------------------+
# | NVIDIA-SMI 545.23.08              Driver Version: 545.23.08    CUDA Version: 12.3     |
# |-----------------------------------------+----------------------+----------------------+
# | GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
# | Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
# |                                         |                      |               MIG M. |
# |=========================================+======================+======================|
# |   0  Tesla V100-SXM3-32GB           On  | 00000000:E7:00.0 Off |                    0 |
# | N/A   46C    P0              52W / 350W |      0MiB / 32768MiB |      0%      Default |
# |                                         |                      |                  N/A |
# +-----------------------------------------+----------------------+----------------------+
                                                                                         
# +---------------------------------------------------------------------------------------+
# | Processes:                                                                            |
# |  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
# |        ID   ID                                                             Usage      |
# |=======================================================================================|
# |  No running processes found                                                           |
# +---------------------------------------------------------------------------------------+


# 数据集：cifar10


# 实验结果
# Epoch 99: 100%|██████████████████████████████████████████████████████████████████████████████████| 782/782 [00:14<00:00, 54.06it/s, v_num=4, train_loss_step=0.144, train_loss_epoch=0.0388]
# INFO:attack:training finished
# INFO:attack:loading test data
# Files already downloaded and verified
# INFO:attack:test data loaded
# INFO:attack:start testing
# LOCAL_RANK: 0 - CUDA_VISIBLE_DEVICES: [0]
# Testing DataLoader 1: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 141/141 [00:00<00:00, 144.03it/s]
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃        Test metric        ┃       DataLoader 0        ┃       DataLoader 1        ┃
# ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
# │         test_asr          │                           │            1.0            │
# │      test_clean_acc       │    0.8619999885559082     │                           │
# │          test_ra          │                           │            0.0            │
# └───────────────────────────┴───────────────────────────┴───────────────────────────┘
# INFO:attack:test finished
# INFO:attack:results.json save in: /lustre/home/acct-stu/stu378/newwwBackdoorMMT/logs/image-trojan-cifar10-resnet18-pratio-0.1--normal/results.json


# 实验结束后的设备和显存消耗情况:
# Thu Jun 13 00:58:39 2024       
# +---------------------------------------------------------------------------------------+
# | NVIDIA-SMI 545.23.08              Driver Version: 545.23.08    CUDA Version: 12.3     |
# |-----------------------------------------+----------------------+----------------------+
# | GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
# | Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
# |                                         |                      |               MIG M. |
# |=========================================+======================+======================|
# |   0  Tesla V100-SXM3-32GB           On  | 00000000:E7:00.0 Off |                    0 |
# | N/A   49C    P0              85W / 350W |      0MiB / 32768MiB |      0%      Default |
# |                                         |                      |                  N/A |
# +-----------------------------------------+----------------------+----------------------+
                                                                                         
# +---------------------------------------------------------------------------------------+
# | Processes:                                                                            |
# |  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
# |        ID   ID                                                             Usage      |
# |=======================================================================================|
# |  No running processes found                                                           |
# +---------------------------------------------------------------------------------------+


# 本次实验时长: 55 分钟 31 秒