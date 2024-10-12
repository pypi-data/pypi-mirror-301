import sys
import os


if os.name == 'nt':
	from ._win_color_types import TextColor
	from ._win_console_utils import _set_color, _reset_color
else:
	from ._linux_color_types import TextColor
	from ._linux_console_utils import _set_color, _reset_color


def color_print(*values, **kwargs):
	sys.stdout.flush()
	if 'color' in kwargs:
		_set_color(kwargs['color'])
		kwargs.pop('color')
	print(*values, **kwargs)
	sys.stdout.flush()
	_reset_color()


def print_black(*values, **kwargs):
	color_print(*values, color=TextColor.BLACK, **kwargs)


def print_dark_blue(*values, **kwargs):
	color_print(*values, color=TextColor.DARK_BLUE, **kwargs)


def print_dark_green(*values, **kwargs):
	color_print(*values, color=TextColor.DARK_GREEN, **kwargs)


def print_dark_cyan(*values, **kwargs):
	color_print(*values, color=TextColor.DARK_CYAN, **kwargs)


def print_dark_red(*values, **kwargs):
	color_print(*values, color=TextColor.DARK_RED, **kwargs)


def print_dark_magenta(*values, **kwargs):
	color_print(*values, color=TextColor.DARK_MAGENTA, **kwargs)


def print_dark_yellow(*values, **kwargs):
	color_print(*values, color=TextColor.DARK_YELLOW, **kwargs)


def print_light_gray(*values, **kwargs):
	color_print(*values, color=TextColor.LIGHT_GRAY, **kwargs)


def print_gray(*values, **kwargs):
	color_print(*values, color=TextColor.GRAY, **kwargs)


def print_blue(*values, **kwargs):
	color_print(*values, color=TextColor.BLUE, **kwargs)


def print_green(*values, **kwargs):
	color_print(*values, color=TextColor.GREEN, **kwargs)


def print_cyan(*values, **kwargs):
	color_print(*values, color=TextColor.CYAN, **kwargs)


def print_red(*values, **kwargs):
	color_print(*values, color=TextColor.RED, **kwargs)


def print_magenta(*values, **kwargs):
	color_print(*values, color=TextColor.MAGENTA, **kwargs)


def print_yellow(*values, **kwargs):
	color_print(*values, color=TextColor.YELLOW, **kwargs)


def print_white(*values, **kwargs):
	color_print(*values, color=TextColor.WHITE, **kwargs)
