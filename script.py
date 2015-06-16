import re
import string
from collections import defaultdict


class Script(object):
    """ Object representation of a movie's screenplay """

    def __init__(self, **settings):
        """ Configure script based on text patterns

        Set regex to parse scene and dialog patterns and also
        prep script class variables for storing text once
        the script is parsed.

        :param settings: (dict) script configuration parameters
                         to set as instance variables.
        """
        self.script_skeleton = []
        self.text = []

        self.scenes = []
        self.scene_regex = settings.get('scene_regex')

        self.character_dialog = defaultdict(list)
        self.dialog_regex = settings.get('dialog_regex')

        self.notes = []

    def load_from_file(self, path, line_divider='\n\n'):
        """ Load the script from a file

        Load the text of the file specified by 'path', and split them
        into an array of lines using 'line_divider'.

        :param path: (str) path to the script plaintext file to read.
        :param line_divider: (str: default "\n\n") line divider character(s),
                             used to split the file into lines.
        """
        with open(path, 'rU') as inf:
            self.text = [l.strip() for l in inf.read().split(line_divider)]

    def parse(self):
        """ Parse the script into sets of tokens

        After loading the script, parse lines into the appropriate type (dialog,
        scene notes, settings), tokenize, and store them so they can be retrieved
        by the appropriate markov generator.
        """
        scene_counter = 1
        scene_setting = re.compile(self.scene_regex)
        character_dialog = re.compile(self.dialog_regex)

        for line in self.text:
            if scene_setting.match(line):

                r = scene_setting.search(line)
                r_tokens = r.group(1).replace('-', ' ').strip().split()
                r_tokens = [t for t in r_tokens if t not in string.punctuation and t not in string.whitespace]
                self.scenes.extend(r_tokens)

                self.script_skeleton.append({
                    'type': 'scene',
                    'original_text': line,
                    'length': len(r_tokens),
                    'number': scene_counter
                })

                scene_counter += 1

            elif character_dialog.match(line):
                r = character_dialog.search(line)
                name = r.group(1)
                dialog = r.group(2).split()
                dialog = [d for d in dialog if d not in string.punctuation and d not in string.whitespace]
                self.character_dialog[name].extend(dialog)

                self.script_skeleton.append({
                    'type': 'dialog',
                    'character': name,
                    'dialog': dialog,
                    'length': len(dialog)
                })

            else:
                note = line.split()
                note = [n for n in note if n not in string.punctuation and n not in string.whitespace]
                self.notes.extend(note)

                self.script_skeleton.append({
                    'type': 'direction',
                    'text': note,
                    'length': len(note)
                })
