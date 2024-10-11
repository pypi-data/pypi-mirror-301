from setuptools import setup

setup(
    name='subenum',
    version='1.2',
    packages=['subenum'],
    package_dir={'subenum': '.'},
    py_modules=['subenum'],
    entry_points={
        'console_scripts': [
            'subenum = subenum:main',
        ]
    },
    author='Mathias Bochet (aka Zen)',
    description='A tool to find subdomains passively',
    long_description="subenum is a tool designed to enumerate subdomains using search engines, websites and apis.",
    url='https://github.com/42zen/subenum',
    install_requires=[
        'requests',
        'beautifulsoup4',
        'fake-useragent',
        'python-dotenv',
    ],
)