
from tinigine.utils.config import ConfigManager

mod_conf = ConfigManager(mod_name='data_from_tushare')


def load():
    from .mod import DataFromTushare
    mod_instance = DataFromTushare()
    return mod_instance


