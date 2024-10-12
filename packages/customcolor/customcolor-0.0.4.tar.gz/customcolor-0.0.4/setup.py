from setuptools import setup, find_packages


setup(
	name='customcolor',
	version='0.0.4',
	description='Library for colored output of unit tests in the console',
	long_description=open('README.md', encoding="utf-8").read(),
	long_description_content_type='text/markdown',
	author='Kirill',
	author_email='gimpelcomp@gmail.com',
	url='https://github.com/gimpelgit/customcolor/',
	packages=find_packages(),
	install_requires=[],
	python_requires='>=3.6',
	license='MIT',
	keywords='unittest colour color output print windows linux text-decoration',
	classifiers=[
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.6',
	]
)