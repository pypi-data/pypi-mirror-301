.. include:: /properties.rst

Common errors
=============

When using |prgnam| sometimes problems arise after editing input files or upgrading programs like Pandas_ or Matplotlib_. Here are some 'last lines' of an error stack that are displayed in the terminal and, if the program started up, registered in the log-file ``run-log.txt`` (/:smc:`LOGS`/:smc:`EXP`/:smc:`LOGFILNAM`) in the work folder.

With any command
----------------

- ``ImportError: cannot import name 'SOMENAME' from 'coalispr.resources.constant'``

The program or configuration file (one of its components like ``2_shared.txt`` or ``3_EXP.txt``) has been changed and the new version blocks the program due to a variable that is wrong (typo?), missing or novel. The only feedback that can be used for pointers to solve the problem will be the error stack in the terminal. Sometimes errors arise because characters that need to be paired (opened and closed) like ``"``, ``'``, ``{}``, or ``()``, remain 'single' in lines preceding the line that is mentioned to contain the mistake.

Generate a working configuration file directly by: ``python3 -m coalispr.resources.constant_in.make_constant``. This will generate a configuration shipped with |PRGNAM|.

Correct any mistakes in configuration to use for your own experiment :smc:`EXP`, then run ``coalipsr setexp -e EXP -p2``. 

|

``setexp``
----------

- ``File not found: [Errno 2] No such file or directory: '<path to>/Coalispr/config/constant_in/2_shared.txt'``

  This happens when ``coalispr init`` has not been run. Restoring this includes resetting the configuration required for |prgnam| to start up:

  - ``python -m coalispr.resources.constant_in.make_constant``. Rerun the failed commands after this.

|

``storedata``, ``showgraphs``
-----------------------------
  

- ``ModuleNotFoundError: No module named 'pandas.core.indexes.numeric'``

  After upgrading to Pandas_ version 2.x.y from version 1.5.z (say to ``pandas-2.1.1`` from ``pandas-1.5.2``) or when starting afresh with |prgnam| on a dataset after installing ``pandas-2.x`` the :term:`pkl` data files are not opened by ``python.shelve`` (in module ``coalispr.bedgraph_analyze.store``) by absence of ``numeric.py``, which turns out to be required in this context (see also this :ref:`how-to section <the <bckpbd>`). Therefore, place a symbolic link (or a copy) of ``coalispr.resources.numeric.py`` in ``python3/site_packages/pandas/core/indexes/`` (discussed `here <https://github.com/pandas-dev/pandas/issues/53300>`_).


..  - ``unlink`` or ``rm`` (remove/delete) the ``numeric.py`` in ``python3/site_packages/pandas/core/indexes/``.  

|

``storedata``
-------------  

- ``Sorry, program failed. Column 'CONDITION' is  not found in the experiment file (EXPFILE)``

  Sometimes an :ref:`expected column <exp>` in :smc:`EXPFILE` is not relevant for an experimental dataset; for example :smc:`CONDITION` becomes redundant when the different conditions `induced` and `uninduced` are covered by :smc:`CATEGORY` in the definition of controls. Inclusion of an empty condition column with its header will make it work.

|

- ``KeyError '<chromosome name>', stopping.. Have all files to be merged already been binned?``

  When restoring pickled files from a tsv-backup datafiles get merged (not restored from merged data), which goes wrong if chromosome names contain a symbol used as separator. Please redefine :smc:`P2TDELIM` in ``2_shared.txt``
  
|

.. _strdatsiz:

- Size difference between old and new :smc:`EXPFILE`

When changing a sample name the experiment file (:smc:`EXPFILE`) is rebuilt to incorporate the new sample names that replace the original ones. This operation involves ideally the ``Python.zip()`` function but this results in truncation of the output file if not all rows/columns are of equal length (i.e. with the same number of tabs). To minimize problems, ``Python.itertools.zip_longest()`` is used instead because that function takes the longest row/column as standard. Best is an :smc:`EXPFILE` that consists of rows (or columns) with an equal number of cells. (See this `thread on stackoverflow <https://stackoverflow.com/questions/42297228/i-am-losing-values-when-i-use-the-zip-function-in-python-3>`_.)

