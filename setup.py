from setuptools import setup, find_packages

setup(name='serialdispatch',
      version ='0.13',
      url='https://github.com/slightlynybbled/SerialDispatch',
      description='Easy serial communication using Dispatch',
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
      install_requires=['pyserial'],
      zip_safe=False
)