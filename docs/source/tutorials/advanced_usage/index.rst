Advanced Usage
========================

Continuity Special Judge
----------------------------

Sometimes, we need to use special judge not only for predicating \
the correctness of output result, but the quality of result as well. \
So we can return a tuple of values which represent correctness and \
score to do this. Like the following code which is named ``spj_continuity.py``.

.. literalinclude:: spj_continuity.py
    :language: python
    :linenos:

Here is an example of correct result, but it is obviously not the \
best one.

.. literalinclude:: spj_continuity_demo_1.demo.sh
    :language: shell
    :linenos:

.. literalinclude:: spj_continuity_demo_1.demo.sh.txt
    :language: text
    :linenos:

Another example of correct result, which is better than the \
abovementioned one.

.. literalinclude:: spj_continuity_demo_2.demo.sh
    :language: shell
    :linenos:

.. literalinclude:: spj_continuity_demo_2.demo.sh.txt
    :language: text
    :linenos:

And then a wrong example as shown in following part.

.. literalinclude:: spj_continuity_demo_x.demo.sh
    :language: shell
    :linenos:

.. literalinclude:: spj_continuity_demo_x.demo.sh.txt
    :language: text
    :linenos:


Addtional Arguments
----------------------------

In some complex cases, additional arguments need to be passed into \
the special judge function, such as the mode of special judge, or \
something like the extra required data file's path. \
Like the following code which is named ``spj_additional.py``

.. literalinclude:: spj_additional.py
    :language: python
    :linenos:

Here is an common example

.. literalinclude:: spj_additional_demo_1.demo.sh
    :language: shell
    :linenos:

.. literalinclude:: spj_additional_demo_1.demo.sh.txt
    :language: text
    :linenos:

And, if you want the input to be separated by ``,``, just use the \
``-V`` option, like the command line below

.. literalinclude:: spj_additional_demo_2.demo.sh
    :language: shell
    :linenos:

.. literalinclude:: spj_additional_demo_2.demo.sh.txt
    :language: text
    :linenos:


.. note::

    File import features (like ``-I`` and ``-O`` options`) \
    are not supported in addtional arguments.

    If you need to load the content of a data file, just pass \
    the path of the data file by additional arguments, and then \
    manually load the file in your special judge function.


Create My Runnable Special Judge CLI
-------------------------------------------

You can create your own special judge CLI with the \
``pyspj_entry`` function. Like the following code named \
``spj_runnable.py``.

.. literalinclude:: spj_runnable.py
    :language: python
    :linenos:

You can see its version information.

.. literalinclude:: spj_runnable_version.demo.sh
    :language: shell
    :linenos:

.. literalinclude:: spj_runnable_version.demo.sh.txt
    :language: text
    :linenos:

And see its help information, which is almost the same as the \
native ``pyspj`` CLI.

.. literalinclude:: spj_runnable_help.demo.sh
    :language: shell
    :linenos:

.. literalinclude:: spj_runnable_help.demo.sh.txt
    :language: text
    :linenos:

The cli script ``spj_runnable.py`` created by yourself can be used \
like the ``pyspj`` CLI.

Besides, this runnable special judge script can be built to a \
standalone special judge executable file if needed.

.. literalinclude:: spj_runnable_installer.sh
    :language: shell
    :linenos:

