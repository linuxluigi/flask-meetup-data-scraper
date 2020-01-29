IDE
=====================================

This Project was created with `Visual Studio Code <https://code.visualstudio.com/>`_ and this
section help you to setup your VS Code installation for this project.

Recommanded Extensions for VS-Code
----------------------------------

Python
^^^^^^

- `Python <https://marketplace.visualstudio.com/items?itemName=ms-python.python>`_
- `MagicPython <https://marketplace.visualstudio.com/items?itemName=magicstack.MagicPython>`_
- `Visual Studio IntelliCode <https://marketplace.visualstudio.com/items?itemName=VisualStudioExptTeam.vscodeintellicode>`_
- `autoDocstring <https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring>`_

Docker
^^^^^^

- `Docker <https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker>`_
- `Docker Linter <https://marketplace.visualstudio.com/items?itemName=henriiik.docker-linter>`_

Install Python
--------------

Please use the same Version of Python as it used in the Flask Dockerfiles! Right now it is 
Python 3.8.

Windows 10
^^^^^^^^^^

.. note::
   Change the command ``Python`` to ``py`` when following the instructions!

To enable Python 3 in your Windows 10 Power please follow the article on 
`Digitalocean.com <https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-windows-10>`_

Mac
^^^

On mac you can use ``brew``

.. code-block:: console

    $ brew install python3


Linux
^^^^^

In moste linux systems python is installed and maintaind out of the box, you just need to check if
you use the same version as in in Dockerfiles.


Install Python dependencies
---------------------------

Virtualenv
^^^^^^^^^^

If you like, you can install every dependency in a specific folder via virtualenv.
To create a `virtualenv <https://virtualenv.pypa.io/en/stable/userguide/>`_ for the project
dependencies.

Virtualenv when Python 3 is the default python interpreter.

.. code-block:: console

    $ virtualenv venv

When you want to select a different python version use the param ``-p``

.. code-block:: console

    $ virtualenv venv -p python38

To use the virtualenv use the ``source`` command.

.. code-block:: console

    $ source venv/bin/activate

Install development packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Windows
.......

.. code-block:: console

    $ python -m pip install -r .\requirements\local.txt

Mac / Linux
...........

.. code-block:: console

    $ pip install -r requirements/local.txt

Code Format
-----------

This use `Black <https://github.com/psf/black>`_ to format this code, in VS Code you can set on
every save to format the code in black. You can add auto format in black on every save when you add
follow settings in your ``settings.json`` 

.. code-block:: json

    {
        "editor.formatOnSave": true,
        "python.formatting.provider": "black",
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        },
    }

To install ``black`` use ``pip``. 

For Windows::

    $ python -m pip install black

For Mac / Linux::

    $ pip install black

To format the code from the terminal you can use the black cli. For example to format the whole 
project use.

.. code-block:: console

    $ black ./