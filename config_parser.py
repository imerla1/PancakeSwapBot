from fileinput import filename
import os
import yaml


class YamlConfigParser(object):
    def __init__(self, filename, logger) -> None:
        self.logger = logger
        self.filename = filename

    def load_config(self):
        logger = self.logger
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, self.filename)
        try:
            logger.debug(f"Trying to parse config File, Path={file_path}")
            with open(file_path, "r") as config_file:
                data = yaml.safe_load(config_file)
                logger.debug("Config parsed succesfully.")

            return data

        except FileNotFoundError:
            logger.critical(
                f"{self.filename} doesn't exist on this, directory please check filename or directory")

if __name__ == "__main__":
    from utils.logger import setup_logger
    debug_logger = setup_logger("debug_logger", "debug.log")
    _file = "config.yaml"
    config_object = YamlConfigParser(
        _file, debug_logger
    )
    data = config_object.load_config()