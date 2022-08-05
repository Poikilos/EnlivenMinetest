#!/usr/bin/env python
import setuptools
import sys
import os
# - For the example on which this was based, see
#   https://github.com/poikilos/linux-preinstall/blob/main/setup.py
#   which is based on
#   https://github.com/poikilos/world_clock/blob/main/setup.py
#   which is based on
#   https://github.com/poikilos/nopackage/blob/main/setup.py
#   which is based on
#   https://github.com/poikilos/pypicolcd/blob/master/setup.py
# - For nose, see https://github.com/poikilos/mgep/blob/master/setup.py

# python_mr = sys.version_info.major
# versionedModule = {}
# versionedModule['urllib'] = 'urllib'
# if python_mr == 2:
#     versionedModule['urllib'] = 'urllib2'

install_requires = []

if os.path.isfile("requirements.txt"):
    with open("requirements.txt", "r") as ins:
        for rawL in ins:
            line = rawL.strip()
            if len(line) < 1:
                continue
            install_requires.append(line)

description = (
    "Manage Minetest using Python."
)
long_description = description
if os.path.isfile("readme.md"):
    with open("readme.md", "r") as fh:
        long_description = fh.read()

setuptools.setup(
    name='pyenliven',
    version='0.3.0',
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        ('License :: OSI Approved ::'
         ' GNU General Public License v2 or later (GPLv2+)'),
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development :: Version Control',
        'Topic :: System :: Installation/Setup',
    ],
    keywords=('minetest repo management commit data analyzer'
              ' meld merge compare files diff'),
    url="https://github.com/poikilos/EnlivenMinetest",
    author="Jake Gustafson",
    author_email='7557867+poikilos@users.noreply.github.com',
    license='GPLv2.1',
    # packages=setuptools.find_packages(),
    packages=['pyenliven'],
    # include_package_data=True,  # look for MANIFEST.in
    # scripts=['example'] ,
    # See <https://stackoverflow.com/questions/27784271/
    # how-can-i-use-setuptools-to-generate-a-console-scripts-entry-
    # point-which-calls>
    entry_points={
        'console_scripts': [
            'compatiblizemod=pyenliven.compatiblizemod:main',
        ],
    },
    install_requires=install_requires,
    #     versionedModule['urllib'],
    # ^ "ERROR: Could not find a version that satisfies the requirement
    #   urllib (from nopackage) (from versions: none)
    #   ERROR: No matching distribution found for urllib"
    test_suite='nose.collector',
    tests_require=['nose', 'nose-cover3'],
    zip_safe=False,  # It can't run zipped due to needing data files.
 )
