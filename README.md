# Markov at the Movies
Use markov chains to create random versions of a movie script.

## Setup
Everything you need to run the script and generate your own random movies is included in this package. All of the dependencies are stdlib, so there's nothing to install!

Edit the config.yml file include a text input script, an output path, and an output format (currently "markdown" and "plaintext" are supported). The size of the tuple helps control the amount of randomness in the generated text - generally, a smaller tuple size will produce more random text but faster runtimes, while a larger tuple produces less randomness, but longer runtimes. Too large a tuple size with a small corpus might not produce much variation in the output text.

**Warning: regex ahead.** The last piece of the puzzle is telling the script parser how to interpret the script you're passing it. I've built this script on the basic assumption that a script contains three types of entities - scene settings, dialog, and script notes (i.e. anything that's not a setting or a line of dialog). The script uses the "dialog_regex" and "scene_regex" parameters to identify lines that match those types. Anything that doesn't match those two expressions will be left as a script note.

## Running

Once the configuration file is set up, just run `$ python markov_movie.py` to make your new script.

## Credits

I got the idea to do this from reading [this blog post](http://mbutler.org/projects/the-markov-chain-gang/) and [also this one](http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/). I adapted some of my code from there too.