import yaml

from markov_generator import MarkovGenerator
from script import Script


def read_script_config(path):
    with open(path, 'r') as inf:
        return yaml.load(inf)

if __name__ == '__main__':
    print '\t--> Reading settings file: "config.yml"'
    configs = read_script_config('config.yml')

    print '\t--> Configuring script object'
    script_configs = configs['script_configs']
    movie_script = Script(**script_configs)

    print '\t\t--> Loading script from file "{}"'.format(configs['run_configs']['script_path'])
    movie_script.load_from_file(configs['run_configs']['script_path'])

    print '\t\t--> Parsing script text'
    movie_script.parse()

    print '\t--> Setting up Markov generator for script notes'
    note_generator = MarkovGenerator(movie_script.notes)

    print '\t--> Setting up Markov generator for scene settings'
    setting_generator = MarkovGenerator(movie_script.scenes)

    print '\t--> Setting up Markov generators for character dialog'
    character_generators = {}
    for character, character_dialog in movie_script.character_dialog.items():
        character_generators[character] = MarkovGenerator(character_dialog)

    print '\t--> Writing output script'
    if configs['run_configs']['output_format'] == 'markdown':
        scene_fmt = "#####{}. {}"
        direction_fmt = "*{}*"
        dialog_fmt = "**{}**: {}"
    elif configs['run_configs']['output_format'] == 'plaintext':
        scene_fmt = "{}. {}"
        direction_fmt = "{}"
        dialog_fmt = "{}: {}"

    outf = open(configs['run_configs']['output_path'], 'w')
    for line in movie_script.script_skeleton:
        if line['type'] == 'scene':
            outf.write(scene_fmt.format(line['number'], setting_generator.generate_markov_text(line['length'], line['original_text'][0])))
        if line['type'] == 'direction':
            outf.write(direction_fmt.format(note_generator.generate_markov_text(line['length'], line['text'][0])))
        if line['type'] == 'dialog':
            if len(character_generators[line['character']].corpus) <= 3:
                outf.write(dialog_fmt.format(line['character'], ' '.join(line['dialog'])))
            else:
                outf.write(dialog_fmt.format(line['character'], character_generators[line['character']].generate_markov_text(line['length'], line['dialog'][0])))

        outf.write('\n\n')

    outf.close()
