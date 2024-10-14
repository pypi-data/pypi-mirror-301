========================
Examples
========================

Install
=========

Type these commands in the terminal:

.. code-block:: bash

    $ git clone https://github.com/ojso/flask-exts.git
    $ cd flask-exts/examples
    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install flask-exts
    

Run the demo applications
==========================

Type the command in the terminal:

.. code-block:: bash

    $ flask --app start run --debug --port=5000

Bootstrap 4
-----------------

.. code-block:: bash

    $ flask --app bootstrap4/app.py run

Bootstrap 5
-----------------

.. code-block:: bash
    
    $ flask --app bootstrap5/app.py run

Now go to http://localhost:5000.

admin
-----------------

.. code-block:: bash
    
    $ flask --app admin/simple run

Now go to http://localhost:5000.


Overview of icons
-----------------

When Bootstrap-Flask updates the icon file, the overview page can be upgraded with:


.. code-block:: bash

    $ python3 update-icons.py

