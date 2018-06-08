from typing import Iterable, Tuple

import ruamel.yaml

from plover.steno_dictionary import StenoDictionary
from plover.steno import normalize_steno, STROKE_DELIMITER


class YAMLDictionary(StenoDictionary):
    '''
    Stenography dictionary for YAML files.

    Format:

    Translation 1:
    - STROKE_1
    - STROKE_2
    Translation 2:
    - STROKE_1

    etc.
    '''

    def _load(self, filename: str):
        '''
        Populates the dictionary entries for Plover from a file.

        :param filename: The file path of the dictionary to load.
        '''

        self.update(YAMLDictionary.load_yaml_file(filename))

    def _save(self, filename: str):
        '''
        Saves off the current dictionary state in Plover to a file.

        :param filename: The file path of the dictionary to save to.
        '''

       # Group dictionary by value, sorted alphabetically
        data = {}

        for strokes, translation in sorted(self._dict.items(), key=lambda x: x[1].casefold()):
            # Need to join the multi-stroke entries into one stroke string first
            stroke = STROKE_DELIMITER.join(strokes)
            data.setdefault(translation, []).append(stroke)
            data[translation] = sorted(data[translation])

        # Write out the data
        yaml = ruamel.yaml.YAML(typ='safe')
        yaml.allow_unicode = True
        yaml.default_flow_style = False
        yaml.indent(sequence=4, offset=2)

        with open(filename, 'w', encoding='utf-8') as out_file:
            yaml.dump(data, out_file)

    @staticmethod
    def load_yaml_file(filename: str) -> Iterable[Tuple[Tuple[str], str]]:
        '''
        Loads a YAML dictionary file and provides an iterable to its
        stroke to translation mappings.

        :param filename: The file path of the YAML dictionary to load.
        :return: An iterable that provides tuples of stroke tuple, translation.
        '''

        # Load the data. Can't use the round-trip loader for performance reasons
        yaml = ruamel.yaml.YAML(typ='safe')

        with open(filename, 'r', encoding='utf-8') as in_file:
            data = yaml.load(in_file)

        # Provide tuples of stroke tuple, translation
        for translation, strokes in data.items():
            for stroke in strokes:
                yield (normalize_steno(stroke), translation)
