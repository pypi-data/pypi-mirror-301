
Overview
========

Data Types
----------

:term:`NWL` follows a strictly defined structure composed of
elementary data types, each with a 'plain text' representation.
There are many additional predefined types, but all are derived as some
composition of the following elementary types:

* ``bool``: boolean True / False values
* ``int``: integer digit values
* ``float``: floating point values
* ``string``: array of encoded characters
* ``list``: ordered sequence of values
* ``dict``: ordered mapping of key-value pairs
* ``struct``: like a ``dict``, but the types are fixed for each key-value pair,
  and each key may be defined by different types.
* ``union``: a set of types

.. note::

  :term:`NWL` itself does not restrict the format of data stored in files,
  but :term:`YAML` is currently the only implemented format for
  loading and saving the :term:`NWL` definitions, inputs, and result files.

  An important, but sometimes subtle, distinction is made in :term:`NWL` that
  **all mappings are assumed to be ordered**.
  This restriction was chosen to provide consistent order for evaluation and
  visualization of mapping fields.
  Care should be taken by third-party serialization to ensure that the order of
  mappings is preserved, which :term:`YAML` amd :term:`JSON` do not specify,
  and which parsing libraries may not enforce by default.

A :term:`NWL Tool` (:class:`~partis.nwl.tool.Tool`) definition consists of
seven top-level sections:

* ``info`` (:mod:`partis.nwl.info`): user-friendly label, version, author, and documentation.
* ``resources`` (:mod:`partis.nwl.resources`): Computational capabilities,
  static data, and program requirements.
* ``inputs`` (:mod:`partis.nwl.inputs`): data schema for the input values.
* ``outputs`` (:mod:`partis.nwl.outputs`): data schema for the output values.
* ``commands`` (:mod:`partis.nwl.commands`): prepares and executes scripts or
  underlying program(s) to achieve the goal of the tool.
* ``prolog``: issue messages regarding the ``inputs`` as a whole.
* ``epilog``: issue messages regarding overall tool execution.

Inputs
------

All input types have fields for ``label``, ``doc``, ``visible``, ``enabled``,
and ``default_val`` (``default_case`` for unions).
The ``label`` is used to provide a short, user-friendly name for the input.
Additional information may be placed in the ``doc`` field, which is used to provide
more contextual information about the purpose of the input.
The ``default_val`` is used as the initial value in the graphical inputs editor,
or to fill in a value when one is not provided in the input file when the tool is run.

.. note::

  All inputs have a ``default_val`` even if the value is not used at
  run-time. If one is not specified, then the value will chosen by the run-time that
  is valid according to the schema.

.. only:: html

  .. include:: input_html.rst.in
  .. include:: command_html.rst.in

