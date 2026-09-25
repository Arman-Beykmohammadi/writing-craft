"""JavaScript-compatibility helpers shared by the aiw_* ports.

The ports in this folder reproduce the avoid-ai-writing Node tools
(https://github.com/conorbronsdon/avoid-ai-writing, v3.36.0, MIT License,
Copyright (c) 2026 Conor Bronsdon) byte for byte. These helpers carry the
JavaScript semantics that Python does not share:

* Strings are handled as UTF-16 code units ("u16 strings"): an astral
  character is stored as two surrogate code points, so len(), indexes and
  regex repetition counts match JavaScript's String and non-/u RegExp.
* JS regex sources are translated to Python re: JS whitespace for \\s,
  ASCII \\w/\\d/\\b, line-terminator aware ^ $ and ., end-of-input $.
* Math.round, Number.prototype.toFixed and JSON.stringify output.

Standard library only; Python 3.9 compatible.
"""

import math
import re
from decimal import ROUND_HALF_UP, Decimal

# JS WhiteSpace + LineTerminator, the set behind \s, trim() and split(/\s+/).
JS_WS_CHARS = (
    '\t\n\x0b\x0c\r \xa0        '
    '        　﻿'
)
_WS_CLASS = (
    '\\t\\n\\x0b\\x0c\\r \\xa0\\u1680\\u2000-\\u200a\\u2028\\u2029'
    '\\u202f\\u205f\\u3000\\ufeff'
)
_LT_CLASS = '\\n\\r\\u2028\\u2029'
WS = '[' + _WS_CLASS + ']'
NOT_WS = '[^' + _WS_CLASS + ']'
LT = '[' + _LT_CLASS + ']'
# Multiline ^ and $ as JavaScript defines them (any line terminator).
LINE_START = '(?:\\A|(?<=' + LT + '))'
LINE_END = '(?=' + LT + '|\\Z)'

_ASTRAL = re.compile('[\U00010000-\U0010ffff]')
_SURROGATE = re.compile('[\ud800-\udfff]')


def _pair(match):
    cp = ord(match.group(0)) - 0x10000
    return chr(0xD800 + (cp >> 10)) + chr(0xDC00 + (cp & 0x3FF))


def to_u16(s):
    """Split astral characters into surrogate pairs (JS string view)."""
    return _ASTRAL.sub(_pair, s)


def from_u16(s):
    """Join surrogate pairs back into characters; lone surrogates stay."""
    if not _SURROGATE.search(s):
        return s
    return s.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


def js_truthy(v):
    """JavaScript truthiness for the values these ports receive."""
    if v is None or v is UNDEFINED or v is False:
        return False
    if isinstance(v, (int, float)) and (v == 0 or v != v):
        return False
    if isinstance(v, str) and v == '':
        return False
    return True


def js_trim(s):
    return s.strip(JS_WS_CHARS)


def js_trim_start(s):
    return s.lstrip(JS_WS_CHARS)


def js_trim_end(s):
    return s.rstrip(JS_WS_CHARS)


def js_lower(s):
    """String.prototype.toLowerCase on a u16 string."""
    if _SURROGATE.search(s):
        return to_u16(from_u16(s).lower())
    return s.lower()


def js_round(x):
    """Math.round: halves round toward +infinity."""
    f = math.floor(x)
    return f + 1 if x - f >= 0.5 else f


def js_to_fixed(x, digits):
    """Number.prototype.toFixed: exact decimal value, ties away from zero."""
    if x == 0:
        x = 0.0
    if x != x:
        return 'NaN'
    if abs(x) >= 1e21:
        return js_number(x)
    q = Decimal(x).quantize(Decimal(1).scaleb(-digits), rounding=ROUND_HALF_UP)
    return '{:f}'.format(q)


