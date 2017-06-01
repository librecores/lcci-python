#!/usr/bin/env python

import argparse, logging
from lcci import __version__
from lcci.configuration import Configuration
from lcci.tools import ToolRepository

def agent_list(args):
    conf = Configuration(args)

    for agent in conf.agents:
        print("{}".format(agent))

def agent_start(args):
    conf = Configuration(args)

    try:
        agent = conf.agents[args.agent]
    except KeyError:
        logging.error("Cannot find agent {}".format(args.agent))
        exit(1)

    agent.start(args.no_daemon)

def agent_stop(args):
    conf = Configuration(args)

    try:
        agent = conf.agents[args.agent]
    except KeyError:
        logging.error("Cannot find agent {}".format(args.agent))
        exit(1)

    agent.stop()

def tools_list(args):
    tools = Configuration(args).get_tool_repository()
    for tool in tools.list():
        print("{}".format(tool.name))
        print("  versions:")
        for version in tool.versions:
            release = tool.version_in_release(version)
            if release is None:
                print("    {}".format(version))
            else:
                print("    {} ({})".format(version, release))

def tools_install(args):
    tools = []
    releases = []
    for a in args.tool_or_release:
        if a[0].isdigit():
            releases.append(a)
        else:
            colon = a.find(":")
            if colon < 1:
                logging.error("{} is not a valid tool, <tool>:<version> required".format(a))
            else:
                tool = a[0:colon]
                version = a[colon+1:]
                if len(tool) == 0 or len(version) == 0:
                    logging.error("{} is not a valid tool, <tool>:<version> required".format(a))
                else:
                    tools.append({'name': tool, 'version': version})

    logging.info("Get tool repository")
    if len(releases) == 0:
        # Only catch the required tools
        repo = Configuration(args).get_tool_repository([t['name'] for t in tools])
    else:
        repo = Configuration(args).get_tool_repository()

    known_releases = repo.get_releases()

    for r in releases:
        if r not in known_releases:
            logging.warn("Unknown release: {}".format(r))
        for t in repo.list(r):
            tools.append({'name': t.name, 'version': t.lcci_releases[r]})

    logging.info("Will install the following tools:")
    for t in tools:
        logging.info("  {}:{}".format(t['name'],t['version']))

    for t in tools:
        tool = repo.get_tool(t['name'])
        tool.install(t['version'])

def main():
     logging.basicConfig(level=logging.INFO)

     parser = argparse.ArgumentParser()
     subparsers = parser.add_subparsers()

     parser.add_argument('--version', help='Display the lcci version', action='version', version=__version__)

     # Agent subparser
     parser_agent = subparsers.add_parser('agent', help='Agent functions')
     subparsers_agent = parser_agent.add_subparsers()

     # Agent 'list' subsubparser
     parser_agent_list = subparsers_agent.add_parser('list', help='List agents')
     parser_agent_list.set_defaults(func=agent_list)

     # Agent 'start' subsubparser
     parser_agent_start = subparsers_agent.add_parser('start', help='Start agent')
     parser_agent_start.add_argument("agent")
     parser_agent_start.add_argument("--no-daemon", action='store_true')
     parser_agent_start.set_defaults(func=agent_start)

     # Agent 'stop' subsubparser
     parser_agent_start = subparsers_agent.add_parser('stop', help='Stop agent')
     parser_agent_start.add_argument("agent")
     parser_agent_start.set_defaults(func=agent_stop)

     # Tools subparser
     parser_tools = subparsers.add_parser('tools', help='Tool functions')
     subparsers_tools = parser_tools.add_subparsers()

     # Tools 'list' subsubparser
     parser_tools_list = subparsers_tools.add_parser('list', help='List tools')
     parser_tools_list.add_argument("--releases", action='store_true')
     parser_tools_list.set_defaults(func=tools_list)

     # Tools 'install' subsubparser
     parser_tools_install = subparsers_tools.add_parser('install', help='Install tools')
     parser_tools_install.add_argument('tool_or_release', nargs=argparse.REMAINDER)
     parser_tools_install.set_defaults(func=tools_install)

     parsed_args = parser.parse_args()
     if hasattr(parsed_args, 'func'):
         parsed_args.func(parsed_args)
     else:
         parser.print_help()

if __name__ == "__main__":
    main()
