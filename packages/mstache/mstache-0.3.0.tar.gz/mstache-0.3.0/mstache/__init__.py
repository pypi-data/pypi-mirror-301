"""
mstache module.

This module alone implements the entire mstache library, including its
minimal command line interface.

The main functions are considered to be :func:`cli`, :func:`render` and
:func:`stream`, and they expose different approaches to template rendering:
command line interface, buffered and streaming rendering API, respectively.

Other functionality will be considered **advanced**, exposing some
implementation-specific complexity and potentially non-standard behavior
which could reduce compatibility with other mustache implementations and
future major mstache revisions.

"""
"""
mstache, Mustache for Python
============================

See `README.md`_, `project documentation`_ and `project repository`_.

.. _README.md: https://mstache.readthedocs.io/en/latest/README.html
.. _project documentation: https://mstache.readthedocs.io
.. _project repository: https://gitlab.com/ergoithz/mstache


License
-------

Copyright (c) 2021-2024, Felipe A Hernandez.

MIT License (see `LICENSE`_).

.. _LICENSE: https://gitlab.com/ergoithz/mstache/-/blob/master/LICENSE

"""

import codecs
import collections
import collections.abc
import math
import re
import types
import typing

__author__ = 'Felipe A Hernandez'
__email__ = 'ergoithz@gmail.com'
__license__ = 'MIT'
__version__ = '0.3.0'
__all__ = (
    # api
    'tokenize',
    'stream',
    'render',
    'cli',
    # exceptions
    'TokenException',
    'ClosingTokenException',
    'SectionException',
    'UnopenedSectionException',
    'UnclosedSectionException',
    'UnclosedTokenException',
    'DelimiterTokenException',
    'TemplateRecursionError',
    # defaults
    'default_recursion_limit',
    'default_resolver',
    'default_getter',
    'default_strict_getter',
    'default_getter_tuple',
    'default_stringify',
    'default_escape',
    'default_lambda_render',
    'default_tags',
    'default_cache',
    'default_cache_make_key',
    'default_virtuals',
    # types
    'Buffer',
    'TString',
    'PartialResolver',
    'PropertyGetter',
    'PropertyGetterTuple',
    'StringifyFunction',
    'EscapeFunction',
    'LambdaRenderFunctionConstructor',
    'VirtualPropertyFunction',
    'VirtualPropertyMapping',
    'TagsTuple',
    'TagsByteTuple',
    'CompiledToken',
    'CompiledTemplate',
    'CompiledTemplateCache',
    'CacheMakeKeyFunction',
    )

T = typing.TypeVar('T')
"""Generic."""

D = typing.TypeVar('D')
"""Generic."""

Buffer: typing.TypeAlias = str | bytes
"""
String/bytes, string or bytes depending on text or binary mode.

.. versionadded:: 0.3.0

"""

TString = typing.TypeVar('TString', bound=Buffer)
"""String/bytes generic, string or bytes depending on text or binary mode."""

PartialResolver: typing.TypeAlias = collections.abc.Callable[
    [Buffer],
    Buffer | None,
    ]
"""
Template partial resolver function interface.

.. seealso::

    :func:`mstache.default_resolver`
        Default partial resolver stub implementation.

"""

PropertyGetter: typing.TypeAlias = collections.abc.Callable[
    [typing.Any, collections.abc.Sequence, Buffer, T],
    typing.Any | T,
    ]
"""
Template property getter function interface.

.. seealso::

    :func:`mstache.default_getter`
        Default non-strict getter implementation.

    :func:`mstache.default_strict_getter`
        Default strict getter implementation.

"""

PropertyGetterTuple: typing.TypeAlias = (
    tuple[PropertyGetter, PropertyGetter]
    | collections.abc.Sequence[PropertyGetter]
    )
"""
Tuple of property getter functions: non-strict and strict.

.. seealso::

    :attr:`mstache.PropertyGetter`
        Property getter function interface.

    :func:`mstache.default_getter`
        Default non-strict getter implementation.

    :func:`mstache.default_strict_getter`
        Default strict getter implementation.

.. versionaddedd:: 0.3.0

"""

StringifyFunction: typing.TypeAlias = collections.abc.Callable[
    [typing.Any, bool],
    bytes,
    ]
"""
Template variable general stringification function interface.

.. seealso::

    :func:`mstache.default_stringify`
        Default stringify-function implementation.

"""

EscapeFunction: typing.TypeAlias = collections.abc.Callable[[bytes], bytes]
"""Template variable value escape function interface."""

LambdaRenderFunctionConstructor: typing.TypeAlias = collections.abc.Callable[
    ...,
    collections.abc.Callable[..., Buffer],
    ] | None
"""
Lambda render function constructor or :type:`None` for implicit rendering.

Options:

- :type:`collections.abc.Callable` returning another callable which to be sent
  via  ``render`` parameter to explicit (chevron-style) lambdas expecting
  both template content and render parameters.
- :type:`None` enables implicit rendering of lambda return values (spec-style)
  with lambdas only receving the template content as argument.

.. seealso::

    :func:`mstache.default_lambda_render`
        Default explicit lambda render constructor.

.. versionchanged:: 0.3.0
    :type:`None` for implicit return value render.

"""

LambdaRenderFunctionFactory = LambdaRenderFunctionConstructor
"""
.. deprecated:: 0.1.3
    Use :attr:`LambdaRenderFunctionConstructor` instead.

"""

