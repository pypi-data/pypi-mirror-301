import sys


_RESET = '\033[0m'


def _set_color(color):
	print(color, end='')


def _reset_color():
	print(_RESET, end='')
	sys.stdout.flush()