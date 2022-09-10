from glob import glob
from distutils.core import setup

package_name = 'superfences_examples'

setup(
    name=package_name,
    version='0.1.0',
    install_requires=['pymdown-extensions'],
    packages=[package_name],
)