VirtualPropertyFunction: typing.TypeAlias = collections.abc.Callable[
    [typing.Any],
    typing.Any,
    ]
"""Virtual property implementation callable interface."""

VirtualPropertyMapping: typing.TypeAlias = collections.abc.Mapping[
    str,
    VirtualPropertyFunction,
    ]
"""
Virtual property mapping interface.

.. seealso::

    :attr:`mstache.default_virtuals`
        Default mapping of virtual property functions.

"""

TagsTuple: typing.TypeAlias = (
    tuple[Buffer, Buffer]
    | collections.abc.Sequence[Buffer]
    )
"""
Mustache tag tuple interface.

.. seealso::

    :attr:`mstache.default_tags`
        Default tuple of mustache template tags.

"""

TagsByteTuple: typing.TypeAlias = (
    tuple[bytes, bytes]
    | collections.abc.Sequence[bytes]
    )
"""
Mustache tag byte tuple interface.

.. seealso::

    :attr:`mstache.default_tags`
        Default tuple of mustache template tags.

"""

CompiledToken: typing.TypeAlias = tuple[bool, bool, bool, bytes, bytes, int]
"""
Compiled template token.

Tokens are tuples containing a renderer decision path, key, content and flags.

``a: bool``
    Decision for rendering path node ``a``.

``b: bool``
    Decision for rendering path node ``b``.

``c: bool``
    Decision for rendering path node ``c``.

``key: bytes``
    Template substring with token scope key.

``content: bytes``
    Template substring with token content data.

``flags: int``
    Token flags.

    - Unused: ``-1`` (default)
    - Variable flags:
        - ``0`` - escaped
        - ``1`` - unescaped
    - Block start flags:
        - ``0`` - falsy
        - ``1`` - truthy
    - Block end value: block content index.

"""

CompiledTemplate: typing.TypeAlias = tuple[CompiledToken, ...]
"""
Compiled template interface.

.. seealso::

    :attr:`mstache.CompiledToken`
        Item type.

    :attr:`mstache.CompiledTemplateCache`
        Interface exposing this type.

"""


class CompiledTemplateCache(typing.Protocol):
    """
    Cache object protocol.

    .. seealso::

        :attr:`mstache.CompiledTemplate`
            Item type.

        :attr:`mstache.CacheMakeKeyFunction`
            Cache key function interface.

        :attr:`mstache.default_cache`
            Default cache instance.

    """

    def get(self, key: typing.Any) -> CompiledTemplate | None:
        """Get compiled template from key, if any."""

    def __setitem__(self, key: typing.Any, value: CompiledTemplate) -> None:
        """Assign compiled template to key."""


CacheMakeKeyFunction: typing.TypeAlias = collections.abc.Callable[
    [tuple[bytes, bytes, bytes, bool, bool, bool]],
    typing.Any,
    ]
"""
Cache mapping key function interface.

.. seealso::

    :attr:`mstache.CompiledTemplateCache`
        Interface exposing this type.

    :func:`mstache.default_cache_make_key`
        Default implementation of cache make-key function.

"""


class LRUCache(collections.OrderedDict, typing.Generic[T]):
    """Capped mapping discarding least recently used elements."""

    def __init__(self, maxsize: int, *args, **kwargs) -> None:
        """
        Initialize.

        :param maxsize: maximum number of elements will be kept

        Any parameter excess will be passed straight to dict constructor.

        """
        self.maxsize = maxsize
        super().__init__(*args, **kwargs)

    def get(self, key: collections.abc.Hashable, default: D = None) -> T | D:
        """
        Get value for given key or default if not present.

        :param key: hashable
        :param default: value will be returned if key is not present
        :returns: value if key is present, default if not

        """
        try:
            return self[key]
        except KeyError:
            return default  # type: ignore

    def __getitem__(self, key: collections.abc.Hashable) -> T:
        """
        Get value for given key.

        :param key: hashable
        :returns: value if key is present
        :raises KeyError: if key is not present

        """
        self.move_to_end(key)
        return super().__getitem__(key)

    def __setitem__(self, key: collections.abc.Hashable, value: T) -> None:
        """
        Set value for given key.

        :param key: hashable will be used to retrieve values later on
        :param value: value for given key

        """
        super().__setitem__(key, value)
        try:
            self.move_to_end(key)
            while len(self) > self.maxsize:
                self.popitem(last=False)
        except KeyError:  # race condition
            pass


default_recursion_limit = 1024
"""
Default number of maximum nested renders.

A nested render happens whenener the lambda render parameter is used or when
a partial template is injected.

Meant to avoid recursion bombs on templates.

"""

default_tags = b'{{', b'}}'
"""Tuple of default mustache tags as in ``tuple[bytes, bytes]``."""

default_cache: CompiledTemplateCache = LRUCache(1024)
"""
Default template cache mapping, keeping the 1024 most recently used
compiled templates (LRU expiration).
"""

default_cache_make_key: CacheMakeKeyFunction = tuple
"""
Defaut template cache key function, :class:`tuple`, so keys would be
as in ``tuple[bytes, bytes, bytes, bool]`` containing the relevant
:func:`mstache.tokenizer` parameters.
"""


def virtual_length(ref: collections.abc.Sized) -> int:
    """
    Resolve virtual length property.

    :param ref: any non-mapping object implementing ``__len__``
    :returns: number of items
    :raises TypeError: if ref is mapping or has no ``__len__`` method

    """
    if isinstance(ref, collections.abc.Mapping):
        raise TypeError
    return len(ref)