.. only:: latex

  Simple Inputs
  ^^^^^^^^^^^^^

  * | ``The Bool``
    | The ``bool`` input type allows a single ``true`` or ``false`` value.

    * The Boolean Class :class:`partis.nwl.inputs.BoolInput`

    * The Boolean Tool Editor :numref:`bool_tool_editor` 

    * A minimized version of the boolean yaml :numref:`bool_yaml_min` 

    * A full version of whats in the boolean yaml :numref:`bool_yaml_full`

  * | ``The Int``
    | The ``int`` input type allows a numeric value that must be equivalent to 
    | a whole number.


    * The Python Class reprsentation of an int :class:`partis.nwl.inputs.IntInput`

    * The Int tool editor :numref:`int_tool_editor`

    * Minimized version of the integer yaml :numref:`int_yaml_min`

    * Full version of whats in the integer yaml :numref:`int_yaml_full`
      
  .. note::

    In YAML, integers are represented differently than floats
    (e.g. ``10`` is an integer, while ``10.0`` and ``1e1`` are floats), but NWL
    validation treat these values equivalently.


  * | ``The Float``
    | The ``float`` input type allows a numeric value that must be equivalent to
    | a real number.

    * The Python Class representation of a floating point :class:`partis.nwl.inputs.FloatInput`

    * The Float Tool Editor :numref:`float_tool_editor`

    * Minimized version of the float yaml :numref:`float_yaml_min`

    * Full version of the float yaml :numref:`float_yaml_full`

  .. note::
    In YAML, integers are represented differently than floats
    (e.g. ``10`` is an integer, while ``10.0`` and ``1e1`` are floats), but NWL
    validation treat these values equivalently.


  * | ``The String``
    | The ``string`` input type allows a string of characters satisfying optional
    | conditions (lines, columns, regex pattern, etc).

    * The Python Class representation of a string :class:`partis.nwl.inputs.StrInput`

    * The string Tool Editor :numref:`string_tool_editor`

    * Minimized version of the string yaml :numref:`string_yaml_min`

    * Full version of the string yaml :numref:`string_yaml_full`


  * | ``The File``
    | Path to file that must exist before tool runs.

    * The Python Class representation of a File :class:`partis.nwl.inputs.WorkFileInput`

    * The File Tool Editor :numref:`file_tool_editor`

    * Minimized version of the File yaml :numref:`file_yaml_min`

    * Full version of the File yaml :numref:`file_yaml_full`

  * | ``The Dir``
    | Path to directory that must exist before tool runs.

    * The Python Class representation of a Dir :class:`partis.nwl.inputs.WorkDirInput`

    * The Dir Tool Editor :numref:`dir_tool_editor`

    * Minimized version of the Dir yaml :numref:`dir_yaml_min`

    * Full version of the Dir yaml :numref:`dir_yaml_full`

  * | ``The List``
    | The ``list`` input type allows for a variable length list (ordered sequence)
    | of values.
    | Each value in the list is validated against the definition in the list's ``item``.
    | For example, the list definition shown would allow a list of boolean values.

    * The Python Class representation of a List :class:`partis.nwl.inputs.ListInput`

    * The List Tool Editor :numref:`list_tool_editor`

    * Minimized version of the List yaml :numref:`list_yaml_min`

    * Full version of the List yaml :numref:`list_yaml_full`

  Structued Input Types
  ^^^^^^^^^^^^^^^^^^^^^

  * | ``The Struct``
    | The ``struct`` input type allows for a mapping of pre-defined key-value pairs
    | defined by the children in the ``struct`` field.
    | The ``struct_proxy`` field optionally allows a non-mapping value to be given as
    | an input value, which is assigned as the value for the given key leaving all other
    | values given by their respective ``default_val``.

    * The Python Class representation of a List :class:`partis.nwl.inputs.StructInput`

    * The List Tool Editor :numref:`struct_tool_editor`

    * Minimized version of the List yaml :numref:`struct_yaml_min`

    * Full version of the List yaml :numref:`struct_yaml_full`


  * | ``The Union``
    | The ``union`` input type allows the input value to be valid against one of
    | several possible cases.
    | In order to prevent ambiguity which case a value corresponds to while parsing
    | the input file, the cases allowed in the union is restricted to the following
    | combinations:
    | - Max of one ``bool``.
    | - Max of one numeric ``int`` or ``float``.
    | - Max of one ``string``.
    | - Max of one ``list``.
    | - Any number of cases of type ``struct`` (the ``type`` for the struct is
    |  set by the case key )
    | - No *direct* case of another ``union`` (a list/struct with a union is ok).
    | The union type has a ``default_case`` instead of ``default_val``, which is the
    | key of the case that will be used to get the initial/default value.
    | If the ``default_case`` is not given, then the *first* case is used as the default.

    * The Python Class representation of a Union :class:`partis.nwl.inputs.UnionInput`

    * The Union Tool Editor :numref:`union_tool_editor`

    * Minimized version of the Union yaml :numref:`union_yaml_min`

    * Full version of the Union yaml :numref:`union_yaml_full`


  * | ``The Selection``
    | The ``selection`` field appears on the ``int``, ``float``, and ``string`` input
    | types that can be used when there is a predefined set of allowed values.
    | In the graphical inputs editor, this will create a drop-down combo with the
    | selection as the available options instead of the general input editor.
    | If the label of each option is a non-empty string, then it is used as the
    | displayed value instead of the literal value.

    * The Python Class representation when selecting an int :class:`partis.nwl.inputs.IntSelectOption`
    * The Python Class representation when selecting a float :class:`partis.nwl.inputs.FloatSelectOption`
    * The Python Class representation when selecting a string :class:`partis.nwl.inputs.StrSelectOption`

    * The Selection Tool Editor :numref:`selection_tool_editor`
    * The Minimized version of the selection yaml :numref:`selection_yaml_min`
    * Full version of the selection yaml :numref:`selection_yaml_full`


  * | ``Outputs``
    | Tool outputs are structurally similar to the inputs, supporting all the same
    | types and nesting/combinations as the inputs section.
    | The main difference is that an additional ``value`` expression must be given
    | to define how the output value is computed.
    | The ``value`` expression must be defined at the first level of output names,
    | and the return of the expression will be validated according to the remaining
    | levels of the given output.
    | In the example shown below, the ``new_key`` output is defined as a list of bools,
    | and so the expression must evaluate to a list of boolean values (
    | e.g. ``[True, False, True]``).

    * The output's tool editor :numref:`tool_tool_editor`
    * The output's yaml minimized :numref:`tool_yaml_min`
    * The outpus's yaml maximized :numref:`tool_yaml_full`

  .. note::

    Outputs also have a ``default_val``, but  that value is *only* used in the event
    that the expression evaluates to ``None``.

  Command Types
  ^^^^^^^^^^^^^

  * | ``Process``
    | Run a command line program.

    * The Process Class representation in python :class:`~partis.nwl.commands.process.ProcessCommand`

    * The Process tool editor :numref:`process_tool_editor`
    * The Process yaml minimized :numref:`process_yaml_min`
    * The Process yaml maximized :numref:`process_yaml_full`

    * The Process post epilog message :numref:`process_epilog`


  .. note::

    The first item in the ``args`` list is the base command to run.

  .. note::

    By default, the process ``returncode`` is used to determine if the process
    exited because of an error.
    This is done in the default ``epilog``, and must be preserved, or altered, to
    impose other conditions on the success of the command.



  * | ``File Command``
    | Creating a file with different specifications

    * | Creating a file in the run directory with given contents.
      | :numref:`file_command_run_dir`

    * | By default, the ``contents`` are given as text and encoded as UTF-8.
      | However, it may be an expression that generates the content of the file
      | :numref:`file_command_expression`

    * | or, by setting ``content_mode: binary``, the contents given as raw binary data
      | in the URL- and filesystem-safe Base64 alphabet, which substitutes
      | ``-`` instead of ``+``, and ``_`` instead of ``/``.
      | :numref:`file_command_raw_generation`

      * The File Command python representation :class:`~partis.nwl.commands.file.FileCommand`

      * The File Command tool editor :numref:`file_command_tool_editor`

      * The File Command minimized yaml :numref:`file_command_min_yaml`

      * The File command maximized yaml :numref:`file_command_max_yaml`

  * | ``Directory Command``
    | Create a directory in the run directory.

    * The Directory Command Class representation in python :class:`~partis.nwl.commands.dir.DirCommand`

    * The Directory Command tool editor :numref:`dir_command_tool_generation`
    * The Process yaml minimized :numref:`dir_command_yaml_min`
    * The Process yaml maximized :numref:`dir_command_yaml_full`

    * Generating a Directory in the run directory :numref:`create_dir`


  * | ``Script Command``
    | The return value of the script is accessible to subsequent commands and output
    | expressions, and may be composed of the above elementary data types.

    * The Script Command Class representation in python :class:`~partis.nwl.commands.script.ScriptCommand`

    * The Script tool editor :numref:`script_command_tool_editor`
    * The Script yaml minimized :numref:`script_command_min_yaml`
    * The Script yaml maximized :numref:`script_command_full_yaml`

    * A Python script for running commands :numref:`running_script`