def js_number(x):
    """Number.prototype.toString for the values JSON.stringify prints."""
    if isinstance(x, bool):
        return 'true' if x else 'false'
    if isinstance(x, int):
        return str(x)
    if x != x or x in (float('inf'), float('-inf')):
        return 'null'
    if x == 0:
        return '0'
    sign = '-' if x < 0 else ''
    r = repr(abs(x))
    mant, _, exp = r.partition('e')
    exp = int(exp) if exp else 0
    ip, _, fp = mant.partition('.')
    digits = ip + fp
    point = len(ip) + exp
    stripped = digits.lstrip('0')
    point -= len(digits) - len(stripped)
    digits = stripped.rstrip('0') or '0'
    k, n = len(digits), point
    if k <= n <= 21:
        body = digits + '0' * (n - k)
    elif 0 < n <= 21:
        body = digits[:n] + '.' + digits[n:]
    elif -6 < n <= 0:
        body = '0.' + '0' * (-n) + digits
    else:
        e = n - 1
        esign = '+' if e >= 0 else '-'
        body = digits[0] + ('.' + digits[1:] if k > 1 else '') + 'e' + esign + str(abs(e))
    return sign + body


class _Undefined(object):
    """Marker for a JS `undefined` property: JSON.stringify omits it."""

    def __repr__(self):
        return 'undefined'


UNDEFINED = _Undefined()

_ESCAPES = {'"': '\\"', '\\': '\\\\', '\b': '\\b', '\f': '\\f', '\n': '\\n', '\r': '\\r', '\t': '\\t'}


def js_quote(s):
    """JSON.stringify string quoting over a u16 string (well-formed JSON)."""
    out = ['"']
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        o = ord(c)
        if c in _ESCAPES:
            out.append(_ESCAPES[c])
        elif o < 0x20:
            out.append('\\u%04x' % o)
        elif 0xD800 <= o <= 0xDBFF and i + 1 < n and 0xDC00 <= ord(s[i + 1]) <= 0xDFFF:
            out.append(from_u16(c + s[i + 1]))
            i += 1
        elif 0xD800 <= o <= 0xDFFF:
            out.append('\\u%04x' % o)
        else:
            out.append(c)
        i += 1
    out.append('"')
    return ''.join(out)


def js_stringify(value, indent=2):
    """JSON.stringify(value, null, indent) for dict/list/str/number/bool/None."""
    pad = ' ' * indent if indent else ''

    def enc(v, level):
        if v is None:
            return 'null'
        if v is True:
            return 'true'
        if v is False:
            return 'false'
        if isinstance(v, (int, float)):
            return js_number(v)
        if isinstance(v, str):
            return js_quote(v)
        inner = pad * (level + 1)
        if isinstance(v, (list, tuple)):
            if not v:
                return '[]'
            items = ['null' if x is UNDEFINED else enc(x, level + 1) for x in v]
            if not pad:
                return '[' + ','.join(items) + ']'
            return '[\n' + ',\n'.join(inner + x for x in items) + '\n' + pad * level + ']'
        if isinstance(v, dict):
            items = [(k, x) for k, x in v.items() if x is not UNDEFINED]
            if not items:
                return '{}'
            sep = ': ' if pad else ':'
            parts = [js_quote(str(k)) + sep + enc(x, level + 1) for k, x in items]
            if not pad:
                return '{' + ','.join(parts) + '}'
            return '{\n' + ',\n'.join(inner + p for p in parts) + '\n' + pad * level + '}'
        raise TypeError('cannot serialize %r' % (v,))

    return enc(value, 0)


def translate(source, flags=''):
    """Translate a JS RegExp source (non-/u, no /s) into Python re syntax."""
    multiline = 'm' in flags
    out = []
    i, n = 0, len(source)
    while i < n:
        c = source[i]
        if c == '\\':
            nxt = source[i + 1]
            if nxt == 's':
                out.append(WS)
            elif nxt == 'S':
                out.append(NOT_WS)
            elif nxt == '/':
                out.append('/')
            elif nxt == '0':
                out.append('\\x00')
            elif nxt == 'u' and source[i + 2:i + 3] == '{':
                raise ValueError('\\u{...} needs /u: ' + source)
            elif nxt in 'cpPk':
                raise ValueError('unsupported escape \\' + nxt + ' in ' + source)
            else:
                out.append(c + nxt)
            i += 2
            continue
        if c == '[':
            j = i + 1
            body = []
            if j < n and source[j] == '^':
                body.append('^')
                j += 1
            if j < n and source[j] == ']':
                raise ValueError('empty JS class in ' + source)
            has_s = has_not_s = False
            while source[j] != ']':
                ch = source[j]
                if ch == '\\':
                    nxt = source[j + 1]
                    if nxt == 's':
                        has_s = True
                        body.append(_WS_CLASS)
                    elif nxt == 'S':
                        has_not_s = True
                    elif nxt == '/':
                        body.append('/')
                    elif nxt == '0':
                        body.append('\\x00')
                    else:
                        body.append(ch + nxt)
                    j += 2
                    continue
                if ch in '[&~|':
                    body.append('\\' + ch)
                else:
                    body.append(ch)
                j += 1
            if has_not_s:
                # Only [\s\S] (any character) occurs in the upstream sources.
                if not (has_s and len(body) == 1):
                    raise ValueError('unsupported \\S inside class in ' + source)
                out.append('[\\s\\S]')
            else:
                out.append('[' + ''.join(body) + ']')
            i = j + 1
            continue
        if c == '.':
            out.append('[^' + _LT_CLASS + ']')
        elif c == '^':
            out.append(LINE_START if multiline else '\\A')
        elif c == '$':
            out.append(LINE_END if multiline else '\\Z')
        else:
            out.append(c)
        i += 1
    return ''.join(out)