default_virtuals: VirtualPropertyMapping = types.MappingProxyType({
    'length': virtual_length,
    })
"""
Immutable mapping with default virtual properties.

The following virtual properties are implemented:

- **length**, for non-mapping sized objects, returning ``len(ref)``.

"""

TOKEN_TYPES = tuple({
    **dict.fromkeys(range(0x100), (True, False, True, False, False)),
    0x21: (False, False, False, False, False),  # '!'
    0x23: (False, True, True, False, False),  # '#'
    0x26: (True, True, True, True, False),  # '&'
    0x2F: (False, True, False, False, False),  # '/'
    0x3D: (False, False, False, True, True),  # '='
    0x3E: (False, False, True, False, False),  # '>'
    0x5E: (False, True, True, True, False),  # '^'
    0x7B: (True, True, False, True, True),  # '{'
    }.values())
"""
ASCII-indexed tokenizer decision matrix.

``a: bool``
    Decision for tokenization path node ``a``.

``b: bool``
    Decision for tokenization path node ``b``.

``c: bool``
    Decision for tokenization path node ``c``.

``d: bool``
    Decision for tokenization path node ``d``.

``e: bool``
    Three-keyed variable / tag switch for next text start logic.

"""

COMMON_FALSY: tuple = None, False, 0, '', b'', (), [], frozenset(), set()
NON_LOOPING_TYPES: tuple = str, bytes, collections.abc.Mapping
MISSING = object()

RE_TAGS = re.compile(br'[^ ]+')
RE_STANDALONE = re.compile(br'[^\S\r\n]*(\n|\r\n?|$)')
RE_INDENT = re.compile(br'^(?!$)', re.MULTILINE)


class TokenException(SyntaxError):
    """Invalid token found during tokenization."""

    _fmt = 'Invalid tag {tag!r} at line {row} column {column}'

    @classmethod
    def from_template(
            cls,
            template: bytes,
            start: int,
            end: int | None = None,
            ) -> 'TokenException':
        """
        Create exception instance from parsing data.

        :param template: template bytes
        :param start: character position where the offending tag starts at
        :param end: character position where the offending tag ends at
        :returns: exception instance

        """
        tag = template[start:end].decode(errors='replace')
        row = 1 + template[:start].count(b'\n')
        column = 1 + start - max(0, template.rfind(b'\n', 0, start))
        return cls(cls._fmt.format(tag=tag, row=row, column=column))


class SectionException(TokenException):
    """
    Section error found during tokenization.

    .. versionadded:: 0.3.0

    """

    _fmt = 'Non-matching tag {tag!r} at line {row} column {column}'


ClosingTokenException = SectionException
"""

.. deprecated:: 0.3.0
    Use :attr:`SectionException` instead.


"""


class UnopenedSectionException(SectionException):
    """
    Closing unknown section during tokenization.

    .. versionadded:: 0.3.0

    """

    _fmt = 'Unopened section {tag!r} at line {row} column {column}'


class UnclosedSectionException(SectionException):
    """
    Section left unclosed during tokenization.

    .. versionadded:: 0.3.0

    """

    _fmt = 'Unclosed section {tag!r} at line {row} column {column}'


class UnclosedTokenException(TokenException):
    """Token left unclosed during tokenization."""

    _fmt = 'Unclosed token {tag!r} at line {row} column {column}'


class DelimiterTokenException(TokenException):
    """
    Invalid delimiters token found during tokenization.

    .. versionadded:: 0.1.1

    """

    _fmt = 'Invalid delimiters {tag!r} at line {row} column {column}'


class TemplateRecursionError(RecursionError):
    """Template rendering exceeded maximum render recursion."""


def default_stringify(data: typing.Any, text: bool) -> bytes:
    """
    Convert arbitrary data to bytes.

    :param data: value will be serialized
    :param text: whether running in text mode or not (bytes mode)
    :returns: template bytes

    .. versionchanged:: 0.3.0
       ``None`` to emit empty bytes

    """
    return (
        b'' if data is None else
        str(data).encode() if text or not isinstance(data, bytes) else
        data
        )


def default_escape(data: bytes) -> bytes:
    """
    Convert bytes conflicting with HTML to their escape sequences.

    :param data: bytes containing text
    :returns: escaped text bytes

    """
    return (
        data
        .replace(b'&', b'&amp;')
        .replace(b'<', b'&lt;')
        .replace(b'>', b'&gt;')
        .replace(b'"', b'&quot;')
        .replace(b"'", b'&#x60;')
        .replace(b'`', b'&#x3D;')
        )


def default_resolver(name: typing.Any) -> None:
    """
    Mustache partial resolver function (stub).

    :param name: partial template name
    :returns: None

    """


