import yaml
from lcci.agent import Agent

class Configuration(object):
    """docstring for Configuration"""
    def __init__(self, args):
        self.args = args
        self.volumes = {}
        self.agents = {}

        with open("lcci.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)

        if 'volumes' in cfg:
            self.volumes = cfg['volumes']

        if 'agents' in cfg:
            for name in cfg['agents']:
                config = cfg['agents'][name]
                agent = Agent(name, config)
                self.agents[name] = agent
