from setuptools import setup


setup(name='puffin',
      version='0.3.0',
      description='Python replacement for awk',
      url='http://github.com/kespindler/puffin',
      author='Kurt Spindler',
      author_email='kespindler@gmail.com',
      license='MIT',
      packages=['puf'],
      zip_safe=False,
      entry_points={
          'console_scripts': [
              'puf=puf.cli:main',
          ],
      },
)