def getter_resolve_binary(
        scope: typing.Any,
        components: collections.abc.Sequence[bytes],
        virtuals: VirtualPropertyMapping,
        default: typing.Any = None,
        ) -> tuple[bool, bool, typing.Any]:
    """
    Resolve binary component sequence from scope object.

    :param scope: current object scope to resolve from
    :param component: sequence of reference path components
    :param virtuals: mapping if virtual property getters
    :param default: value will be used as default when missing
    :returns: tuple with success (bool), recursed (bool) and result

    .. versionadded:: 0.3.0

    """
    recursed = False
    for name in components:
        try:
            scope = scope[name]
            recursed = True
            continue
        except (KeyError, TypeError, AttributeError):
            pass
        try:
            name = name.decode()  # type: ignore
        except UnicodeDecodeError:
            return False, recursed, default
        try:
            scope = scope[name]
            recursed = True
            continue
        except (KeyError, TypeError, AttributeError):
            pass
        if name.isdigit():
            try:
                scope = scope[int(name)]
                recursed = True
                continue
            except (TypeError, KeyError, IndexError):
                pass
        else:
            try:
                scope = getattr(scope, name)  # type: ignore
                recursed = True
                continue
            except AttributeError:
                pass
        try:
            scope = virtuals[name](scope)  # type: ignore
            recursed = True
            continue
        except (KeyError, TypeError, AttributeError):
            pass
        return False, recursed, default
    return True, True, scope


def getter_resolve(
        scope: typing.Any,
        components: collections.abc.Sequence[str],
        virtuals: VirtualPropertyMapping,
        default: typing.Any = None,
        ) -> tuple[bool, bool, typing.Any]:
    """
    Resolve component sequence from scope object.

    :param scope: current object scope to resolve from
    :param component: sequence of reference path components
    :param virtuals: mapping if virtual property getters
    :param default: value will be used as default when missing
    :returns: tuple with success (bool), recursed (bool) and result

    .. versionadded:: 0.3.0

    """
    recursed = False
    for name in components:
        try:
            scope = scope[name]
            recursed = True
            continue
        except (KeyError, TypeError, AttributeError):
            pass
        if name.isdigit():
            try:
                scope = scope[int(name)]
                recursed = True
                continue
            except (TypeError, KeyError, IndexError):
                pass
        else:
            try:
                scope = getattr(scope, name)  # type: ignore
                recursed = True
                continue
            except AttributeError:
                pass
        try:
            scope = virtuals[name](scope)  # type: ignore
            recursed = True
            continue
        except (KeyError, TypeError, AttributeError):
            pass
        return False, recursed, default
    return True, True, scope


def default_getter(
        scope: typing.Any,
        scopes: collections.abc.Sequence,
        key: Buffer,
        default: typing.Any = None,
        *,
        virtuals: VirtualPropertyMapping = default_virtuals,
        ) -> typing.Any:
    """
    Extract property value from scope hierarchy retrying until full match.

    :param scope: uppermost scope (corresponding to key ``'.'``)
    :param scopes: parent scope sequence
    :param key: property key
    :param default: value will be used as default when missing
    :param virtuals: mapping of virtual property callables
    :param strict: disable compatibility workarounds
    :returns: value from scope or default

    Both :class:`AttributeError` and :class:`TypeError` exceptions
    raised by virtual property implementations will be handled as if
    that property doesn't exist, which can be useful to filter out
    incompatible types.

    .. versionadded:: 0.1.3
       **virtuals** parameter.

    """
    if key in (b'.', '.'):
        return scope

    components, resolve = (
        (key.split('.'), getter_resolve) if isinstance(key, str) else
        (key.split(b'.'), getter_resolve_binary)
        )

    m, _, res = resolve(scope, components, virtuals)  # type: ignore
    if m:
        return res

    for ref in reversed(scopes):
        m, _, res = resolve(ref, components, virtuals)  # type: ignore
        if m:
            return res

    return default


def default_strict_getter(
        scope: typing.Any,
        scopes: collections.abc.Sequence,
        key: Buffer,
        default: typing.Any = None,
        *,
        virtuals: VirtualPropertyMapping = default_virtuals,
        ) -> typing.Any:
    """
    Extract property value from scope hierarchy retrying until partial match.

    :param scope: uppermost scope (corresponding to key ``'.'``)
    :param scopes: parent scope sequence
    :param key: property key
    :param default: value will be used as default when missing
    :param virtuals: mapping of virtual property callables
    :returns: value from scope or default

    Both :class:`AttributeError` and :class:`TypeError` exceptions
    raised by virtual property implementations will be handled as if
    that property doesn't exist, which can be useful to filter out
    incompatible types.

    .. versionadded:: 0.3.0

    """
    if key in (b'.', '.'):
        return scope

    components, resolve = (  # type: ignore
        (key.split('.'), getter_resolve) if isinstance(key, str) else
        (key.split(b'.'), getter_resolve_binary)
        )

    _, m, res = resolve(scope, components, virtuals, default)  # type: ignore
    if m:
        return res

    for ref in reversed(scopes):
        _, m, res = resolve(ref, components, virtuals, default)  # type: ignore
        if m:
            return res

    return default


default_getter_tuple = default_getter, default_strict_getter
"""
Tuple with each getter function for compatibility and strict modes.

Items:

- Reference to :func:`default_getter` used in non-strict mode.
- Reference to :func:`default_strict_getter` used in strict mode..

.. seealso::

    :func:`default_getter`
        Default getter implementation referenced by this tuple.

.. versionadded:: 0.3.0

"""


def default_lambda_render(
        scope: typing.Any,
        **kwargs,
        ) -> collections.abc.Callable[[TString], TString]:
    r"""
    Generate a template-only render function with fixed parameters.

    :param scope: current scope
    :param \**kwargs: parameters forwarded to :func:`render`
    :returns: template render function

    """

    def lambda_render(template: TString) -> TString:
        """
        Render given template to string/bytes.

        :param template: template text
        :returns: rendered string or bytes (depending on template type)

        """
        return render(template, scope, **kwargs)

    return lambda_render


