from setuptools import setup

setup(
    name='reinforcement_learning_trader',
    version='1.0',
    packages=['src', 'src.generator', 'trader', 'trader.generators'],
    url='',
    license='Apache 2.0',
    author='Shamanou van Leeuwen',
    author_email='mandarijnopw8@gmail.com',
    description=''
)

install_requires = [
    'cssselect',
    'lxml'
    'psycopg2',
    'requests',
    'numpy',
    'keras'
    'tgym'
]
