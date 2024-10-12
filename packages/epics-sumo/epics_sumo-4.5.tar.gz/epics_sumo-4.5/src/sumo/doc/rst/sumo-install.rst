Installing Sumo
===============

Parts of sumo
-------------

Sumo consists of scripts, python modules, documentation and configuration
files. 

The distribution does not contain the configuration files since you have
to adapt them to your development host. Examples of configuration files are
shown further below.

Sumo is available as a debian or rpm package, as a tar.gz or wheel file and on
pypi. The sections below describe all installation options.

Note that you have to *configure* sumo after installing it, see 
`The sumo configuration file`_.

Requirements
------------

Sumo requires at least `Python <https://www.python.org>`_ version 3.5 or newer.

Sumo is tested on `debian <https://www.debian.org>`_ and 
`Fedora <https://getfedora.org>`_ linux distributions but should run on all
linux distributions. It probably also runs on other flavours of unix, probably
even MacOS, but this is not tested.

It may run on windows, escpecially the `Cygwin <https://www.cygwin.com>`_
environment, but this is also not tested.

Install methods
---------------

If you just want to give sumo a try without going too much into installation
details, you can enter these commands ('DIRECTORY' is created by this)::

  python -m venv DIRECTORY
  source DIRECTORY/bin/activate
  pip install EPICS-sumo

The sections below describe installation methods in more detail.

Install with pip
++++++++++++++++

`pip <https://en.wikipedia.org/wiki/Pip_(package_manager)>`_ is the python
package manager. It is easy to use, the only disadvantage is that on Linux
systems it circumvents your package manager.

Install locations
:::::::::::::::::

First you have to check *where* you want to install sumo:

- globally, which is the default,
  see `global install <https://docs.python.org/3/installing/index.html>`_
- just for the current user, see `user install <https://docs.python.org/3/installing/index.html#install-packages-just-for-the-current-user>`_
- at a specific path, see `PYTHONUSERBASE <https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUSERBASE>`_
- in a python virtual environment, see `virtual environment <https://docs.python.org/3/library/venv.html>`_

Install examples (shown for global install)
:::::::::::::::::::::::::::::::::::::::::::

Install from pypi (easiest when you have an internet connection)::

  pip install EPICS-sumo

Install from downloaded \*.tar.gz or \*.whl file [1]_::

  pip install FILENAME

Install from source directory [2]_::

  pip install DIRECTORY

.. [1] You can download these files at  
  `sumo downloads at Sourceforge <https://sourceforge.net/projects/epics-sumo/files/?source=navbar>`_

.. [2] You can checkout the repository with 
   ``hg clone http://hg.code.sf.net/p/epics-sumo/mercurial epics-sumo-mercurial``

Global install with with system's package manager (Linux)
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

On systems with debian package manager (debian/ubuntu/suse...) [1]_ [3]_::

  dpkg -i PACKAGEFILE

On systems with rpm package manager (fedora/RHEL/CentOS...) [1]_ [4]_::

  rpm -ivh PACKAGEFILE

.. [3] The \*.deb files were created for Debian Linux. They may work for other
   debian based distributions like ubuntu but this was not tested.

.. [4] The \*.rpm files were created for Fedora Linux. They may work for other
   rpm based distributions like RedHat Linux but this was not tested.

The sumo configuration file
---------------------------

In order to use sumo on your system you should create a configuration file. The
default name for this file is "sumo.config". 

See :doc:`configuration-files` for a complete description of configuration files.

See :ref:`sumo.config examples <configuration-files-config-examples>` for examples
of configuration files.

See :ref:`sumo config new <reference-sumo-config-new>` for a command that
creates a configuration file from a template provided with sumo.
