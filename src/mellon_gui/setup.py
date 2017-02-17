from setuptools import setup, find_packages
import os

version = '0.0.1'

setup(name='mellon_gui',
      version=version,
      description="Mellon Web Interface.",
      long_description=open("README.md").read() + "\n" +
                       open("HISTORY.txt").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
      ],
      keywords=['zca'],
      author='David Davis',
      author_email='david.davis@crowdstrike.com',
      url='https://github.com/CrowdStrike/mellon',
      download_url = '',
      license='MIT',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=[],
      include_package_data=True,
      package_data = {
          '': ['*.zcml', '*.xml']
        },
      zip_safe=False,
      install_requires=[
          'setuptools',
          'zc.buildout',
          'sparc.configuration',
          'sparc.utils',
          'mellon',
          'mellon_api'
      ],
      tests_require=[
      ],
      entry_points={
          'console_scripts':['mellon_gui=mellon_gui.app:main'],
          'zc.buildout': ['ember = mellon_gui.recipes.ember:Ember']
          },
      )