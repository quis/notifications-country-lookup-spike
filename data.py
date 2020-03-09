from functools import lru_cache

from notifications_utils.sanitise_text import SanitiseASCII
from notifications_utils.columns import Columns
from country_data import (
    COUNTRIES_AND_TERRITORIES,
    ADDITIONAL_SYNONYMS,
    UK_ISLANDS,
    ROYAL_MAIL_EUROPEAN,
    UK_POSTAGE_REGIONS,
    UK,
    Postage,
)


class CountryMapping(Columns):

    original_values = {}

    @staticmethod
    @lru_cache(maxsize=2048, typed=False)
    def make_key(original_key):

        normalised = "".join(
            character.lower() for character in original_key
            if character not in " _-',.()+&"
        )

        if '?' in SanitiseASCII.encode(normalised):
            return normalised

        return SanitiseASCII.encode(normalised)

    def __getitem__(self, key):
        return super().get(key) or super().get(f'the {key}')


countries = CountryMapping(
    COUNTRIES_AND_TERRITORIES + ADDITIONAL_SYNONYMS + UK_ISLANDS
)


class Country():

    def __init__(self, given_name):
        self.canonical_name = countries[given_name]

    @property
    def postage_zone():
        if self.canonical_name in UK_POSTAGE_REGIONS:
            return Postage.UK
        if self.canonical_name in europe:
            return Postage.EUROPE
        return Postage.REST_OF_WORLD
