Make line-wise union, intersection, difference, or Cartesian product of files
and print it to stdout.

Example
=======

Users who don't have ``/bin/bash`` as their terminal (``grep -v`` simulation)::

    $ grep "/bin/bash" /etc/passwd | setop -d /etc/passwd - | cut -d: -f1

This is equivalent to::

    $ grep -v "/bin/bash" /etc/passwd | sort | cut -d: -f1

