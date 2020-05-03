#!/usr/bin/env python3

"""List Debian packages which nothing else depends on

This script can be used to see which packages are "roots" in the conceptual tree where "depends on" relationships flow
from roots to leaves. In general these are likely to be the actual applications that are used and installed by choice,
and they should probably be flagged as manually-installed (see list-manual-packages.py).

This script outputs one package name per line, with the package architecture as a suffix separated by a colon."""

__author__ = "David Osolkowski"
__copyright__ = "Copyright 2020 David Osolkowski"
__license__ = "MIT"
__status__ = "Development"
__version__ = "1.1.0"

from apt import cache

# All installed packages
installed = {
    pkg
    for pkg in cache.Cache()
    if pkg.is_installed
}

installedNames = {pkg.fullname for pkg in installed}

# All installed dependencies of installed packages
installedDependencies = {
    dep_pkg.name + ":" + pkg.architecture()
    for pkg in installed
    for dep in pkg.installed.get_dependencies('PreDepends', 'Depends', 'Recommends')
    for dep_pkg in dep
    if dep_pkg.name + ":" + pkg.architecture() in installedNames
}

# All installed suggestions of installed packages
installedSuggestions = {
    dep_pkg.name + ":" + pkg.architecture()
    for pkg in installed
    for dep in pkg.installed.get_dependencies('Suggests')
    for dep_pkg in dep
    if dep_pkg.name + ":" + pkg.architecture() in installedNames
}

# All installed packages that nothing installed depends on
installedRoots = [
    pkg.fullname + (" (SUGGESTED)" if pkg.name in installedSuggestions else "")
    for pkg in installed
    if pkg.fullname not in installedDependencies
]

installedRoots.sort()

print('\n'.join(installedRoots))
