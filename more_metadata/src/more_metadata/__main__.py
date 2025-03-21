from pyulog.core import ULog
import os
import re
from pathlib import Path
import numpy as np

import logging
from roboto import ActionRuntime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    runtime = ActionRuntime.from_env()

    input_dir = runtime.input_dir
    output_dir = runtime.output_dir
    dataset = runtime.dataset

    if not input_dir:
        error_msg = "Set ROBOTO_INPUT_DIR env variable."
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    for root, dirs, paths in os.walk(input_dir):
        for file in paths:
            # Check if the file ends with .ulg
            if file.endswith(".ulg"):
                _, ulg_file_name = os.path.split(file)

                msg_filter = ["vehicle_air_data"]
                full_path = os.path.join(root, file)
                relative_path = Path(full_path).relative_to(input_dir)
                file_id = dataset.get_file_by_path(relative_path)

                ulog = ULog(full_path, msg_filter, True)

                baro_temp_c = None
                baro_temp_c_max = None
                baro_temp_c_min = None
                baro_temp_c_mean = None

                if any(elem.name == "vehicle_air_data" for elem in ulog.data_list):
                    vehicle_air_data = ulog.get_dataset("vehicle_air_data")
                    baro_temp_c = vehicle_air_data.data["baro_temp_celcius"]
                    baro_temp_c_max = round(float(max(baro_temp_c)),2)
                    baro_temp_c_min = round(float(min(baro_temp_c)),2)
                    baro_temp_c_mean = round(float(np.mean(baro_temp_c)),2)
                    print(baro_temp_c_max, baro_temp_c_min, baro_temp_c_mean)

                    file_id.put_metadata({
                        "max_baro_temp": baro_temp_c_max,
                        "min_baro_temp": baro_temp_c_min,
                        "mean_baro_temp": baro_temp_c_mean,
                        "aircraft_iid": "BB"
                        })
                else:
                    print("no vehicle_air_data topic")

                file_id.put_metadata({"aircraft_sid": "81800"})