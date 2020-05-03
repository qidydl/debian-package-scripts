#! /usr/bin/env python3

from apt import cache

aptCache = cache.Cache()

# All manually-installed packages
manual = {
    pkg
    for pkg in aptCache
    if pkg.is_installed and not pkg.is_auto_installed
}

# *All* dependencies (manual or otherwise!) of manually-installed packages
depends = {
    dep_pkg.name
    for pkg in manual
    for dep in pkg.installed.get_dependencies('PreDepends', 'Depends')#, 'Recommends')
    for dep_pkg in dep
}

# All manually-installed packages that nothing installed depends on
manualRoots = [
    pkg.name
    for pkg in manual
    if pkg.name not in depends
]

manualRoots.sort()

print('\n'.join(manualRoots))

manualNotRoots = [
    pkg.name
    for pkg in manual
    if pkg.name in depends
]

manualNotRoots.sort()

print("Manual depended on by something: " + ', '.join(manualNotRoots))
