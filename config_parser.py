# coding=utf-8
import types


class ConfigParser(dict):
    """
    CFG 配置文件解析器, 用来解析 .cfg 配置
    """
    def __init__(self, path):
        self.path = path
        super(dict, self).__init__()

        d = types.ModuleType('config')
        d.__file__ = self.path
        try:
            with open(self.path) as config_file:
                exec(compile(config_file.read(), self.path, 'exec'), d.__dict__)
        except IOError as e:
            raise e

        for key in dir(d):
            if key.isupper():
                self[key] = getattr(d, key)