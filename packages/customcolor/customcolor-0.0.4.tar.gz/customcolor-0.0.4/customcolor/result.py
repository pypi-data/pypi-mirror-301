from unittest.result import TestResult

from .colors import *


class ColorTestResult(TestResult):
	separator1 = '=' * 70
	separator2 = '-' * 70
	tab = ' ' * 2

	colors = {
		'none': print,
		'func': print_yellow,
		'doc': print_cyan,
		'success': print_green,
		'fail': print_red,
		'error': print_red,
		'expected': print_green,
		'unexpected': print_red,
		'skip': print,
	}

	def __init__(self, stream, descriptions, verbosity):
		super(ColorTestResult, self).__init__(stream, descriptions, verbosity)
		self.descriptions = descriptions
		self.showAll = verbosity > 1
		self.dots = verbosity <= 1

	def printDescription(self, test, end=''):
		doc = test.shortDescription()
		if self.descriptions and doc:
			self.colors['func'](test)
			self.colors['doc'](self.tab+doc, end=end)
		else:
			self.colors['func'](test, end=end)


	def startTest(self, test):
		super(ColorTestResult, self).startTest(test)
		if self.showAll:
			self.printDescription(test)
			self.colors['none'](' ... ', end='')


	def printResult(self, short, long, color_key = 'none'):
		color = self.colors[color_key]
		if self.showAll:
			color(long)
		elif self.dots:
			color(short, end='')


	def addSuccess(self, test):
		super().addSuccess(test)
		self.printResult('.', 'OK', 'success')


	def addFailure(self, test, err):
		super().addFailure(test, err)
		self.printResult('F', 'FAIL', 'fail')


	def addError(self, test, err):
		super().addError(test, err)
		self.printResult('E', 'ERROR', 'error')


	def addExpectedFailure(self, test, err):
		super(ColorTestResult, self).addExpectedFailure(test, err)
		self.printResult('x', 'expected failure', 'expected')


	def addUnexpectedSuccess(self, test):
		super(ColorTestResult, self).addUnexpectedSuccess(test)
		self.printResult('u', 'unexpected success', 'unexpected')


	def addSkip(self, test, reason):
		super(ColorTestResult, self).addSkip(test, reason)
		self.printResult('s', 'skipped {0!r}'.format(reason), 'skip')


	def printErrors(self):
		if self.dots or self.showAll:
			self.colors['none']()
		self.printErrorList('ERROR', self.errors, 'error')
		self.printErrorList('FAIL', self.failures, 'fail')
		unexpectedSuccesses = getattr(self, 'unexpectedSuccesses', ())
		if unexpectedSuccesses:
			self.colors['none'](self.separator1, end='\n')
			for test in unexpectedSuccesses:
				self.colors['unexpected']('UNEXPECTED SUCCESS', end='')
				self.colors['none'](': ', end='')
				self.printDescription(test, end='\n')


	def printErrorList(self, flavour, errors, color_key = 'none'):
		for test, err in errors:
			self.colors['none'](self.separator1, end='\n')
			self.colors[color_key](f"{flavour}", end='')
			self.colors['none'](': ', end='')
			self.printDescription(test, end='\n')
			self.colors['none'](self.separator2, end='\n')
			self.colors['none'](err)
