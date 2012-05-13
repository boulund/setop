Make line-wise union, intersection, difference, or Cartesian product of files
and print it to ``stdout``. Both set and multiset modes are available. This
little program was inspired by Matthew Might's article on `Relational Shell
Programming <http://matt.might.net/articles/sql-in-the-shell/>`_.

If you happen to find a bug, or have an idea for SetOp feature, feel free to let
me know via `GitHub <https://github.com/tigr42/setop>`_ or e-mail.

Example
=======

Users who don't have ``/bin/bash`` as their terminal (``grep -v`` simulation)::

    $ grep "/bin/bash" /etc/passwd | setop -d /etc/passwd - | cut -d: -f1

This is equivalent to::

    $ grep -v "/bin/bash" /etc/passwd | sort | cut -d: -f1

Reference
=========

General syntax is: ``setop operation [options] file [file ...]``

::

	setop -u --union
	      -i --intersection
	      -d --difference
	      -p --product [-D delimiter] <--- default delimiter: TAB
	
	      -m --multiset (-u | -i | -d | -p | -s --sum) <--- enable multiset mode
	
	      -n --newlines (windows | unix) <--- defaults to current OS
	      
	      -h --help
	      -v --version

License
=======

::

	# Copyright (c) 2012 Tigr <tigr42@centrum.cz>
	# All rights reserved.
	#
	# Redistribution and use in source and binary forms, with or without
	# modification, are permitted provided that the following conditions
	# are met:
	# 1. Redistributions of source code must retain the above copyright
	#    notice, this list of conditions and the following disclaimer.
	# 2. Redistributions in binary form must reproduce the above copyright
	#    notice, this list of conditions and the following disclaimer in the
	#    documentation and/or other materials provided with the distribution.
	#
	# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER ``AS IS'' AND ANY EXPRESS
	# OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
	# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
	# IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY DIRECT, INDIRECT,
	# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
	# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
	# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
	# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
	# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
	# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Changelog
=========

- v0.2 (2012-05-13): add ``--multiset`` mode
- v0.1 (2012-04-14): initial release
