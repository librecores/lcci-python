.. LibreCores CI Tool documentation master file, created by
   sphinx-quickstart on Tue May 30 13:39:22 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

LibreCores CI Tool
==================

Welcome to the LibreCores CI tool (``lcci``).
This tool is used to setup and control agents connected to the LibreCores Continuous Integration (CI) infrastructure.
Agents can be set up and connected to run jobs for either your own projects, any other project or with projects matching certain criteria.

To ensure agents share a common setup and to guarantee reproducible builds we use `Environment Modules <http://modules.sourceforge.net>`_.
Tools can be installed in different versions and the build environment selects the proper version.
We provide a set of `Docker <http://docker.com>`_ containers to automatically build and/or install the tools.
Along with the tool itself the configuration files for Environment Modules are created (so called ``modulefiles``).

In the projects' ``Jenkinsfile`` the modules are then accordingly loaded:

.. code-block:: groovy

   node('lcci-2017.1') {
      lcci.load(["eda/fusesoc/1.6.1",
                 "eda/verilator/3.902"])

      ...
   }


Contents
--------

.. toctree::
   :maxdepth: 2

   gettingstarted
   api

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