def decode_tags(start_tag: Buffer, end_tag: Buffer) -> TagsByteTuple:
    """
    Convert tag delimiters to bytes.

    :param start_tag: tag start delimiter
    :param end_tag: tag end delimiter
    :returns: tuple with delimiters as bytes

    .. versionadded:: 0.3.0

    """
    return (
        start_tag.encode() if isinstance(start_tag, str) else start_tag,
        end_tag.encode() if isinstance(end_tag, str) else end_tag,
        )


def tokenize(
        template: bytes,
        *,
        tags: TagsByteTuple = default_tags,
        comments: bool = False,
        cache: CompiledTemplateCache = default_cache,
        cache_make_key: CacheMakeKeyFunction = default_cache_make_key,
        keep_lines: bool = False,
        strict: bool = False,
        ) -> CompiledTemplate:
    """
    Compile mustache template as a tuple of token tuples.

    :param template: template as utf-8 encoded bytes
    :param tags: mustache tag tuple (open, close)
    :param comments: whether yield comment tokens or not (ignore comments)
    :param cache: mutable mapping for compiled template cache
    :param cache_make_key: key function for compiled template cache
    :param keep_lines: disable mustache tag-only-line collapsing
    :param strict: disable compatibility workarounds
    :returns: tuple of token tuples

    :raises UnclosedSectionException: if section is left unclosed
    :raises UnopenedSectionException: if closing an invalid section
    :raises UnclosedTokenException: if tag is left unclosed
    :raises DelimiterTokenException: if delimiter token syntax is invalid

    .. versionadded:: 0.3.0
        **keep_lines** to disable tag-only-line collapsing,
        **strict** to disable compatability workarounds

    """
    start_tag, end_tag = tags

    if cached := cache.get(tokenization_key := cache_make_key(
            (template, start_tag, end_tag, comments, keep_lines, strict),
            )):
        return cached

    template_find = template.find
    tags_find = RE_TAGS.findall

    stack: list[tuple[bytes | None, int, int, int]] = []
    stack_append = stack.append
    stack_pop = stack.pop
    scope_label = None
    scope_head = 0
    scope_start = 0
    scope_index = 0

    indent = b''
    standalone = RE_STANDALONE.match
    linebreaks = b'\r', b'\n'

    end_literal = b'}' + end_tag
    end_switch = b'=' + end_tag
    start_len = len(start_tag)
    end_len = len(end_tag)

    token_types = TOKEN_TYPES
    recording: list[CompiledToken] = []
    record = recording.append

    text_start = 0
    while (text_end := template_find(start_tag, text_start)) != -1:
        tag_start = text_end + start_len
        try:
            a, b, c, d, e = token_types[template[tag_start]]
        except IndexError:
            raise UnclosedTokenException.from_template(
                template=template,
                start=text_end,
                ) from None

        if a:  # variables
            tag_start += b

            if text_start < text_end:  # inline text
                tail = template[text_start:text_end]
                record((False, True, True, b'', tail, -1))

            if c:  # variable
                tag_end = template_find(end_tag, tag_start)
                text_start = tag_end + end_len

            else:  # triple-keyed variable
                tag_end = template_find(end_literal, tag_start)
                text_start = tag_end + end_len + 1

            if tag_end < 0:
                raise UnclosedTokenException.from_template(
                    template=template,
                    start=text_end,
                    )

            record((
                False, True, False,
                template[tag_start:tag_end].strip(), b'', d,
                ))

            continue

        tag_start += 1
        cur_start = text_start

        if e:
            tag_end = template_find(end_switch, tag_start)
            text_start = tag_end + end_len + 1
        else:
            tag_end = template_find(end_tag, tag_start)
            text_start = tag_end + end_len

        if tag_end < 0:
            raise UnclosedTokenException.from_template(
                template=template,
                start=text_end,
                )

        if keep_lines:
            if cur_start < text_end:  # inline text
                tail = template[cur_start:text_end]
                record((False, True, True, b'', tail, -1))
        elif wholeline := standalone(template, text_start):
            if cur_start < text_end:
                tail = template[cur_start:text_end]
                trimmed = tail.rstrip(b' ')
                if not trimmed and not cur_start:  # start standalone
                    text_start = wholeline.end()
                    indent = tail
                elif trimmed.endswith(linebreaks):  # linebreak standalone
                    record((False, True, True, b'', trimmed, -1))
                    text_start = wholeline.end()
                    indent = tail[len(trimmed):]
                else:
                    record((False, True, True, b'', tail, -1))
                    indent = b''
            else:
                text_start = wholeline.end()
                indent = b''
        elif cur_start < text_end:
            tail = template[cur_start:text_end]
            record((False, True, True, b'', tail, -1))
            indent = b''
        else:
            indent = b''

        if b:  # block

            if c:  # open
                stack_append((scope_label, text_end, scope_start, scope_index))
                scope_label = template[tag_start:tag_end].strip()
                scope_head = text_end
                scope_start = text_start
                scope_index = len(recording) + 1
                record((
                    True, False, True,
                    scope_label, b'', d,
                    ))

            elif scope_label == template[tag_start:tag_end].strip():  # close
                record((
                    True, True, True,
                    scope_label,  # type: ignore
                    template[scope_start:text_end].strip(),
                    scope_index,
                    ))
                scope_label, scope_head, scope_start, scope_index = stack_pop()

            else:
                raise UnopenedSectionException.from_template(
                    template=template,
                    start=text_end,
                    end=text_start,
                    )

        elif c:  # partial
            record((
                True, False, False,
                template[tag_start:tag_end].strip(), indent, -1,
                ))

        elif d:  # tags
            try:
                start_tag, end_tag = (
                    tags_find(template, tag_start, tag_end) if strict else
                    tags_find(template, tag_start, tag_end)[:2]
                    )
            except ValueError:
                raise DelimiterTokenException.from_template(
                    template=template,
                    start=tag_start,
                    end=tag_end,
                    ) from None

            end_literal = b'}' + end_tag
            end_switch = b'=' + end_tag
            start_len = len(start_tag)
            end_len = len(end_tag)

            record((
                False, False, True,
                start_tag, end_tag, -1,
                ))

        elif comments:  # comment
            record((
                False, False, False,
                b'', template[tag_start:tag_end].strip(), -1,
                ))

    if stack:
        raise UnclosedSectionException.from_template(
            template=template,
            start=scope_head,
            end=scope_start,
            )

    if (tail := template[text_start:]) or not recording:   # text
        record((
            False, True, True,
            b'', tail, -1,
            ))

    tokens = cache[tokenization_key] = tuple(recording)
    return tokens


