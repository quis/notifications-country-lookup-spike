import json


def _load_data(filename):
    with open(filename) as contents:
        if filename.endswith('.json'):
            return json.load(contents)
        return [line.strip() for line in contents.readlines()]


def find_canonical(item, graph, key):
    if item['meta']['canonical']:
        return key, item['names']['en-GB']
    return find_canonical(
        graph[item['edges']['from'][0]],
        graph,
        key,
    )


UK = 'United Kingdom'

COUNTRIES_AND_TERRITORIES = [
    find_canonical(item, graph, item['names']['en-GB'])
    for item in _load_data('location-autocomplete-graph.json')
]

ADDITIONAL_SYNONYMS = [
    key, value
    for key, value in _load_data('synonyms.json').items()
]

UK_ISLANDS = [
    synonym, synonym for synonym in _load_data('uk-islands.txt')
]

ROYAL_MAIL_EUROPEAN = _load_data('europe.txt')

UK_POSTAGE_REGIONS = [UK] + UK_ISLANDS


class Postage:
    UK = UK
    EUROPE = 'Europe'
    REST_OF_WORLD = 'rest of world'
