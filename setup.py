try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_description = '''
Python implementation of RakNet 3.25. This is not aimed to be a complete port of RakNet,
just everything that's needed to run a server.
'''

setup(name='Pyraknet',
      description='Python implementation of RakNet 3.25.',
      long_description=long_description,
      license='Apache 2.0',
      version='1.0.0',
      author='Caleb Marshall',
      author_email='anythingtechpro@gmail.com',
      maintainer='Caleb Marshall',
      maintainer_email='anythingtechpro@gmail.com',
      url='https://github.com/AnythingTechPro/pyraknet',
      packages=['pyraknet'],
      classifiers=[
          'Programming Language :: Python :: 3',
      ])
