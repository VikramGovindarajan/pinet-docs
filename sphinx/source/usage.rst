Usage
=====

.. _installation:

Installation
------------

To use PINET documentation, first install it using pip:

.. code-block:: console

   $ pip install pinet-docs
   
Creating recipes
----------------

To retrieve a list of random ingredients,
you can use the ``lumache.get_random_ingredients()`` function:

.. autofunction:: lumache.get_random_ingredients
	
.. autoexception:: lumache.InvalidKindError

   
>>> import lumache
>>> lumache.get_random_ingredients()
['shells', 'gorgonzola', 'parsley']