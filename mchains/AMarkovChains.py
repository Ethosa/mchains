# -*- coding: utf-8 -*-
# authors: Ethosa

from random import choice
import re

import regex


class AMarkovChains(dict):
    def __add__(self, other):
        """Adds chains from other MarkovChains object.

        Arguments:
            other {MarkovChains} -- other MarkovChains object.
        """
        for key in other.keys():
            if key in self.keys():
                self[key].extend(other[key])
            else:
                self[key] = other[key][:]

    def __iadd__(self, other):
        self.__add__(other)
        return self

    def __init__(self, ignorecase=False, use_regex=False, other=None):
        """Creates a new MarkovChains object.

        Keyword Arguments:
            ignorecase {bool} (default: {False})
            use_regex {bool} -- use regex instead of re, if True. (default: {False})
            other {MarkovChains} -- other MarkovChains. (default: {None})
        """
        self.ignorecase = ignorecase
        self.re = regex if use_regex else re
        if isinstance(other, AMarkovChains):
            dict.__init__(**other)
            self.ignorecase = other.ignorecase

    def __str__(self):
        return "[%s]" % (", ".join("[%s]=>%s" % (key, self[key]) for key in self.keys()))

    async def add(self, key, next_chain=""):
        """Adds a new chain.

        Arguments:
            key {str} -- chain name.

        Keyword Arguments:
            next_chain {str} -- name of next chain. (default: {key})
        """
        key = await self._contains(key)
        if key not in self:
            self[key] = [next_chain]
        else:
            self[key].append(next_chain)

    async def contains(self, key):
        """Returns string object, if key in MarkovChains.

        Arguments:
            key {str} -- chain name.

        Returns:
            str
        """
        if self.ignorecase:
            text = "\n" + "\n".join([key for key in self.keys()]) + "\n"
            found = self.re.findall("\n(%s)\n" % key, text, self.re.IGNORECASE)
            if found:
                return found[0]
        else:
            if key in self.keys():
                return key

    async def _contains(self, key):
        timed_key = await self.contains(key)
        if timed_key:
            return timed_key
        return key

    async def genseq(self, length=1, auth=None):
        """Generates sequence.

        Keyword Arguments:
            length {number} -- length of sequence (default: {1})
            auth {str} -- auth chain name (default: {random})

        Returns:
            list -- generated sequence
        """
        if not auth:
            auth = choice([i for i in self.keys()])
        now = choice(self[await self._contains(auth)])

        generated = []
        for i in range(length):
            generated.append(now)
            now = choice(self[await self._contains(now)])
        return generated

    async def genstr(self, length=1, auth=None, sep=" "):
        """Generates string.

        Keyword Arguments:
            length {number} -- length of string (default: {1})
            auth {str} -- auth chain name (default: {random})
            sep {str} -- word separator (default: {" "})

        Returns:
            list -- generated string
        """
        return sep.join(await self.genseq(length, auth))

    async def to_chains(self, text, sep=r"\s+"):
        """Translates text to chains.

        Arguments:
            text {str}
            sep {regex str} -- separator.
        """
        words = self.re.split(sep, text)
        length = len(words)
        for i in range(length-1):
            await self.add(words[i], words[i+1])