Evaluated Expressions
---------------------

Expressions are non-literal values such as a Python statement/function or a
Cheetah template string.
The actual value used for the field is determined by evaluating the expression,
such as using the Python interpreter or template engine.

Expressions are embedded as plain-text beginning with the ``$`` escape
character that is followed by a specifier for how the expression is to be
evaluated.
Currently there are three supported types of expressions:

.. tab-set::

  .. tab-item:: expr:py

    .. code-block:: yaml

      $expr:py _.data.inputs.some_input == 3

    A :term:`Python` expression, the value being the equivalent
      to using :func:`eval`.


  .. tab-item:: func:py

    .. code-block:: yaml

      $func:py

      x = ( _.data.inputs.some_input + 2 ) % 3

      return x == 0

    A :term:`Python` function, the resulting value must be given with ``return`` statement.

  .. tab-item:: tmpl:cheetah

    .. code-block:: yaml

      $tmpl:cheetah
      #if $_.data.inputs.some_input == 3:
      It's going to do the thing.
      #else
      Not doing it.
      #end if

    A :term:`Cheetah` template for a string.

    .. note::

      Cheetah templates are only available for certain fields that have a *string*
      value.

Depending on where they appear in the tool definition,
expressions may use input values, run-time information, command results,
or output values.
Values accessible in an expression are stored within the underscore ``_``
object available in the expression's local context.

