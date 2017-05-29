import logging

import docker

class Agent(object):
    """docstring for Agent."""
    def __init__(self, name, config, volumes = {}):
        super(Agent, self).__init__()
        self.name = name
        self.type = config["type"] if "type" in config else "modules"
        self.id = config["agent-id"] if "agent-id" in config else ""
        self.secret = config["agent-secret"] if "agent-secret" in config else ""
        self.devices = config["devices"] if "devices" in config else []

        self.volumes = {}
        for v in volumes:
            self.volumes[v] = {'bind': volumes[v], 'mode': 'rw'}

    def start(self,no_daemon=False):
        logging.info("Start agent {}".format(self.name))
        client = docker.from_env(version='auto')
        logging.info("Pull the image")
        try:
            client.images.pull("librecores/ci-{}".format(self.type))
        except docker.errors.ImageNotFound:
            logging.error("Cannot find image, invalid type set in configuration")

        env = { "AGENT_ID": self.id, "AGENT_SECRET": self.secret }

        client.containers.run(
            "librecores/ci-{}".format(self.type),
            devices = self.devices,
            environment = env,
            detach = not no_daemon,
            volumes = self.volumes
        )
