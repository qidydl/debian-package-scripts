#! /usr/bin/env python3

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
