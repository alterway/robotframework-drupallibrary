# -*- coding: utf-8 -*-
"""\
============================
robotframework-drupallibrary
============================

RobotFramework keywords and utilities for Drupal testings
"""

# FIXME: Please read http://pythonhosted.org/setuptools/setuptools.html to
#        customize in depth your setup script

from setuptools import setup, find_packages
import os, sys

version = '1.0.0a1'

this_directory = os.path.abspath(os.path.dirname(__file__))

def read(*names):
    fpath = os.path.join(this_directory, *names)
    if not os.path.isfile(fpath):
        # Sphinx docs are not in sdist
        return ''
    return open(fpath, 'r').read().strip()

long_description = '\n\n'.join(
    [read(*paths) for paths in (('README.rst',),
                               ('docs', 'contributors.rst'),
                               ('docs', 'changes.rst'))]
    )
dev_require = ['Sphinx', 'sphinxcontrib-robotdoc']
if sys.version_info < (2, 7):
    dev_require += ['unittest2']

try:
    from sphinx.setup_command import BuildDoc
except ImportError:
    # We won't have it
    class BuildDoc(object):
        def run(self):
            print "Sphinx is not installed here"
            print "Please run \"pip install robotframework-drupallibrary[dev]\" first"


class CustomSphinxBuilder(BuildDoc):
    """Customized command for build_sphinx
    """
    def run(self):
        # We need to create some assets in the source tree first...
        from robot.libdoc import libdoc
        out_file = os.path.join(self.source_dir, 'robot-doc.html')
        libdoc('DrupalLibrary::None', out_file)
        # ... before running the regular Sphinx builder
        BuildDoc.run(self)


setup(name='robotframework-drupallibrary',
      version=version,
      description="robotframework keywords and utilities for Drupal testings",
      long_description=long_description,
      classifiers=[
          "Programming Language :: Python",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Topic :: Software Development :: Testing",
          "Development Status :: 3 - Alpha",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7"
          ],
      keywords='robotframework drupal',
      author='Gilles Lenfant',
      author_email='gilles.lenfant@gmail.com',
      url='https://github.com/alterway/robotframework-drupallibrary',
      license='GPLv3',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'robotframework-selenium2library',
          'lxml'
          ],
      entry_points={
          },
      tests_require=dev_require,
      test_suite='tests.all_tests',
      extras_require={
          'dev': dev_require
      },
      cmdclass={
          'build_sphinx': CustomSphinxBuilder
      }
      )
