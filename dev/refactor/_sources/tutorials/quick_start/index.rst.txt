Quick Start
=========================

Painless Test
-----------------------

Firstly, we need to create a new special judge function, \
like the following code in ``spj_demo.py``.

.. literalinclude:: spj_demo.py
    :language: python
    :linenos:

Then test a simple pair of input and output by the following \
command line.

.. literalinclude:: spj_simple.demo.sh
    :language: shell
    :linenos:

The output should be

.. literalinclude:: spj_simple.demo.sh.txt
    :language: text
    :linenos:

But when wrong output is given like below

.. literalinclude:: spj_simple_wrong.demo.sh
    :language: shell
    :linenos:


.. literalinclude:: spj_simple_wrong.demo.sh.txt
    :language: text
    :linenos:


Use File Input/Ouput Instead
-------------------------------------

When the scale of input and output are too large, we can use \
``-I`` and ``-O`` option to input from file or output to file.

Here is an example if input file ``input_demo.txt``

.. literalinclude:: input_demo.txt
    :language: text
    :linenos:

And an output file ``output_demo.txt``

.. literalinclude:: output_demo.txt
    :language: text
    :linenos:

When the following command is executed

.. literalinclude:: spj_file_io.demo.sh
    :language: shell
    :linenos:

The output result should be

.. literalinclude:: spj_file_io.demo.sh.txt
    :language: text
    :linenos:


Pretty Print the Result
-----------------------------------

The output result is a json-formatted string, and it is \
placed in one line in default. So if you want it to be prettily \
printed, the following command can be used.

.. literalinclude:: spj_pretty.demo.sh
    :language: shell
    :linenos:

Its output should be

.. literalinclude:: spj_pretty.demo.sh.txt
    :language: text
    :linenos:

