"""Load constants for use the rest of the package."""
import importlib.resources as resources

import yaml

constants_location = resources.files("dkist_processing_pac") / "data" / "constants.yml"
with resources.as_file(constants_location) as p:
    with open(p, "rb") as f:
        CONSTANTS = yaml.safe_load(f)
