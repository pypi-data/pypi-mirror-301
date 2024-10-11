from operator import methodcaller
from re import compile, IGNORECASE

from pybrary import fuzzy_select
from .select_base import SelectWidget


def select_exact(entries, pattern):
    return [i for i in entries if i == pattern]


def select_contain(entries, pattern):
    return [i for i in entries if pattern in i]


def select_insensitive(entries, pattern):
    return [i for i in entries if pattern in i.lower()]


def select_start(entries, pattern):
    return [i for i in entries if i.startswith(pattern)]


def select_end(entries, pattern):
    return [i for i in entries if i.endswith(pattern)]


def select_rex(entries, pattern):
    rex = compile(pattern, IGNORECASE).search
    return [i for i in entries if rex(i)]


def select_fuzzy(entries, pattern):
    return fuzzy_select(pattern, entries, decorate=methodcaller('lower'))


selectors = dict(
    x = select_exact,
    c = select_contain,
    i = select_insensitive,
    s = select_start,
    e = select_end,
    r = select_rex,
    f = select_fuzzy,
)


def select_multi(entries, pattern):
    if len(pattern) < 3:
        return entries

    if pattern[1] == ':':
        method, pattern = pattern[0], pattern[2:]
    else:
        method = 'f'

    if selector := selectors.get(method):
        return selector(entries, pattern)
    else:
        raise ValueError('Invalid pattern : %s', pattern)


class SelectExact(SelectWidget):
    def select(self, pattern):
        return select_exact(self.entries, pattern)


class SelectContain(SelectWidget):
    def select(self, pattern):
        return select_contain(self.entries, pattern)


class SelectInsensitive(SelectWidget):
    def select(self, pattern):
        return select_insensitive(self.entries, pattern)


class SelectStart(SelectWidget):
    def select(self, pattern):
        return select_start(self.entries, pattern)


class SelectEnd(SelectWidget):
    def select(self, pattern):
        return select_end(self.entries, pattern)


class SelectRex(SelectWidget):
    def select(self, pattern):
        return select_rex(self.entries, pattern)


class SelectFuzzy(SelectWidget):
    def select(self, pattern):
        return select_fuzzy(self.entries, pattern)


class SelectMulti(SelectWidget):
    def select(self, pattern):
        return select_multi(self.entries, pattern)

