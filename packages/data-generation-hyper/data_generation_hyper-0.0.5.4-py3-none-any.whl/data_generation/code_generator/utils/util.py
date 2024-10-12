import json
import argparse

from code_generator.dataframe_generation.code_gen_parallel import generate_training
from code_generator.helpers.save_batches import save_final


def pipeline(args): 
    save_final(generate_training(**args))


def parse_args():

    with open(r'app\functions\code_generator\config\arguments.json', 'r') as f:
        default_args_dict = json.load(f)

    parser = argparse.ArgumentParser(description="Pipeline Argument Parser")

    for arg_name, default_value in default_args_dict.items():
        parser.add_argument(f'--{arg_name}', type=type(default_value), default=default_value,
                            help=f'Value for {arg_name}. Default is {default_value}')

    args = parser.parse_args()

    args_dict = vars(args)
    return args_dict