_CACHE = {}


def js_re(source, flags=''):
    """Compile a JS regex source with JS semantics (cached)."""
    key = (source, flags)
    rx = _CACHE.get(key)
    if rx is None:
        pyflags = re.ASCII
        if 'i' in flags:
            pyflags |= re.IGNORECASE
        rx = re.compile(translate(source, flags), pyflags)
        _CACHE[key] = rx
    return rx


def py_re(pattern, flags=0):
    """Compile a hand-written Python pattern with ASCII classes (cached)."""
    key = ('py', pattern, flags)
    rx = _CACHE.get(key)
    if rx is None:
        rx = re.compile(pattern, re.ASCII | flags)
        _CACHE[key] = rx
    return rx


def exec_all(rx, s, pos=0):
    """Every match of a global JS regex, as a `while (re.exec(s))` loop sees them.

    An empty match advances by one code unit, as String.prototype.match,
    matchAll and replace do for non-/u regexes.
    """
    out = []
    n = len(s)
    while pos <= n:
        m = rx.search(s, pos)
        if m is None:
            break
        out.append(m)
        pos = m.end() if m.end() > m.start() else m.end() + 1
    return out


def count_matches(rx, s):
    return len(exec_all(rx, s))


def js_replace_all(rx, s, repl):
    """String.prototype.replace with a global regex and a function replacement."""
    parts = []
    last = 0
    for m in exec_all(rx, s):
        parts.append(s[last:m.start()])
        parts.append(repl(m))
        last = m.end()
    parts.append(s[last:])
    return ''.join(parts)


def js_split(rx, s):
    """String.prototype.split(regex) for patterns that never match empty."""
    return rx.split(s)


def node_fs_error(exc, path, syscall='open'):
    """The message Node's fs puts on an error, e.g. "ENOENT: ..., open 'x'"."""
    import errno as _errno
    code = _errno.errorcode.get(exc.errno or 0, 'EIO')
    texts = {
        'ENOENT': 'no such file or directory',
        'EACCES': 'permission denied',
        'EISDIR': 'illegal operation on a directory',
        'ENOTDIR': 'not a directory',
        'EMFILE': 'too many open files',
        'ELOOP': 'too many symbolic links encountered',
        'ENAMETOOLONG': 'name too long',
        'EPERM': 'operation not permitted',
    }
    text = texts.get(code, (exc.strerror or 'unknown error').lower())
    if code == 'EISDIR':
        return '%s: %s, read' % (code, text)
    return "%s: %s, %s '%s'" % (code, text, syscall, path)


def read_file_utf8(path):
    """fs.readFileSync(path, 'utf8'): lossy decode, BOM kept. Returns u16 text."""
    with open(path, 'rb') as fh:
        data = fh.read()
    return to_u16(data.decode('utf-8', 'replace'))


def write_stdout(text):
    """Write a u16 string to stdout as UTF-8, as Node does (lone surrogates -> U+FFFD)."""
    import sys
    real = from_u16(text)
    data = real.encode('utf-8', 'replace') if not _SURROGATE.search(real) else \
        _SURROGATE.sub('�', real).encode('utf-8')
    sys.stdout.buffer.write(data)
    sys.stdout.buffer.flush()


def write_stderr(text):
    import sys
    real = _SURROGATE.sub('�', from_u16(text))
    sys.stderr.buffer.write(real.encode('utf-8'))
    sys.stderr.buffer.flush()


