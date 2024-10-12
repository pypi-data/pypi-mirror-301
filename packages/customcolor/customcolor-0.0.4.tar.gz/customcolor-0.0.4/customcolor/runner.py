from unittest.runner import TextTestRunner

from .result import ColorTestResult


class ColorTestRunner(TextTestRunner):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)


	def _makeResult(self):
		return ColorTestResult(self.stream, self.descriptions, self.verbosity)
