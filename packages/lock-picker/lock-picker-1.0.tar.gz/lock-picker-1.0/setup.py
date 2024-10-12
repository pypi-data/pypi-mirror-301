from setuptools import setup

setup(
    name='lock-picker',
    version='1.0',
    packages=['lock_picker'],
    package_dir={'lock_picker': '.'},
    py_modules=['lock_picker'],
    entry_points={
        'console_scripts': [
            'lock-picker = lock_picker:main',
        ]
    },
    author='Mathias Bochet (aka Zen)',
    description='A tool to find api keys from Github',
    long_description="lock-picker is a tool designed to find api keys from an environment variable.",
    url='https://github.com/42zen/lock-picker',
    install_requires=[
        'requests',
        'python-dotenv',
    ],
)