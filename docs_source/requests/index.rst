Request Reference
=================

It is the aim of `pykollib` that every action that can be performed through the
Kingdom of Loathing web interface is represented as a `request` in this module.
`requests` handle the two aspects of interacting programmatically with KoL -
generating the requisite URL and parsing the HTML response.

Normally to use a request you pass it to the `parse` method of your Session instance.
However, in the case of a bug or to capture something not covered by the parse function,
it is possible to carry out these two operations separately.

.. code-block:: python

   async def spend_ten_turns_in_canadia_gym():
     response = await canadia_gym(session, 10)
     # do something else with response
     return await response.parse()

As the parsed return type is a result of a different function, the documentation is
currently not displaying it, but we’re working on it!

.. automodule:: pykollib.request
 :members:
 :undoc-members:
