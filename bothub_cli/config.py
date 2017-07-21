# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function, unicode_literals)

import os
import codecs

import yaml
from bothub_cli import exceptions as exc

from six.moves.configparser import ConfigParser


class Config(object):
    path = None

    def __init__(self, path=None):
        self.config = {}
        self.path = Config.determine_path(path)

    @staticmethod
    def determine_path(path):
        # if path is not list, make sure parent dir exists and return
        if isinstance(path, str):
            Config.make_parent_dir(path)
            return path

        # if path is list or tuple, iterate to lookup existing path,
        # if not found, try to make empty one with first entry
        if isinstance(path, (list, tuple)):
            for path_candidate in path:
                if os.path.isfile(path_candidate):
                    return path_candidate

            non_exists_path = path[0]
            Config.make_parent_dir(non_exists_path)
            return non_exists_path

    @staticmethod
    def make_parent_dir(path):
        parent_dir = os.path.dirname(path)
        if len(parent_dir) > 0 and not os.path.isdir(parent_dir):
            os.makedirs(parent_dir)

    def load(self):
        try:
            with open(self.path) as fin:
                self.config = yaml.load(fin)
        except IOError:
            raise exc.ImproperlyConfigured()

    def save(self):
        with codecs.open(self.path, 'wb', encoding='utf8') as fout:
            content = yaml.dump(self.config, default_flow_style=False)
            fout.write(content)

    def set(self, key, value):
        self.config[key] = value

    def get(self, key):
        return self.config.get(key)


class ProjectConfig(Config):
    def __init__(self, path=('bothub.yml', 'bothub.yaml')):
        super(ProjectConfig, self).__init__(path)
