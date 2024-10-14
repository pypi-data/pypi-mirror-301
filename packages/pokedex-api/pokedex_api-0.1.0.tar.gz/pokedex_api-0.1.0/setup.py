from setuptools import setup, find_packages

setup(
    name='pokedex-api',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    description='A simple API wrapper for accessing Pokémon information.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Andrew Muratov',
    author_email='andrewamuratov@gmail.com',
    url='https://github.com/AndrewAMur/pokedex-api',
    license='MIT',
)
