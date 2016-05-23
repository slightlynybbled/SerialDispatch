from setuptools import setup, find_packages

setup(name='serialdispatch',
      version ='0.12',
      url='https://github.com/slightlynybbled/SerialDispatch',
      description='Easy serial communication using Dispatch',
      author='Jason Jones',
      author_email='slightlynybbled@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['pyserial'],
      zip_safe=False
)