An APIResult object is returned by most calls to [APIRequest.query](APIRequest#query.md). It is a subtype of the Python dict type and is identical in almost all ways. See the [Python documentation](http://docs.python.org/library/stdtypes.html#mapping-types-dict) for full documentation. APIResult also includes a <var>response</var> member variable that includes HTTP response headers for debugging purposes.

In general, there is no reason to ever need to create an APIResult object (they're created automatically when needed), and they can, for all intents and purposes, be treated as a dict.

The format of the actual data in the object is dependent on the API module being queried; see the [API documentation](http://www.mediawiki.org/wiki/API) for more information.