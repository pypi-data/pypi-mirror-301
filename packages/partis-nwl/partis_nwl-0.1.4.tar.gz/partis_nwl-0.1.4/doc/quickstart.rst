
Quickstart
==========

Install ``partis-nwl``
----------------------

.. code-block:: bash

  pip install partis-nwl

.. note::

  Optionally install ``partis-view`` (Only needed to use graphical editor).

  .. code-block:: bash

    pip install partis-view

Create tool file
----------------

The example Tool below simply sets the output ``y`` equal to the input ``x``.

.. code-block:: yaml
  :caption: simply_xy.yml

  type: tool
  inputs:
    x:
      type: float
  outputs:
    y:
      type: float
      value: $expr:py _.data.inputs.x

Run Tool (as file)
^^^^^^^^^^^^^^^^^^

This may be run *as-is*, ``partis-nwl [[options]] [tool_name] [inputs_file]``,

.. code-block:: bash

  partis-nwl --workdir ./tmp ./simply_xy.yml ''

* The empty quotes ``''`` uses all default input values.
* ``--workdir ./tmp`` sets the working directory.

produces the following results:

.. code-block:: yaml
  :caption: ./tmp/simply_xy/nwl.results.yml

  type: results
  data:
    inputs:
      x: 0.0
    outputs:
      y: 0.0
  ...

Create tool package
-------------------

.. note::

  While not strictly needed to run a tool, putting multiple tools in a package
  provides some organization to related tools installed
  together, combining dependencies and any static/extra files.
  Doing this also generates HTML documentation from the tool(s).

.. code-block:: yaml
  :caption: nwl_simple.yml

  type: tool_pkg
  info:
    name: nwl_simple

  tools:
    - simply_xy.yml


The following command packages all tool files,

.. code-block:: bash

  partis-nwl-pkg -o ./dist ./nwl_simple.yml

producing (in this case):

* ``dist/nwl_simple-0.1-py3-none-any.whl`` - Generated Python package, may be installed
  using

  .. code-block:: bash

    pip install 'dist/nwl_simple-0.1-py3-none-any.whl[run]'

  .. note::

    The ``[run]`` extra also installs all specified dependencies,
    although there aren't any in this case.
    These are separated as an *extra* to allow installing the tool without
    dependencies, for instance, so it can be inspected by the graphical editor.

* ``dist/nwl_simple-0.1-doc.tar.gz`` - Generated HTML documentation

  .. note::

    It is possible to build the package *without* building the documentation
    using the ``--no-doc`` option.

Run Tool (as package)
^^^^^^^^^^^^^^^^^^^^^

The *packaged* tool may be run now using its qualified package name
``nwl_simple.simply_xy``, instead of the original file name,

.. code-block:: bash

  partis-nwl --find-links ./dist --workdir ./tmp nwl_simple.simply_xy ''


.. note::

  The optional ``--find-links`` argument is used by ``pip`` to install the packaged
  ``.whl`` file (if not already installed), or to find any other *local* Python
  dependencies.
