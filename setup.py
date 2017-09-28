from setuptools import setup, find_packages
import os

# ---------------------------------
# imports the version from the package
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'readme.md')) as f:
    README = f.read()
exec(open(os.path.join(here, 'serialdispatch/version.py')).read())

setup(name='serialdispatch',
      version=__version__,
      url='https://github.com/slightlynybbled/SerialDispatch',
      description='Easy serial communication using Dispatch',
      long_description=README,
      author='Jason Jones',
      author_email='slightlynybbled@gmail.com',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Topic :: System :: Hardware',
          'Topic :: System :: Monitoring',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: 3.1',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5'
      ],
      license='MIT',
      packages=find_packages(),
      install_requires=['pyserial >= 3.4'],
      zip_safe=False
)