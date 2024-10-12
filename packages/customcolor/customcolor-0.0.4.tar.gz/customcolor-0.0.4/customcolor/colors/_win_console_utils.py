import ctypes


class _Coord(ctypes.Structure):
	_fields_ = [
		("X", ctypes.c_short),
		("Y", ctypes.c_short)
	]


class _SmallRect(ctypes.Structure):
	_fields_ = [
		("Left", ctypes.c_short),
		("Top", ctypes.c_short),
		("Right", ctypes.c_short),
		("Bottom", ctypes.c_short)
	]


class _ConsoleScreenBufferInfo(ctypes.Structure):
	_fields_ = [
		("dwSize", _Coord),
		("dwCursorPosition", _Coord),
		("wAttributes", ctypes.c_ushort),
		("srWindow", _SmallRect),
		("dwMaximumWindowSize", _Coord)
	]


_hConsole = ctypes.windll.kernel32.GetStdHandle(ctypes.c_uint(-11))
_original_attributes = None


def _set_color(color):
	global _original_attributes
	csbi = _ConsoleScreenBufferInfo()
	ctypes.windll.kernel32.GetConsoleScreenBufferInfo(_hConsole, ctypes.byref(csbi))
	_original_attributes = csbi.wAttributes
	background_color = _original_attributes & 0xF0
	new_color = color | background_color
	ctypes.windll.kernel32.SetConsoleTextAttribute(_hConsole, new_color)


def _reset_color():
	if _original_attributes is not None:
		ctypes.windll.kernel32.SetConsoleTextAttribute(_hConsole, _original_attributes)
