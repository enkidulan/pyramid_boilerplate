*********************************************
Development Environment for Pyramid projects
*********************************************

Pyramid_  is the greatest web framework that I've ever seen, so I use it
quite often and want to share this environment assembling boilerplate in
hope that it will hope other people.

This boilerplate based on `zc.buildout`_ and designed to accomplish following
goals:

    #. Provide easy and robust maintenance system.
    #. Provide easy to configure settings.


Environment assembling
----------------------

For environment set up zc.buildout is used (https://pypi.python.org/pypi/zc.buildout)

Before building it you need to set up environment version you would like to have.
Currently there is *production* and *development* configuration available, to
set configuration do following:

.. code-block:: bash

    $ cp buildout.cfg.example buildout.cfg
    $ vim buildout.cfg

and in buildout.cfg uncomment one of profiles extends  you would like to be
activated, for example if you would like your environment to be build in
*production* mode the part section of buildout should look like this:

.. code-block::

    [buildout]
    extends =
        profiles/production.cfg
    #    profiles/devel.cfg


To build buildout run following command:

.. code:: bash

    $ python bootstrap-buildout.py
    $ bin/buildout


Development helpers
-------------------

1. *Git remote repo python distribution wrapper*

Usually I use NGBP template for my frontend applications and distribute
it as a python package for simple version control handling.

.. code-block:: bash

    $bin/pypack blog_frontend https://github.com/ngbp/ngbp.git

And now you have ngbp wrapped as python distribution.



.. _Pyramid: http://www.pylonsproject.org/projects/pyramid/about
.. _zc.buildout: http://www.buildout.org/en/latest/