def process(
        template: bytes,
        scope: typing.Any,
        *,
        scopes: collections.abc.Iterable = (),
        resolver: PartialResolver = default_resolver,
        getter: PropertyGetter | PropertyGetterTuple = default_getter_tuple,
        stringify: StringifyFunction = default_stringify,
        escape: EscapeFunction = default_escape,
        lambda_render: LambdaRenderFunctionConstructor = default_lambda_render,
        tags: TagsByteTuple = default_tags,
        cache: CompiledTemplateCache = default_cache,
        cache_make_key: CacheMakeKeyFunction = default_cache_make_key,
        recursion_limit: int = default_recursion_limit,
        keep_lines: bool = False,
        strict: bool = False,
        text: bool = False,
        ) -> collections.abc.Generator[bytes, None, None]:
    """
    Generate rendered mustache template byte chunks.

    :param template: mustache template string
    :param scope: root object used as root mustache scope
    :param scopes: iterable of parent scopes
    :param resolver: callable will be used to resolve partials (bytes)
    :param getter: callable will be used to pick variables from scope
    :param stringify: callable will be used to render python types (bytes)
    :param escape: callable will be used to escape template (bytes)
    :param lambda_render: explicit lambda render function constructor
    :param tags: mustache tag tuple (open, close)
    :param cache: mutable mapping for compiled template cache
    :param cache_make_key: key function for compiled template cache
    :param recursion_limit: maximum number of nested render operations
    :param keep_lines: disable mustache tag-only-line collapsing
    :param strict: disable compatibility workarounds
    :param text: toggle str/bytes mode
    :returns: byte chunk generator

    :raises UnclosedSectionException: if section is left unclosed
    :raises UnopenedSectionException: if closing an invalid section
    :raises UnclosedTokenException: if tag is left unclosed
    :raises DelimiterTokenException: if delimiter token syntax is invalid
    :raises TemplateRecursionError: if rendering recursion limit is exceeded

    .. versionadded:: 0.3.0
        **getter** support for :type:`mstache.PropertyGetterTuple`,
        **keep_lines** to disable tag-only-line collapsing,
        **strict** to disable compatability workarounds

    """
    if recursion_limit < 0:
        message = 'Template rendering exceeded maximum render recursion'
        raise TemplateRecursionError(message)

    # current context
    recursion_left = recursion_limit - 1
    current_tags = tags
    items: collections.abc.Iterator | None = None
    callback = False
    silent = False

    # context stack
    stack: list[tuple[collections.abc.Iterator | None, bool, bool]] = []
    stack_append = stack.append
    stack_pop = stack.pop

    # scope stack
    scopes = list(scopes)
    scopes_append = scopes.append
    scopes_pop = scopes.pop

    # locals
    templ = Buffer
    decode: typing.Callable[[bytes], Buffer] = (
        bytes.decode if text else  # type: ignore
        bytes
        )
    implicit_render = lambda_render is None
    miss = MISSING
    falsies = COMMON_FALSY
    non_looping = NON_LOOPING_TYPES
    isnan = math.isnan
    mappings = collections.abc.Mapping
    indent_sub = RE_INDENT.sub
    getv = getter if callable(getter) else getter[strict]

    start = 0
    tokens = tokenized = tokenize(
        template,
        tags=tags,
        cache=cache,
        cache_make_key=cache_make_key,
        keep_lines=keep_lines,
        strict=strict,
        )
    while True:
        for a, b, c, token_name, token_content, token_option in tokens:
            if silent:
                if a:
                    if b:  # close / loop
                        closing_scope = scope
                        closing_callback = callback

                        scope = scopes_pop()
                        items, callback, silent = stack_pop()

                        if closing_callback and not silent:  # lambda block
                            content = decode(token_content)

                            if implicit_render:  # mustache lambda
                                value = closing_scope(content)  # type: ignore
                                if value and isinstance(value, templ):
                                    yield from process(
                                        template=(
                                            value.encode()
                                            if isinstance(value, str) else
                                            value
                                            ),
                                        scope=scope,
                                        scopes=scopes,
                                        resolver=resolver,
                                        getter=getter,
                                        stringify=stringify,
                                        escape=escape,
                                        lambda_render=lambda_render,
                                        tags=current_tags,
                                        cache=cache,
                                        cache_make_key=cache_make_key,
                                        recursion_limit=recursion_left,
                                        keep_lines=keep_lines,
                                        strict=strict,
                                        text=text,
                                        )
                                elif value := stringify(value, text):
                                    yield value

                            elif value := stringify(  # chevron lambda
                                    closing_scope(  # type: ignore
                                        content,
                                        lambda_render(  # type: ignore
                                            scope=scope,
                                            scopes=scopes,
                                            resolver=resolver,
                                            getter=getter,
                                            stringify=stringify,
                                            escape=escape,
                                            lambda_render=lambda_render,
                                            tags=current_tags,
                                            cache=cache,
                                            cache_make_key=cache_make_key,
                                            recursion_limit=recursion_left,
                                            keep_lines=keep_lines,
                                            strict=strict,
                                            ),
                                        ),
                                    text,
                                    ):
                                yield value

                    elif c:  # block
                        scopes_append(scope)
                        stack_append((items, callback, silent))

            elif a:
                if b:  # close / loop
                    if items and (scope := next(items, miss)) is not miss:
                        callback = callable(scope)
                        silent = callback

                        if start != token_option:
                            start = token_option
                            tokens = tokenized[start:]

                        break  # restart

                    scope = scopes_pop()
                    items, callback, silent = stack_pop()

                elif c:  # block
                    curr = scope
                    scope = getv(curr, scopes, decode(token_name), None)
                    scopes_append(curr)
                    stack_append((items, callback, silent))

                    falsy = (
                        hasattr(scope, '__float__') and isnan(scope)
                        if scope else
                        scope in falsies or not isinstance(scope, mappings)
                        )
                    if token_option:  # falsy block
                        items = None
                        callback = False
                        silent = not falsy

                    elif falsy:  # truthy block with falsy value
                        items = None
                        callback = False
                        silent = True

                    elif (  # loop
                            hasattr(scope, '__iter__')
                            and not isinstance(scope, non_looping)
                            ):
                        items = iter(scope)

                        if (  # loop item
                                scope := next(items, miss)  # type: ignore
                                ) is not miss:
                            callback = callable(scope)
                            silent = callback

                        else:  # loop exhausted
                            items = None
                            scope = None
                            callback = False
                            silent = True

                    else:  # truthy block with truthy value
                        items = None
                        callback = callable(scope)
                        silent = callback

                elif value := resolver(decode(token_name)):  # partial
                    content = (
                        value.encode() if isinstance(value, str) else
                        value
                        )
                    yield from process(
                        template=(
                            indent_sub(token_content, content)
                            if token_content else
                            content
                            ),
                        scope=scope,
                        scopes=scopes,
                        resolver=resolver,
                        getter=getter,
                        stringify=stringify,
                        escape=escape,
                        lambda_render=lambda_render,
                        tags=tags,
                        cache=cache,
                        cache_make_key=cache_make_key,
                        recursion_limit=recursion_left,
                        keep_lines=keep_lines,
                        strict=strict,
                        text=text,
                        )

            elif b:
                if c:  # text
                    yield token_content

                elif (  # variable
                        value := getv(scope, scopes, decode(token_name), miss)
                        ) is not miss:

                    if (  # lambda variable
                            callable(value)
                            and (value := value())
                            and isinstance(value, templ)
                            ):
                        content = (
                            value.encode() if isinstance(value, str) else
                            value
                            )
                        yield from process(
                            template=(
                                content if token_option else
                                escape(content)
                                ),
                            scope=scope,
                            scopes=scopes,
                            resolver=resolver,
                            getter=getter,
                            stringify=stringify,
                            escape=escape,
                            lambda_render=lambda_render,
                            tags=tags,
                            cache=cache,
                            cache_make_key=cache_make_key,
                            recursion_limit=recursion_left,
                            keep_lines=keep_lines,
                            strict=strict,
                            text=text,
                            )

                    elif value := stringify(value, text):
                        yield value if token_option else escape(value)

            elif c:  # tags
                current_tags = token_name, token_content

            # else comment

        else:
            break


