#!/bin/bash

# List all packages installed from a particular package source, specified as fully-qualified domain name. Look in
# /var/lib/apt/lists/*_Packages to see what the package source domains are on the system.
fqdn=$1

for pkg in $(dpkg-query --show | awk -F "[ \t:]" '{print $1;}'); do
   if grep -q "Package: $pkg" /var/lib/apt/lists/${fqdn}_*_Packages; then
      echo $pkg
   fi
done
