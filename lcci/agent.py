import logging

import docker, requests

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
        for bind in volumes:
            local = volumes[bind]
            self.volumes[local] = {'bind': bind, 'mode': 'rw'}

    def start(self,no_daemon=False):
        logging.info("Start agent {}".format(self.name))
        client = docker.from_env(version='auto')
        logging.info("Pull the image")
        try:
            client.images.pull("librecores/ci-{}-agent".format(self.type))
        except docker.errors.ImageNotFound:
            logging.error("Cannot find image, invalid type set in configuration")
            exit(1)

        env = { "AGENT_ID": self.id, "AGENT_SECRET": self.secret }

        try:
            cont = client.containers.get("lcci-{}".format(self.name))
            logging.warn("Container already/yet exists")
            self.stop()
        except docker.errors.NotFound:
            pass

        logging.info("Start the container")

        client.containers.run(
            "librecores/ci-{}-agent".format(self.type),
            name = "lcci-{}".format(self.name),
            devices = self.devices,
            environment = env,
            detach = not no_daemon,
            volumes = self.volumes
        )

    def stop(self):
        logging.info("Stop agent {}".format(self.name))

        client = docker.from_env(version='auto')

        try:
            cont = client.containers.get("lcci-{}".format(self.name))
        except:
            logging.error("Cannot find container")
            exit(1)

        try:
            cont.stop()
        except docker.errors.APIError as e:
            if (e.status_code() == 137):
                logging.error("Container cannot be stopped" + e)
                exit(1)
        except requests.exceptions.ReadTimeout:
            cont.kill()

        try:
            cont.remove()
        except docker.errors.APIError as e:
            logging.error("Container cannot be removed")
            exit(1)
