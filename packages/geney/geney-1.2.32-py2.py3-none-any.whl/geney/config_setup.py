import os
import json
from pathlib import Path

def get_config():
    config_file = os.path.join(os.path.expanduser('~'), '.oncosplice_setup_1_2', 'config.json')
    if Path(config_file).exists():
        config_setup = {k: {k_in: Path(p_in) for k_in, p_in in p.items()} for k, p in json.loads(open(config_file).read()).items()}

    else:
        print("Database not set up.")
        config_setup = {}

    return config_setup