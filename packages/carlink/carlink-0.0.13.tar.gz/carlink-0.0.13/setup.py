import codecs
import os
import re
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
  """Taken from pypa pip setup.py:
  intentionally *not* adding an encoding option to open, See:
  https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
  """
  return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
  version_file = read(*file_paths)
  version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                            version_file, re.M)
  if version_match:
    return version_match.group(1)
  raise RuntimeError("Unable to find version string.")

setup(
  name='carlink',
  version=find_version("python", "__init__.py"),
  url='https://github.com/deeeepc/carlink',
  author='deep C',
  author_email='',
  packages=[
    'link',
  ],
  package_dir={'link': 'python'},
  platforms='any',
  license='MIT',
  install_requires=[
    'libusb1 == 2.0.1',
    'hexdump >= 3.3',
    'pycryptodome >= 3.9.8',
    'tqdm >= 4.14.0',
    'requests'
  ],
  ext_modules=[],
  description="carlink is a library to interact with your car",
  long_description='See https://github.com/deeeepc/carlink',
  classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    "Natural Language :: English",
    "Programming Language :: Python :: 3",
    "Topic :: System :: Hardware",
  ],
)