def stream(
        template: TString,
        scope: typing.Any,
        *,
        scopes: collections.abc.Iterable = (),
        resolver: PartialResolver = default_resolver,
        getter: PropertyGetter | PropertyGetterTuple = default_getter_tuple,
        stringify: StringifyFunction = default_stringify,
        escape: EscapeFunction = default_escape,
        lambda_render: LambdaRenderFunctionConstructor = default_lambda_render,
        tags: TagsTuple = default_tags,
        cache: CompiledTemplateCache = default_cache,
        cache_make_key: CacheMakeKeyFunction = default_cache_make_key,
        recursion_limit: int = default_recursion_limit,
        keep_lines: bool = False,
        strict: bool = False,
        ) -> collections.abc.Generator[TString, None, None]:
    """
    Generate rendered mustache template chunks.

    :param template: mustache template (str or bytes)
    :param scope: current rendering scope (data object)
    :param scopes: list of precedent scopes
    :param resolver: callable will be used to resolve partials (bytes)
    :param getter: callable will be used to pick variables from scope
    :param stringify: callable will be used to render python types (bytes)
    :param escape: callable will be used to escape template (bytes)
    :param lambda_render: explicit lambda render function constructor
    :param tags: tuple (start, end) specifying the initial mustache delimiters
    :param cache: mutable mapping for compiled template cache
    :param cache_make_key: key function for compiled template cache
    :param recursion_limit: maximum number of nested render operations
    :param keep_lines: disable mustache tag-only-line collapsing
    :param strict: disable compatibility workarounds
    :returns: generator of bytes/str chunks (type depends on template)

    :raises UnclosedSectionException: if section is left unclosed
    :raises UnopenedSectionException: if closing an invalid section
    :raises UnclosedTokenException: if tag is left unclosed
    :raises DelimiterTokenException: if delimiter token syntax is invalid
    :raises TemplateRecursionError: if rendering recursion limit is exceeded

    .. versionadded:: 0.3.0
       **getter** support for :attr:`mstache.PropertyGetterTuple`,
       **keep_lines** to disable block-line stripping,
       **strict** to disable compatability workarounds

    """
    text = isinstance(template, str)
    data = process(
        template=template.encode() if text else template,  # type: ignore
        scope=scope,
        scopes=scopes,
        resolver=resolver,
        getter=getter,
        stringify=stringify,
        escape=escape,
        lambda_render=lambda_render,
        tags=decode_tags(*tags),
        cache=cache,
        cache_make_key=cache_make_key,
        recursion_limit=recursion_limit,
        keep_lines=keep_lines,
        strict=strict,
        text=text,
        )
    return codecs.iterdecode(data, 'utf8') if text else data  # type: ignore


