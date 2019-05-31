API Reference
=============

.. toctree::
   :hidden:

   session

`pykollib` can be used through the API layer, the Request API or circumvented entirely
to directly visit URLs. That list is also in order of decreasing preference - we aim to
support every action through the API and at the very least through a Request.

.. code-block:: python

  async def main():
      async with Session() as kol:
          # Session.login is an API-level function to login
          await kol.login("username", "password")

          # Here we are using the mall_search request as there isn't currently
          # any API support for it.
          listings = await kol.parse(mall_search, "lime")

          for listing in listings:
            print("{} at {}".format(listing.stock, listing.price))
