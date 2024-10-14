from setuptools import setup, find_packages
 
setup(
    include_package_data=True,
	name="vcipher",
	version="1.0.0",
	packages=find_packages(),
	description="(De)cryption software. Allows you to encrypt or decrypt data based on a 128 bits encryption key.",
	url="https://github.com/Lou-du-Poitou/vcipher",
	author="V / Lou du Poitou",
	license="MIT",
	python_requires=">=3.9.7"
)