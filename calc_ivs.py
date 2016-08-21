from __future__ import print_function, division

import itertools
from pokedata import *

def find_ivs(pokemon):
    cpm = LevelStats[int(round(pokemon['level'] * 2 - 2))]["cpmulti"]
    base = PokemonByName[pokemon['species']]
    php = pokemon['hp'][1]
    pcp = pokemon['cp']

    # Just ugly bruteforce
    for a, d, s in itertools.product(range(16), repeat=3):
        da = a + base['attack']
        dd = d + base['defense']
        ds = s + base['stamina']
        hp = int(ds * cpm)
        cp = int(da * (dd**0.5) * (ds**0.5) * (cpm**2) / 10.0)
        if (hp == php or (php == 10 and hp <= 10)) and \
           (cp == pcp or (pcp == 10 and cp <= 10)):
            yield a,d,s

def parse_args(argv):
    import argparse
    parser = argparse.ArgumentParser(description="Read pokemon stats from a screenshot")
    parser.add_argument('level', type=int, help='trainer level')
    parser.add_argument('imgs', nargs='+', help='image filenames')
    return parser.parse_args(argv)

def main(argv):
    import read_screenshot
    from PIL import Image

    args = parse_args(argv)

    for imfn in args.imgs:
        pokemon = read_screenshot.read_data(Image.open(imfn), args.level)
        print(imfn, pokemon)
        for iv in find_ivs(pokemon):
            print('    %.1f%%: %s' % (sum(iv) / 45.0 * 100.0, iv))

if __name__ == '__main__':
    import sys
    exit(main(sys.argv[1:]))

# print(list(find_ivs({'family': u'Eevee', 'level': 26.0, 'hp': (85, 85), 'dust': 4000, 'cp': 747, 'species': u'Eevee'})))
# => [(7, 14, 15), (10, 7, 15), (11, 5, 15)]
