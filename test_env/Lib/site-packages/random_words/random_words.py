# -*- coding: utf-8 -*-

import os
import json
from random import sample
from itertools import chain

main_dir = os.path.split(os.path.abspath(__file__))[0]


class Random(dict):

    def __init__(self, file):
        self.types_file = {
            'nouns': self.load_nouns,
            'nicknames': self.load_nicknames,
            'dmails': self.load_dmails,
        }

        self.load_file(file)

        super(Random, self).__init__()

    def load_file(self, file):
        """
        :param str file: filename
        """
        self.types_file[file](file)

    def load_nouns(self, file):
        """
        Load dict from file for random words.

        :param str file: filename
        """
        with open(os.path.join(main_dir, file + '.dat'), 'r') as f:
            self.nouns = json.load(f)

    def load_dmails(self, file):
        """
        Load list from file for random mails

        :param str file: filename
        """
        with open(os.path.join(main_dir, file + '.dat'), 'r') as f:
            self.dmails = frozenset(json.load(f))

    def load_nicknames(self, file):
        """
        Load dict from file for random nicknames.

        :param str file: filename
        """
        with open(os.path.join(main_dir, file + '.dat'), 'r') as f:
            self.nicknames = json.load(f)

    @staticmethod
    def check_count(count):
        """
        Checks count

        :param int count: count number ;)
        :raises: ValueError
        """
        if type(count) is not int:
            raise ValueError('Param "count" must be int.')
        if count < 1:
            raise ValueError('Param "count" must be greater than 0.')


class RandomWords(Random):

    def __init__(self):
        self.available_letters = 'qwertyuiopasdfghjklzcvbnm'

        super(RandomWords, self).__init__('nouns')

    def random_word(self, letter=None):
        """
        Return random word.

        :param str letter: letter
        :rtype: str
        :returns: random word
        """
        return self.random_words(letter)[0]

    def random_words(self, letter=None, count=1):
        """
        Returns list of random words.

        :param str letter: letter
        :param int count: how much words
        :rtype: list
        :returns: list of random words
        :raises: ValueError
        """
        self.check_count(count)

        words = []

        if letter is None:
            all_words = list(
                chain.from_iterable(self.nouns.values()))

            try:
                words = sample(all_words, count)
            except ValueError:
                len_sample = len(all_words)
                raise ValueError('Param "count" must be less than {0}. \
(It is only {0} words)'.format(len_sample + 1, letter))

        elif type(letter) is not str:
            raise ValueError('Param "letter" must be string.')

        elif letter not in self.available_letters:
            raise ValueError(
                'Param "letter" must be in {0}.'.format(
                    self.available_letters))

        elif letter in self.available_letters:
            try:
                words = sample(self.nouns[letter], count)
            except ValueError:
                len_sample = len(self.nouns[letter])
                raise ValueError('Param "count" must be less than {0}. \
(It is only {0} words for letter "{1}")'.format(len_sample + 1, letter))

        return words


class RandomNicknames(Random):

    def __init__(self):
        self.available_letters = 'qwertyuiopasdfghjklzxcvbnm'

        super(RandomNicknames, self).__init__('nicknames')

    def random_nick(self, letter=None, gender=None):
        """
        Return random nick.

        :param str letter: letter

        :param str gender: ``'f'`` for female, ``'m'`` for male and None for\
            both

        :rtype: str
        :returns: random nick
        """
        return self.random_nicks(letter, gender)[0]

    def random_nicks(self, letter=None, gender='u', count=1):
        """
        Return list of random nicks.

        :param str letter: letter
        :param str gender: ``'f'`` for female, ``'m'`` for male and None for both
        :param int count: how much nicks
        :rtype: list
        :returns: list of random nicks
        :raises: ValueError
        """
        self.check_count(count)

        nicks = []

        if gender not in ('f', 'm', 'u'):
            raise ValueError('Param "gender" must be in (f, m, u)')

        if letter is None:

            all_nicks = list(
                chain.from_iterable(self.nicknames[gender].values()))

            try:
                nicks = sample(all_nicks, count)
            except ValueError:
                len_sample = len(all_nicks)
                raise ValueError('Param "count" must be less than {0}. \
(It is only {0} words.")'.format(len_sample + 1))

        elif type(letter) is not str:
            raise ValueError('Param "letter" must be string.')

        elif letter not in self.available_letters:
            raise ValueError(
                'Param "letter" must be in "{0}".'.format(
                    self.available_letters))

        elif letter in self.available_letters:
            try:
                nicks = sample(self.nicknames[gender][letter], count)
            except ValueError:
                len_sample = len(self.nicknames[gender][letter])
                raise ValueError('Param "count" must be less than {0}. \
(It is only {0} nicks for letter "{1}")'.format(len_sample + 1, letter))

        return nicks


class RandomEmails(Random):

    def __init__(self):
        self.rn = RandomNicknames()

        super(RandomEmails, self).__init__('dmails')

    def randomMail(self):
        """
        Return random e-mail.

        :rtype: str
        :returns: random e-mail
        """
        return self.randomMails()[0]

    def randomMails(self, count=1):
        """
        Return random e-mails.

        :rtype: list
        :returns: list of random e-mails
        """
        self.check_count(count)

        random_nicks = self.rn.random_nicks(count=count)
        random_domains = sample(self.dmails, count)

        return [
            nick.lower() + "@" + domain for nick, domain in zip(random_nicks,
                                                                random_domains)
        ]
