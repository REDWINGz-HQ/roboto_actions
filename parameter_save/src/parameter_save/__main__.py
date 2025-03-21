import argparse
import os
import pathlib
from pyulog import ULog
from roboto.env import RobotoEnvKey


# Argument Parser Setup
parser = argparse.ArgumentParser()
parser.add_argument(
    "-i", 
    "--input-dir", 
    dest="input_dir", 
    type=pathlib.Path, 
    default=os.environ.get(RobotoEnvKey.InputDir.value), 
    help="Directory containing input files"
)
parser.add_argument(
    "-o", 
    "--output-dir", 
    dest="output_dir", 
    type=pathlib.Path, 
    default=os.environ.get(RobotoEnvKey.OutputDir.value), 
    help="Directory for output files"
)

args = parser.parse_args()

# Process all .ulg files in input directory
for root, _, files in os.walk(args.input_dir):
    for file in files:
        if file.endswith(".ulg"):
            _, ulg_file_name = os.path.split(file)
            output_folder_path = os.path.join(args.output_dir, ulg_file_name.replace(".ulg", ""))

            os.makedirs(output_folder_path, exist_ok=True)

            full_path = os.path.join(root, file)
            ulog = ULog(full_path)
            parameters = ulog.initial_parameters

            base_file_name = ulg_file_name.replace(".ulg", "")
            param_file = os.path.join(output_folder_path, "param_" + base_file_name + ".param")
            txt_file = os.path.join(output_folder_path, "param_txt_" + base_file_name + ".txt")

            def save_parameters(filepath):
                with open(filepath, "w") as f:
                    f.write("# PX4 parameter file\n")
                    for param, value in parameters.items():
                        f.write(f"{param} {value}\n")
            
            save_parameters(param_file)
            save_parameters(txt_file)

            print(f"Saved parameters to {param_file} and {txt_file}")