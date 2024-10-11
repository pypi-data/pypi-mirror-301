from setuptools import setup, find_packages
import os
def package_files(directory):
	paths = []
	for (path, directories, filenames) in os.walk(directory):
		for filename in filenames:
			paths.append(os.path.relpath(os.path.join(path, filename), directory))
	return paths


binary_files = package_files('src/gpt4all-pypi-part_007/input')

setup(
	name='gpt4all-pypi-part_007',
	version='0.0.1',
	description='Package with binary files and subfolders',
	packages=find_packages(where='src'),
	package_dir={'': 'src'},
	package_data = {
		'gpt4all-pypi-part_007': binary_files,
	},
	include_package_data=True,
	install_requires=['gpt4all-pypi-part_006==0.0.1', ],
)
