# -*- coding: utf-8 -*-
# authors: Ethosa

from random import choice
import re


class MarkovChains(dict):
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

    def __init__(self, ignorecase=False, other=None):
        """Creates a new MarkovChains object.

        Keyword Arguments:
            ignorecase {bool} (default: {False})
            other {MarkovChains} -- other MarkovChains. (default: {None})
        """
        self.ignorecase = ignorecase
        if isinstance(other, MarkovChains):
            dict.__init__(**other)
            self.ignorecase = other.ignorecase

    def __str__(self):
        return "[%s]" % (", ".join("[%s]=>%s" % (key, self[key]) for key in self.keys()))

    def add(self, key, next_chain=""):
        """Adds a new chain.

        Arguments:
            key {str} -- chain name.

        Keyword Arguments:
            next_chain {str} -- name of next chain. (default: {key})
        """
        key = self._contains(key)
        if key not in self:
            self[key] = [next_chain]
        else:
            self[key].append(next_chain)

    def contains(self, key):
        """Returns string object, if key in MarkovChains.

        Arguments:
            key {str} -- chain name.

        Returns:
            str
        """
        if self.ignorecase:
            text = "\n" + "\n".join([key for key in self.keys()]) + "\n"
            found = re.findall("\n(%s)\n" % key, text, re.IGNORECASE)
            if found:
                return found[0]
        else:
            if key in self.keys():
                return key

    def _contains(self, key):
        timed_key = self.contains(key)
        if timed_key:
            return timed_key
        return key

    def genseq(self, length=1, auth=None):
        """Generates sequence.

        Keyword Arguments:
            length {number} -- length of sequence (default: {1})
            auth {str} -- auth chain name (default: {random})

        Returns:
            list -- generated sequence
        """
        if not auth:
            auth = choice([i for i in self.keys()])
        now = choice(self[self._contains(auth)])

        generated = []
        for i in range(length):
            generated.append(now)
            now = choice(self[self._contains(now)])
        return generated

    def genstr(self, length=1, auth=None, sep=" "):
        """Generates string.

        Keyword Arguments:
            length {number} -- length of string (default: {1})
            auth {str} -- auth chain name (default: {random})
            sep {str} -- word separator (default: {" "})

        Returns:
            list -- generated string
        """
        return sep.join(self.genseq(length, auth))

    def to_chains(self, text):
        """Translates text to chains.

        Arguments:
            text {str}
        """
        words = re.split(r"\s+", text)
        length = len(words)
        for i in range(length-1):
            self.add(words[i], words[i+1])