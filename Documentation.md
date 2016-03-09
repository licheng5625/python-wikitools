This page gives a brief overview of the structure of wikitools, including modules, objects, and exceptions. Functions, methods, and member variables are detailed on the linked pages. The section headers are links to documentation for the modules.


# api #
[api](api.md)
## Objects ##
  * [APIRequest](APIRequest.md)
  * [APIResult](APIResult.md)
  * [APIListResult](APIListResult.md)

## Exceptions ##
  * [APIError](APIError.md)
  * [APIDisabled](APIDisabled.md)

# wiki #
[wiki](wiki.md)
## Objects ##
  * [Wiki](Wiki.md)
  * [Namespace](Namespace.md)
  * [WikiCookieJar](WikiCookieJar.md)

## Exceptions ##
  * [WikiError](WikiError.md) - A base class for all errors related to the wiki and wiki pages
  * [CookiesExpired](CookiesExpired.md) - Raised if trying to login from previously stored cookies that are too old.

# page #
[page](page.md)
## Objects ##
  * [Page](Page.md)

## Exceptions ##
  * [BadTitle](BadTitle.md) - A subclass of WikiError, raised if trying to query information about an invalid page title
  * [NoPage](NoPage.md) - A subclass of WikiError, raised if trying to modify or query information about a non-existent page
  * [BadNamespace](BadNamespace.md) - A subclass of WikiError, raised if trying to create a Page object with a non-existent namespace index.
  * [EditError](EditError.md) - A subclass of WikiError, raised by certain incorrect argument usages in the edit method
  * [ProtectError](ProtectError.md) - A subclass of WikiError, raised by certain incorrect argument usages in the protect method

# user #
[user](user.md)
## Objects ##
  * [User](User.md)

## Exceptions ##
_none_

# category #
[category](category.md)
## Objects ##
  * [Category](Category.md)

## Exceptions ##
_none_

# wikifile #
[wikifile](wikifile.md)
## Objects ##
  * [File](File.md)

## Exceptions ##
  * [FileDimensionError](FileDimensionError.md) - A subclass of WikiError, raised if trying to specify a width and a height if downloading an image
  * [UploadError](UploadError.md) - A subclass of WikiError, raised by certain incorrect argument usages in the upload method


# pagelist #
[pagelist](pagelist.md)
## Objects ##
_none_
## Exceptions ##
_none_