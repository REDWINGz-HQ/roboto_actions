from pyulog.core import ULog
import os
import re
from pathlib import Path

import logging
from roboto import ActionRuntime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    runtime = ActionRuntime.from_env()
    # runtime = ActionRuntime(
    # dataset_id="ds_XXXXXXXXXXXX",
    # input_dir=Path("/path/to/local/input/dir"),
    # invocation_id="iv_XXXXXXXXXXXX",
    # org_id="og_XXXXXXXXXXXX",
    # output_dir=Path("/path/to/local/output/dir"),
    # )

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

                msg_filter = []
                full_path = os.path.join(root, file)
                relative_path = Path(full_path).relative_to(input_dir)
                file_id = dataset.get_file_by_path(relative_path)

                ulog = ULog(full_path, msg_filter, True)
                file_put_tags = list()
                error_log_num = 0
                warning_log_num = 0
                for m in ulog.logged_messages:
                    print(m.log_level_str() + " " + m.message)
                    if m.log_level_str() == "ERROR":
                        error_log_num = error_log_num + 1
                        if "ERROR" not in file_put_tags:
                            file_put_tags.append("ERROR")

                    elif m.log_level_str() == "WARNING":
                        warning_log_num = warning_log_num + 1
                        if "WARNING" not in file_put_tags:
                            file_put_tags.append("WARNING")
                file_id.put_tags(tags=file_put_tags)
                file_id.put_metadata({"error logs": error_log_num})
                file_id.put_metadata({"warning logs": warning_log_num})