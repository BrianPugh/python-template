
Usage
=====

To use this template, click the green "Use Template" button in the github web interface.
Then run:

.. code-block: bash

   git clone YOUR_REPO
   ./bootstrap.py

And follow the on-screen prompts.


Features
========
* Poetry_ support.
* Sphinx + ReadTheDocs.
* ``pre-commit`` linting and static analysis.
* Github actions for:
   + Run ``pre-commit`` and unit tests on pull requests.
   + Build and upload wheels to PyPi on semver tags ``vX.Y.Z``.

.. _Poetry: https://python-poetry.org