..  As an example compare ``coalispr/resources/exp_label_names13-sorted.bak`` to ``coalispr/resources/exp_label_names13-sorted.bak1``; the former has been replaced by  ``coalispr/resources/exp_label_names13-sorted.tsv`` after renaming samples isolated from cells with a deletion in the gene for Ago2 grown to an OD\ :sub:`600` of ~7.

|

``showgraphs``
--------------


- ``pandas.errors.ParserError: Error tokenizing data. C error: Expected 9 fields in line 20, saw 10``

- ``ValueError: Integer column has NA values in column 3``

- ``ValueError: invalid literal for int() with base 10: '313713-313804'``
  
  These different last-line messages occur when a :term:`GTF` annotation file cannot be parsed properly after editing. Each of these lines points to a different mistake, but all affect the structure of the file by not using a ``tab``  where that is expected to separate the columns/fields.

  Check whether a ``tab`` is missing or a ``space`` is used instead.  In the last example, a dash (``-``) was copied over with genome coordinates but not changed to a ``tab``.

  First lines of the stack (to see these scroll up in the terminal or check the log-file) are like:

  .. code-block:: text

        Traceback (most recent call last):
          File "/<path to>/coalispr/coalispr/bedgraph_analyze/genom.py", line 667, in _retrieve_gtf
            return UNSP_PLUS, UNSP_MINUS
        NameError: name 'UNSP_PLUS' is not defined

  The ``_retrieve_gtf`` function provides the annotations from a :term:`GTF` reference file that form the value for a constant, in this case, :smc:`UNSP_PLUS`.

- ``No annotations selected for '<chrnam>'; check GTF.`` 

  The program runs but with this message shown in the terminal.

  Selection of annotation lines beginning with the name of the DNA source (``chrnam``) did not work. Any ``space`` around ``chrnam`` in the GTF file would interfere; make sure that ``chrnam`` is directly followed by a ``tab``.

|

  
``showcount``
-------------

- ``ICE default IO error handler doing an exit(), .. errno = 32``

The set :smc:`BACKEND` cannot cope with displaying the data (see :ref:`'Backends' <ice32>` in the :doc:`/howtoguides`).

- ``Warning: Attempting to freeze the notification queue for object GtkImage[0x5e7f690]``
- ``Property notification does not work during instance finalization.``
- ``lambda event: self.remove_toolitem(event.tool.name))``

In these cases change :smc:`BACKEND` to, say, 'TkAgg' or 'GTK3Agg'.
    
|

``region``
----------

- ``IndexError: GridSpec slice would result in no space allocated for subplot``

There is not enough drawing space to include all sample-rows in the figure. Try reducing the number of samples in the analysis. This error popped up for a diagram with length-distributions for over 100 samples; the count diagram for this dataset gave no issue.

|

``groupcompare``
----------------

- When in :smc:`EXPFILE` a value is followed/replaced by a ``space``, this can interfere with running of the program, giving unexpected results. For example, the empty output for  ``1:``  was caused by a space by itself in the column :smc:`GROUP` during testing:

.. code-block:: text

    bash$ coalispr groupcompare -g 1

    For 'Group' pick subgroup(s) to compare:
	
      List sample numbers, separated by a comma (','). Choose from:
      1:  	  2: a1	  3: meth	  4: re1	  5: re2	  6: re3  7: re4	  8: re5	  9: r1	  10: r6	  11: STANDARD	
    
	('stop' to cancel.)

- Any occurrence would be a bug in the program because such white spaces would be removed when loading the :smc:`EXPFILE` into a Pandas_\ .DataFrame.
    
