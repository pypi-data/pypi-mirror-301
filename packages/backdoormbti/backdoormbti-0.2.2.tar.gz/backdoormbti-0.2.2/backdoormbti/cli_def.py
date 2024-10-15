# backdoormbti/cli_def.py
import argparse
from backdoormbti.scripts.def_train import def_train
from backdoormbti.utils.args import init_args, add_yaml_to_args
from backdoormbti.utils.io import get_cfg_path_by_args, get_train_cfg_path_by_args

def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser()
    init_args(parser)
    atk_args = parser.parse_args()
    def_args = parser.parse_args()

    # 加载攻击和防御配置
    atk_conf_path = get_cfg_path_by_args(atk_args, "attacks")
    add_yaml_to_args(atk_args, atk_conf_path)
    
    def_conf_path = get_cfg_path_by_args(def_args, "defenses")
    add_yaml_to_args(def_args, def_conf_path)
    
    train_conf_path = get_train_cfg_path_by_args(def_args.data_type)
    add_yaml_to_args(def_args, train_conf_path)

    # 调用 def_train 函数
    def_train(atk_args, def_args)

if __name__ == "__main__":
    main()
