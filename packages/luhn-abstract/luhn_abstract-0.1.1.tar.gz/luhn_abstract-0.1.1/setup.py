from setuptools import setup,find_packages

setup(
	name='luhn_abstract',
	version='0.1.1',
	author='',
	author_email='',
	url='https://github.com/JIVJGFJZKF/luhn',
	description='A library for automatically generating an abstract from a document using unsupervised techniques.',
	long_description=open('README.txt').read(),
	long_description_content_type='text/markdown',
	packages=find_packages(),
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
		'Operating System :: OS Independent',
	],
	python_requires='>=3.6',
)