IDE
=====================================

This Project was created with `Visual Studio Code <https://code.visualstudio.com/>`_ and this
section help you to setup your VS Code installation for this project.

Install Python
--------------

Please use the same Version of Python as it used in the Flask Dockerfiles! Right now it is 
Python 3.8.

Windows
^^^^^^^

For Windows users download your version on `Python.org <https://www.python.org/downloads/>`_ and run the
installation. After installation select in your IDE your Python version via IDE or add it in your local
``.vsode/settings.json``.

.. code-block:: json

    {
        "python.pythonPath": "C:\\Python38\\python.exe"
    }

Mac
^^^

On mac you can use ``brew``

.. code-block:: console

    brew install python3

Also set your Python version in the IDE like in Windows.

Linux
^^^^^

In moste linux systems python is installed and maintaind out of the box, you just need to check if you
use the same version as in in Dockerfiles.

Also set your Python version in the IDE like in Windows.

Code Format
-----------

This use `Black <https://github.com/psf/black>`_ to format this code, in VS Code you can set on every save to format
the code in black. You can add auto format in black on every save when you add follow settings in your ``settings.json`` 

.. code-block:: json

    {
        "editor.formatOnSave": true,
        "python.formatting.provider": "black",
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        },
    }