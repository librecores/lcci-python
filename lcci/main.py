#!/usr/bin/env python

import argparse, logging
from lcci import __version__
from lcci.configuration import Configuration

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

    agent.start()

def main():
     logging.basicConfig(level=logging.INFO)

     parser = argparse.ArgumentParser()
     subparsers = parser.add_subparsers()

     parser.add_argument('--version', help='Display the FuseSoC version', action='version', version=__version__)

     # Agent subparser
     parser_agent = subparsers.add_parser('agent', help='Agent functions')
     subparsers_agent = parser_agent.add_subparsers()

     # Agent 'list' subsubparser
     parser_agent_list = subparsers_agent.add_parser('list', help='List agents')
     parser_agent_list.set_defaults(func=agent_list)

     # Agent 'start' subsubparser
     parser_agent_start = subparsers_agent.add_parser('start', help='Start agent')
     parser_agent_start.add_argument("agent")
     parser_agent_start.set_defaults(func=agent_start)

     parsed_args = parser.parse_args()
     if hasattr(parsed_args, 'func'):
         parsed_args.func(parsed_args)
     else:
         parser.print_help()

if __name__ == "__main__":
    main()