Note that the interpreter used to evaluate the ``inputs`` and root
``prolog`` expressions may have limited
capabilities, since these are intended mainly for graphical editors and not the
run-time environment.
Expressions in the ``commands``, ``outputs``, and ``epilog`` are evaluated
by the tool run-time engine, and may make use of import statements
and perform expensive operations.
There are some fields within these sections treated dynamically at different
points in the tool workflow:

* ``enabled``: An expression that can dynamically enable/disable a field or section.
  For logging events and commands the ``enabled`` field controls whether the event
  occurs or whether the command should be executed.

* ``visible``: Controls whether the input should be visible when it is
  *not* enabled.
  A field that is visible may appear disabled or grayed out when not enabled.

* ``value``: For outputs, an expression is used
  to compute the value that is supplied as an output result.

* ``prolog``, ``epilog``: Dynamically triggered and formatted logging events to
  provide additional feedback about the execution of the tool.

* ``contents``, ``source``, ``args``: For commands, expressions used for generating
  file contents, arbitrary scripting actions, and dynamically computed process
  arguments.

The order in which expressions are evaluated at run-time is summarized by the pseudo-code:

* eval ``prolog``
* for each command in ``commands``

  * eval ``enabled``
  * if ``enabled``

    * eval ``prolog``
    * eval  ``contents``, ``source``, ``args``
    * eval ``epilog``

* for each output in ``outputs``

  * eval ``value``

* eval ``epilog``

The ``inputs`` and tool ``prolog`` has access to ``_.data.inputs``.
The commands section has access to ``_.data.inputs``,
``_.runtime``, and ``_.data.commands`` (of preceding commands).
Additionally, a **command** ``epilog`` has access to ``_.command`` that references
the result of the current command.
The outputs section also has access to ``_.data.inputs``,
``_.runtime``, and ``_.data.commands`` with all command results.
Finally, the tool ``epilog`` has access to all of the above plus ``_.data.outputs``.



Logging Events
--------------

Logging events are an optional mechanism to include additional information,
feedback to the user, and error handling.
These may be set in the ``prolog`` or ``epilog`` fields at the root level of
the tool and within each command.
Every log event has three fields: ``level``, ``msg``, and ``enabled``.
The ``enabled`` value controls whether the logging event occurs based on input or
run-time values.
The ``msg`` value is the text string that is to be reported if the log event is enabled.
The ``level`` value marks the severity of the event, and is one of ``DEBUG``, ``INFO``,
``WARNING``, ``ERROR``, or ``CRITICAL``.
All enabled events are saved in the run-time results, but are also printed to the
terminal based on the level set for the runtime.

Logging events specified for inputs may be used by a graphical inputs editor to
provide additional validation or feedback not provided by the NWL specification.

Events specified in the **tool** ``prolog`` are evaluated before
the tool executes, while the ``epilog`` are evaluated after all
commands and outputs have been successfully evaluated.
Similarly, each **command** ``prolog`` is evaluated at run-time before running the command,
and the command ``epilog`` is evaluated after the command has been evaluated.
If any log event is enabled and has a level of ``ERROR`` or ``CRITICAL``, then the tool
will immediately stop in an error state.

Example Tool
------------

A complete example is given here for an NWL Tool that wraps a sub-set of
the Linux ``grep`` command, which reads a text file and returns the lines of
the file that match a given pattern.

.. literalinclude:: ../examples/grep.yml
  :language: yaml
  :linenos:
  :emphasize-lines: 8-36
  :caption: grep.yml

In order to run the tool, an input file has to be supplied that matches the
data structure specified in the ``inputs`` section highlighted above.
The :term:`NWL CLI` can be used to generate a template input file that
is filled with default values.

.. code-block:: bash

  partis-nwl --tool grep.yml --template inputs.yml

.. code-block:: yaml
  :caption: inputs.yml

  type: inputs
  invert_match: false
  inclusion_mode: default
  pattern: ''
  files: []


In this case the templated values will not produce anything useful since both
the ``pattern`` and ``files`` remain empty.
An example file to be searched is created in ``text.txt``, and the pattern is set
to ``'tools,'``, which should match all the lines in the file that have the
word 'tools' followed by a comma.