def render(
        template: TString,
        scope: typing.Any,
        *,
        scopes: collections.abc.Iterable = (),
        resolver: PartialResolver = default_resolver,
        getter: PropertyGetter | PropertyGetterTuple = default_getter_tuple,
        stringify: StringifyFunction = default_stringify,
        escape: EscapeFunction = default_escape,
        lambda_render: LambdaRenderFunctionConstructor = default_lambda_render,
        tags: TagsTuple = default_tags,
        cache: CompiledTemplateCache = default_cache,
        cache_make_key: CacheMakeKeyFunction = default_cache_make_key,
        recursion_limit: int = default_recursion_limit,
        keep_lines: bool = False,
        strict: bool = False,
        ) -> TString:
    """
    Render mustache template.

    :param template: mustache template
    :param scope: current rendering scope (data object)
    :param scopes: list of precedent scopes
    :param resolver: callable will be used to resolve partials (bytes)
    :param getter: callable will be used to pick variables from scope
    :param stringify: callable will be used to render python types (bytes)
    :param escape: callable will be used to escape template (bytes)
    :param lambda_render: explicit lambda render function constructor
    :param tags: tuple (start, end) specifying the initial mustache delimiters
    :param cache: mutable mapping for compiled template cache
    :param cache_make_key: key function for compiled template cache
    :param recursion_limit: maximum number of nested render operations
    :param keep_lines: disable mustache tag-only-line collapsing
    :param strict: disable compatibility workarounds
    :returns: rendered bytes/str (type depends on template)

    :raises UnclosedSectionException: if section is left unclosed
    :raises UnopenedSectionException: if closing an invalid section
    :raises UnclosedTokenException: if tag is left unclosed
    :raises DelimiterTokenException: if delimiter token syntax is invalid
    :raises TemplateRecursionError: if rendering recursion limit is exceeded

    .. versionadded:: 0.3.0
       **getter** support for :attr:`mstache.PropertyGetterTuple`,
       **keep_lines** to disable tag-only-line collapsing,
       **strict** to disable compatability workarounds

    """
    text = isinstance(template, str)
    data = b''.join(process(
        template=template.encode() if text else template,  # type: ignore
        scope=scope,
        scopes=scopes,
        resolver=resolver,
        getter=getter,
        stringify=stringify,
        escape=escape,
        lambda_render=lambda_render,
        tags=decode_tags(*tags),
        cache=cache,
        cache_make_key=cache_make_key,
        recursion_limit=recursion_limit,
        keep_lines=keep_lines,
        strict=strict,
        text=text,
        ))
    return data.decode() if text else data  # type: ignore


def cli(argv: collections.abc.Sequence[str] | None = None) -> None:
    """
    Render template from command line.

    Use ``python -m mstache --help`` to check available options.

    :param argv: command line arguments, :attr:`sys.argv` when None

    """
    import argparse
    import json
    import sys

    arguments = argparse.ArgumentParser(
        description='Render mustache template.',
        )
    arguments.add_argument(
        'template',
        metavar='PATH',
        type=argparse.FileType('r'),
        help='template file',
        )
    arguments.add_argument(
        '-j', '--json',
        metavar='PATH',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help='JSON file, default: stdin',
        )
    arguments.add_argument(
        '-o', '--output',
        metavar='PATH',
        type=argparse.FileType('w'),
        default=sys.stdout,
        help='output file, default: stdout',
        )
    arguments.add_argument(
        '-k', '--keep-lines',
        action='store_true',
        help='disable mustache tag-only-line collapsing',
        )
    args = arguments.parse_args(argv)
    try:
        args.output.write(render(
            args.template.read(),
            json.load(args.json),
            keep_lines=args.keep_lines,
            ))
    finally:
        args.template.close()
        for fd, std in ((args.json, sys.stdin), (args.output, sys.stdout)):
            if fd is not std:
                fd.close()


if __name__ == '__main__':
    cli()
