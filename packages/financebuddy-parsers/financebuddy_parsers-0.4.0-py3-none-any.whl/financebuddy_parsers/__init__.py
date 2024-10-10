# stdlib
import os

__DIR_CURRENT = os.path.dirname(__file__)

# config files
DIR_CONFIGS = os.path.join(__DIR_CURRENT, "configs")
MAP_CONFIG_FILES: dict[tuple[str, str], str] = {}
for basename in os.listdir(DIR_CONFIGS):
    filename, _ = os.path.splitext(basename)
    sub = filename.replace("parser_", "")
    sub = sub.replace("_config", "")
    parts = sub.split("_")
    format, extension = parts[0], parts[1]
    key = (format, extension)
    path = os.path.join(DIR_CONFIGS, basename)
    MAP_CONFIG_FILES[key] = path

PARSER_CONFIGS = list(MAP_CONFIG_FILES.values())
PARSER_CONFIGS.sort()

# sample files
DIR_SAMPLES = os.path.join(__DIR_CURRENT, "samples")
MAP_SAMPLE_FILES: dict[tuple[str, str], list[str]] = {}
for basename in os.listdir(DIR_SAMPLES):
    filename, _ = os.path.splitext(basename)
    sub = filename.replace("sample_", "")
    parts = sub.split("_")
    format, extension = parts[0], parts[1]

    key = (format, extension)
    path = os.path.join(DIR_SAMPLES, basename)
    MAP_SAMPLE_FILES.setdefault(key, []).append(path)
