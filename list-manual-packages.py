#!/usr/bin/env python3

"""List manually-installed Debian packages

This script can be used to see which packages are flagged as having been installed manually. Manually-installed
packages are not eligible for autoremove. Managing this flag will ensure that libraries are cleaned up when no longer
needed.

This script outputs two parts: first, a list of one package name per line for packages that are manually-installed and
also a "root" (see list-root-packages.py). Second, a single big line listing packages that are manually-installed but
not a "root". This output is not designed or intended to be machine-readable; this script is just a heuristic, it does
not even attempt to be bulletproof."""

__author__ = "David Osolkowski"
__copyright__ = "Copyright 2020 David Osolkowski"
__license__ = "MIT"
__status__ = "Development"
__version__ = "1.1.0"

from apt import cache

aptCache = cache.Cache()

# All installed packages
installed = {
    pkg
    for pkg in aptCache
    if pkg.is_installed
}

installedNames = {pkg.name for pkg in installed}

# All installed dependencies of installed packages
depends = {
    dep_pkg.name
    for pkg in installed
    for dep in pkg.installed.get_dependencies('PreDepends', 'Depends', 'Recommends')
    for dep_pkg in dep
    if dep_pkg.name in installedNames
}

# All installed suggestions of installed packages
suggests = {
    dep_pkg.name
    for pkg in installed
    for dep in pkg.installed.get_dependencies('Suggests')
    for dep_pkg in dep
    if dep_pkg.name in installedNames
}

# All manually-installed packages that nothing installed depends on
manualRoots = [
    pkg.name + (" (SUGGESTED)" if pkg.name in suggests else "")
    for pkg in installed
    if not pkg.is_auto_installed and pkg.name not in depends
]

manualRoots.sort()

print('\n'.join(manualRoots))

manualDepends = [
    pkg.name
    for pkg in installed
    if not pkg.is_auto_installed and pkg.name in depends
]

manualDepends.sort()

print("\nManual depended on by something: " + ', '.join(manualDepends))
