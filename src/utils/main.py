from utils.utils import *

json_path = "json_dir/operations.json"
json_full = read_json(json_path)
parse_data(json_full)
print(*result_output(output_last_five(json_full)), sep="\n\n")
