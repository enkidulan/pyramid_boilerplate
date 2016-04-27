This is a Websauna application package for blender.

Prerequisites
=============

* PostgreSQL

* Redis

Installation
============

This installation method assumes you the author of the blender application and wish to develop it. Below are instructions to to install the package to a Python virtual environment using pip command in an editable mode.

Example::

    cd blender  # This is the folder with setup.py file
    virtualenv venv
    source venv/bin/activate

    # Make sure pip itself is up-to-date
    pip install -U pip

    # Install the package and its dependencies to a currently
    # activated virtualenv from the folder with setup.py file
    pip install -e "."

Running the website
===================

Local development machine
-------------------------

Example (OSX / Homebrew)::

    # Create PostgreSQL database
    psql create blender_dev

    # Write table schemas for models
    ws-sync-db development.ini

    # Start web server
    pserve -c development.ini --reload

Running the test suite
======================

Example::

    # Install testing dependencies
    pip install ".[dev,test]"

    # Create database used for unit testing
    psql create blender_test

    # Run test suite using py.test running
    py.test myapp/tests --ini test.ini

More information
================

Please see https://websauna.org/