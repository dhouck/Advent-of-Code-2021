import argparse
import functools
import logging
import sys

try:
	import coloredlogs
	@functools.wraps(coloredlogs.install)
	def configLogging(*args, format=None, **kwargs):
		kwargs['fmt'] = format
		coloredlogs.install(*args, **kwargs)
except ImportError:
	configLogging = logging.basicConfig


@functools.wraps(argparse.ArgumentParser)
def get_argparser(*args, **kwargs):
	parser = argparse.ArgumentParser(*args, **kwargs)
	add_default_arguments(parser)
	return parser


def add_default_arguments(argparser):
	argparser.add_argument('input', type=argparse.FileType('r'), default=sys.stdin)
	log_group = argparser.add_mutually_exclusive_group()
	log_group.add_argument('-v', '--verbose', action='count', default=0)
	log_group.add_argument('-q', '--quiet', action='count', default=0)
	log_group.add_argument('--log-level', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
	                       default='INFO')


def parse_args(parser):
	args = parser.parse_args()
	set_up_logging(args)
	return args


class Indenter(logging.Filter):
	__slots__ = 'level'
	
	def __init__(self):
		super().__init__()
		self.level = 0
	
	def __str__(self):
		return '│ '*(self.level-1) + ('├╴' if self.level else '')
	
	def __enter__(self):
		self.level += 1
	
	def __exit__(self, *_):
		self.level -= 1
	
	def filter(self, record):
		record.indent = str(self)
		record.indent_level = self.level
		return True


indent = Indenter()


def set_up_logging(args):
	new_level = logging.getLevelName(args.log_level) - 10*args.verbose + 10*args.quiet
	new_level = max(min(new_level, logging.CRITICAL + 10), 0)
	configLogging(style='{', format='{levelname}: {indent}{message}', level=new_level)
	logging.getLogger().addFilter(indent)
