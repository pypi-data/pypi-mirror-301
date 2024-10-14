# backdoormbti/cli_atk.py
import argparse
from backdoormbti.scripts.atk_train import atk_train
from backdoormbti.utils.args import init_args, add_yaml_to_args
from backdoormbti.utils.io import get_cfg_path_by_args

def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser()
    init_args(parser)
    args = parser.parse_args()

    # 加载配置文件
    conf_path = get_cfg_path_by_args(args, "attacks")
    add_yaml_to_args(args, conf_path)

    # 调用 atk_train 函数
    atk_train(args)

if __name__ == "__main__":
    main()
