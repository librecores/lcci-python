from github import Github
import docker, logging

class Tool:
    name = None
    versions = {}
    lcci_releases = {}
    basepath = None

    def __init__(self, name, basepath):
        self.name = name
        self.versions = {}
        self.lcci_releases = {}
        self.basepath = basepath

    def version_in_release(self, version):
        for r, v in self.lcci_releases.items():
            if v == version:
                return r
        return None

    def install(self, version):
        logging.info("Install {}:{}".format(self.name, version))
        client = docker.from_env(version='auto')
        logging.info("Pull the image")

        image = "lccitools/{}:{}".format(self.name, version)

        try:
            client.images.pull(image)
        except docker.errors.ImageNotFound:
            logging.error("Cannot find image {}".format(image))
            exit(1)

        logging.info("Start the installation")

        client.containers.run(
            image,
            detach = False,
            volumes = { self.basepath: { "bind": "/tools", "mode": "rw"} }
        )

        logging.info("Done")

class ToolRepository:
    gh = None
    tools = []
    path = None

    def __init__(self, token, path, filter):
        self.gh = Github(login_or_token=token)
        self.path = path
        self.releases = []
        org = self.gh.get_organization("lccitools")
        for repo in org.get_repos():
            if repo.full_name != "lccitools/base":
                tool = repo.full_name[10:]
                if filter is not None and tool not in filter:
                    continue

                t = Tool(tool, path)
                tags = repo.get_tags()
                for tag in tags:
                    if not tag.name.startswith("lcci-"):
                        t.versions[tag.name] = tag.commit.sha

                for tag in tags:
                    if tag.name.startswith("lcci-"):
                        lccitag = tag.name[5:]
                        version = None
                        for v, c in t.versions.items():
                            if c == tag.commit.sha:
                                version = v
                                break

                        if version is not None:
                            t.lcci_releases[lccitag] = version
                            if lccitag not in self.releases:
                                self.releases.append(lccitag)

                self.tools.append(t)

    def list(self, release = None):
        tools = self.tools

        if release is not None:
            tools = []
            for t in self.tools:
                if release in t.lcci_releases:
                    tools.append(t)

        return tools

    def get_tool(self, name):
        for t in self.tools:
            if t.name == name:
                return t
        return None

    def get_releases(self):
        return self.releases