def encode_utf8(text):
    """Encode a u16 string as Node does when writing a string (lone surrogates -> U+FFFD)."""
    return _SURROGATE.sub('�', from_u16(text)).encode('utf-8')


# ─── JSON.parse with V8's error messages ───────────────────────────────────

class JSONParseError(ValueError):
    """SyntaxError raised by JSON.parse; str() is V8's message."""


_ARRAY_INDEX = re.compile(r'(?:0|[1-9][0-9]*)\Z')


def js_key_order(obj):
    """Reorder a dict the way JavaScript orders own properties: array-index
    keys ascending first, then the other keys in insertion order."""
    index_keys = [k for k in obj if _ARRAY_INDEX.match(k) and int(k) < 4294967295]
    if not index_keys:
        return obj
    rest = [k for k in obj if k not in index_keys]
    ordered = {}
    for k in sorted(index_keys, key=int):
        ordered[k] = obj[k]
    for k in rest:
        ordered[k] = obj[k]
    return ordered


class _JsonParser(object):
    WS_CHARS = ' \t\n\r'
    SPECIAL = ('NaN', 'Infinity', 'undefined', '[object Object]')

    def __init__(self, source):
        self.s = source
        self.n = len(source)
        self.pos = 0

    def fail(self, message=None, token=None):
        pos = self.pos
        where = self._where(pos)
        if message:
            raise JSONParseError('%s in JSON at position %d %s' % (message, pos, where))
        if token is None:
            token = self._token(pos)
        if token == 'EOS':
            raise JSONParseError('Unexpected end of JSON input')
        if token == 'NUMBER':
            raise JSONParseError('Unexpected number in JSON at position %d %s' % (pos, where))
        if token == 'STRING':
            raise JSONParseError('Unexpected string in JSON at position %d %s' % (pos, where))
        if self.s in self.SPECIAL:
            raise JSONParseError('"%s" is not valid JSON' % self.s)
        ch = self.s[pos]
        n = self.n
        if n >= 21:
            if pos < 10:
                context = '"%s"...' % self.s[:pos + 10]
            elif pos < n - 10:
                context = '..."%s"...' % self.s[pos - 10:pos + 10]
            else:
                context = '..."%s"' % self.s[pos - 10:]
        else:
            context = '"%s"' % self.s
        raise JSONParseError("Unexpected token '%s', %s is not valid JSON" % (ch, context))

    def _where(self, pos):
        line = 1
        last_break = 0
        i = 0
        while i < pos:
            if self.s[i] == '\r' and i < pos - 1 and self.s[i + 1] == '\n':
                i += 1
            if self.s[i] in '\r\n':
                line += 1
                last_break = i + 1
            i += 1
        return '(line %d column %d)' % (line, 1 + i - last_break)

    def _token(self, pos):
        if pos >= self.n:
            return 'EOS'
        ch = self.s[pos]
        if ch == '"':
            return 'STRING'
        if ch == '-' or '0' <= ch <= '9':
            return 'NUMBER'
        return 'OTHER'

    def skip_ws(self):
        while self.pos < self.n and self.s[self.pos] in self.WS_CHARS:
            self.pos += 1

    def peek(self):
        return self.s[self.pos] if self.pos < self.n else ''

    def parse(self):
        value = self.value()
        self.skip_ws()
        if self.pos < self.n:
            raise JSONParseError('Unexpected non-whitespace character after JSON at position %d %s'
                                 % (self.pos, self._where(self.pos)))
        return value

    def value(self):
        self.skip_ws()
        ch = self.peek()
        if ch == '{':
            return self.obj()
        if ch == '[':
            return self.arr()
        if ch == '"':
            return self.string()
        if ch == '-' or '0' <= ch <= '9' and ch != '':
            return self.number()
        if ch == 't':
            return self.literal('true', True)
        if ch == 'f':
            return self.literal('false', False)
        if ch == 'n':
            return self.literal('null', None)
        self.fail()

    def obj(self):
        self.pos += 1
        out = {}
        self.skip_ws()
        if self.peek() == '}':
            self.pos += 1
            return out
        if self.peek() != '"':
            self.fail("Expected property name or '}'")
        while True:
            key = self.string()
            self.skip_ws()
            if self.peek() != ':':
                self.fail("Expected ':' after property name")
            self.pos += 1
            out[key] = self.value()
            self.skip_ws()
            ch = self.peek()
            if ch == ',':
                self.pos += 1
                self.skip_ws()
                if self.peek() != '"':
                    self.fail('Expected double-quoted property name')
                continue
            if ch == '}':
                self.pos += 1
                return js_key_order(out)
            self.fail("Expected ',' or '}' after property value")

    def arr(self):
        self.pos += 1
        out = []
        self.skip_ws()
        if self.peek() == ']':
            self.pos += 1
            return out
        while True:
            out.append(self.value())
            self.skip_ws()
            ch = self.peek()
            if ch == ',':
                self.pos += 1
                continue
            if ch == ']':
                self.pos += 1
                return out
            self.fail("Expected ',' or ']' after array element")

    def string(self):
        self.pos += 1
        parts = []
        s, n = self.s, self.n
        while True:
            if self.pos >= n:
                self.fail('Unterminated string')
            ch = s[self.pos]
            if ch == '"':
                self.pos += 1
                return ''.join(parts)
            if ch == '\\':
                self.pos += 1
                if self.pos >= n:
                    self.fail(token='EOS')
                e = s[self.pos]
                simple = {'"': '"', '\\': '\\', '/': '/', 'b': '\b', 'f': '\f', 'n': '\n', 'r': '\r', 't': '\t'}
                if e in simple:
                    parts.append(simple[e])
                    self.pos += 1
                elif e == 'u':
                    code = 0
                    for _ in range(4):
                        self.pos += 1
                        h = s[self.pos] if self.pos < n else ''
                        if h == '' or h not in '0123456789abcdefABCDEF':
                            self.fail('Bad Unicode escape')
                        code = code * 16 + int(h, 16)
                    parts.append(chr(code))
                    self.pos += 1
                else:
                    self.fail('Bad escaped character')
                continue
            if ch < '\x20':
                self.fail('Bad control character in string literal')
            parts.append(ch)
            self.pos += 1

    def number(self):
        s, n = self.s, self.n
        start = self.pos
        digits = '0123456789'
        if self.peek() == '-':
            self.pos += 1
        if self.pos >= n or s[self.pos] not in digits:
            self.fail('No number after minus sign')
        if s[self.pos] == '0':
            self.pos += 1
            if self.pos < n and s[self.pos] in digits:
                self.fail(token='NUMBER')
        else:
            while self.pos < n and s[self.pos] in digits:
                self.pos += 1
        if self.peek() == '.':
            self.pos += 1
            if self.pos >= n or s[self.pos] not in digits:
                self.fail('Unterminated fractional number')
            while self.pos < n and s[self.pos] in digits:
                self.pos += 1
        if self.peek() in ('e', 'E'):
            self.pos += 1
            if self.peek() in ('+', '-'):
                self.pos += 1
            if self.pos >= n or s[self.pos] not in digits:
                self.fail('Exponent part is missing a number')
            while self.pos < n and s[self.pos] in digits:
                self.pos += 1
        value = float(s[start:self.pos])
        if value.is_integer() and abs(value) < 2 ** 53:
            return int(value)
        return value

    def literal(self, word, value):
        s = self.s
        remaining = self.n - self.pos
        if s[self.pos:self.pos + len(word)] == word:
            self.pos += len(word)
            return value
        self.pos += 1
        for i in range(min(len(word) - 1, remaining - 1)):
            if word[1 + i] != s[self.pos]:
                self.fail()
            self.pos += 1
        self.fail(token='EOS')


def js_json_parse(source):
    """JSON.parse(source) for a u16 string; raises JSONParseError with V8's message."""
    return _JsonParser(source).parse()


def js_typeof(v):
    if v is None:
        return 'object'
    if isinstance(v, bool):
        return 'boolean'
    if isinstance(v, (int, float)):
        return 'number'
    if isinstance(v, str):
        return 'string'
    if v is UNDEFINED:
        return 'undefined'
    return 'object'


def js_to_string(v):
    """String(v) / template-literal conversion for JSON values."""
    if v is None:
        return 'null'
    if v is UNDEFINED:
        return 'undefined'
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, (int, float)):
        return js_number(v)
    if isinstance(v, str):
        return v
    if isinstance(v, list):
        return ','.join('' if x is None or x is UNDEFINED else js_to_string(x) for x in v)
    return '[object Object]'
