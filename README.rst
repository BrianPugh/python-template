|Python compat| |GHA tests|

A template to quickly get you creating an open-source python library
or project with linting, static analysis, CI, and CD to PyPi.

Usage
=====

To use this template, click the green "Use this template" button in the github web interface.
Then run:

.. code-block:: bash

   git clone YOUR_REPO
   ./bootstrap

And follow the on-screen prompts. ``bootstrap`` uses some git data (like detecting your username and repository name), so cloning the repo generated from the template is necessary.

Compatibility
=============

This template only works on MacOS/Linux/WSL, it *will not work natively on windows*.

Features
========

* Features dependent if project is a library or a standalone project.

* `Poetry`_ support.

  * If not installed, Poetry will automatically be installed when running ``bootstrap``.

* Optional CLI boilerplate using ``typer``.

* `Sphinx`_ + `ReadTheDocs`_.

  * Goto `ReadTheDocs Dashboard`_ and click on "Import a Project".

* `Pre-commit`_ linting and static analysis.

* `Docker`_ support for standalone projects.

* GitHub actions for:

  * Run ``pre-commit`` on pull requests and commits to ``main``.

  * Run unit tests, coverage, and verify docs build on pull requests and commits to ``main``.

    * Goto your `Codecov Dashboard`_ and add your repo.

  * Build and upload wheels to PyPi on semver tags ``vX.Y.Z``.

    * Add your `PyPi API token`_ to your `GitHub secrets`_ for key ``PYPI_TOKEN``.

  * Build and upload docker images to Dockerhub.

    * Add your Dockerhub username and `token`_ to your `GitHub secrets`_
      ``DOCKERHUB_USERNAME`` and ``DOCKERHUB_TOKEN``.


Reference
=========
If you find this in the git history of a project and you like the structure, visit
this template at https://github.com/BrianPugh/python-template .


.. |GHA tests| image:: https://github.com/BrianPugh/python-template/workflows/tests/badge.svg
   :target: https://github.com/BrianPugh/python-template/actions?query=workflow%3Atests
   :alt: GHA Status
.. |Python compat| image:: https://img.shields.io/badge/>=python-3.8-blue.svg

.. _Codecov Dashboard: https://app.codecov.io/gh
.. _Docker: https://www.docker.com
.. _GitHub secrets: https://docs.github.com/en/actions/security-guides/encrypted-secrets
.. _Poetry: https://python-poetry.org
.. _Pre-commit: https://pre-commit.com
.. _PyPi API token: https://pypi.org/help/#apitoken
.. _ReadTheDocs Dashboard: https://readthedocs.org/dashboard/
.. _ReadTheDocs: https://readthedocs.org
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _token: https://docs.docker.com/docker-hub/access-tokens/