.. note::

  Default values do not need to be explicitly set in the input file.

.. code-block:: none
  :caption: text.txt

  https://en.wikipedia.org/wiki/Tool

  A tool is an object that can extend an individual's ability to modify features
  of the surrounding environment.
  Although many animals use simple tools, only human beings, whose use of stone
  tools dates back hundreds of millennia, have been observed using tools to make
  other tools.
  Early tools, made of such materials as stone, bone, and wood, were used for
  preparation of food, hunting, manufacture of weapons, and working of materials
  to produce clothing and useful artifacts. The development of metalworking made
  additional types of tools possible. Harnessing energy sources such as animal
  power, wind, or steam, allowed increasingly complex tools to produce an even
  larger range of items, with the Industrial Revolution marking an marked
  inflection point in the use of tools. The introduction of automation allowed
  tools to operate with minimal human supervision, further increasing the
  productivity of human labor.

.. code-block:: yaml
  :caption: inputs.yml

  type: inputs
  pattern: 'tools,'
  files: [ 'text.txt' ]

After updating the values, the tool can be run using the :term:`NWL CLI`.
The ``--rundir`` argument tells the runner to generate all out in the given
directory, otherwise it will run in the directory the command was invoked.

.. code-block:: bash

  partis-nwl --tool grep.yml --inputs grep_inputs.yml --rundir tmp

.. code-block:: bash

  Run: grep.yml
  Venv dir: /media/cdodd/box/projects/gembio-n1893/partis/src/partis-nwl/examples/tmp/venv_nwlrun
  Loaded tool: grep.yml
  Starting dir: /media/cdodd/box/projects/gembio-n1893/partis/src/partis-nwl/examples
  Working dir: /media/cdodd/box/projects/gembio-n1893/partis/src/partis-nwl/examples
  Run dir: /media/cdodd/box/projects/gembio-n1893/partis/src/partis-nwl/examples/tmp
  Inputs: grep_inputs.yml
  Inputs validated.
  ● Command finished: `run_grep`
  ╰─● last 3 lines of: nwl.cmd.run_grep.stdout.txt
    ╰╸Although many animals use simple tools, only human beings, whose use of stone
      Early tools, made of such materials as stone, bone, and wood, were used for
  Outputs evaluated
  Job completed successfully: wall-time 0:00:01.229344 (H:M:S)


Example Output
--------------

In addition to what is printed to the terminal, the complete ``stdout``,
``stderr``, and a ``results`` file is saved in the run directory.

.. code-block:: none
  :caption: tmp/partis.tool.commands.run_grep.stdout.txt

  Although many animals use simple tools, only human beings, whose use of stone
  Early tools, made of such materials as stone, bone, and wood, were used for

The ``results`` file contains a copy of the values for ``inputs`` used to run the tool
( after filling in default values and performing evaluations ),
the processing ``commands``,
the ``outputs`` (in this case, the filename of the ``stdout`` file)
and information on the ``runtime`` environment.

.. code-block:: yaml
  :caption: tmp/nwl.results.yml

  type: results
  data:
    inputs:
      invert_match: false
      inclusion_mode: default
      pattern: tools,
      files:
      - path: /media/cdodd/box/projects/gembio-n1893/partis/examples/nwl/text.txt
    commands:
      run_grep:
        enabled: true
        success: true
        starttime: 116014.251851176
        timeout: 0.0
        walltime: 0.5988925590063445
        logs: []
        env: {}
        args:
        - grep
        - tools,
        - /media/cdodd/box/projects/gembio-n1893/partis/examples/nwl/text.txt
        pid: 14158
        stdin:
          path: ''
        stdout:
          path: partis.tool.commands.run_grep.stdout.txt
        stderr:
          path: partis.tool.commands.run_grep.stderr.txt
        returncode: 0
    outputs:
      main_output:
        path: partis.tool.commands.run_grep.stdout.txt
  runtime:
    success: true
    workdir: /media/cdodd/box/projects/gembio-n1893/partis/examples/nwl
    rundir: /media/cdodd/box/projects/gembio-n1893/partis/examples/nwl/tmp
    cmd_index: 0
    cmd_id: run_grep
    logs: []
    env: {}
    mpiexec: []
    processes: 1
    cpus_per_process: 1
    threads_per_cpu: 1
    gpus_per_process: 0
