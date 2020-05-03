#! /usr/bin/env python3

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

print("Manual depended on by something: " + ', '.join(manualDepends))
