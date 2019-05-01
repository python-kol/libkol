pykollib [![PyPi version](https://img.shields.io/pypi/v/pykollib.svg)](https://pypi.python.org/pypi/pykollib/) [![Python 3.6+](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
=====

What is it?
-----------
The purpose of pykollib is to create a [Python](http://www.python.org/) package that makes it extremely easy to develop code that works with [The Kingdom of Loathing](http://www.kingdomofloathing.com). pykollib can be used for anything from writing short scripts to complex bots.

It is based on pykol, on which both [kBay](http://forums.kingdomofloathing.com:8080/vb/showthread.php?t=141613) and [wadbot](http://forums.kingdomofloathing.com:8080/vb/showthread.php?t=152258) were built.

Who is it for?
--------------
pykollib is for programmers who are interested in writing scripts and bots for KoL. If you do not feel comfortable writing code, then pykollib is probably not for you.

Example
-------
See `examples/` for example uses of `pykollib`.


Requirements
------------
pykollib requires Python 3.x.

To install third-party libraries

```console
$ make install
```

Running the Unit Tests
----------------------
pykollib includes a [unittest](http://docs.python.org/2/library/unittest.html) suite, to showcase some of its functionality and to help ensure that new game changes don't break your existing code. Developers are strongly encouraged to add unit tests for new features that they create.

To run the test suite:

```console
$ make test username=[username] password=[password]
```

How can I contribute?
---------------------
1. [Fork](http://help.github.com/forking/) pykollib
2. Clone your fork - `git clone git@github.com:your_username/pykollib.git`
3. Add a remote to this repository - `git remote add upstream git://github.com/scelis/pykollib.git`
4. Fetch the current pykollib sources - `git fetch upstream`
5. Create a topic branch - `git checkout -b my_branch upstream/master`
6. Commit (or cherry-pick) your changes
7. Push your branch to github - `git push origin my_branch`
8. Create an [Issue](http://github.com/scelis/pykollib/issues) with a link to your branch
9. That's it!
