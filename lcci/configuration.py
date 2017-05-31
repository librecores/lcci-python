import yaml
from lcci.agent import Agent
from lcci.tools import ToolRepository

class Configuration(object):
    """docstring for Configuration"""
    def __init__(self, args):
        self.args = args
        self.volumes = {}
        self.agents = {}
        self.githubapitoken = None

        candidates = ["lcci.yml", "/etc/lcci.yml"]

        for file in candidates:
            try:
                self.read_file(file)
                break
            except FileNotFoundError:
                pass

    def read_file(self, file):
        with open(file, 'r') as ymlfile:
            cfg = yaml.load(ymlfile)

        if 'volumes' in cfg:
            self.volumes = cfg['volumes']

        if 'agents' in cfg:
            for name in cfg['agents']:
                config = cfg['agents'][name]
                agent = Agent(name, config, self.volumes)
                self.agents[name] = agent

        if 'main' in cfg:
            if 'github-api-token' in cfg['main']:
                self.githubapitoken = cfg['main']['github-api-token']

    def get_tool_repository(self, filter = None):
        return ToolRepository(self.githubapitoken, self.volumes['/tools'], filter)
