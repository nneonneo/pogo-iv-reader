from __future__ import print_function, division

import itertools
from pokedata import *
import multiprocessing

import read_screenshot
from PIL import Image
import sys

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

class FileProcessor:
    def __init__(self, level):
        self.level = level

    def process_file(self, imfn):
        print(imfn, file=sys.stderr)
        pokemon = read_screenshot.read_data(Image.open(imfn), self.level)
        res = imfn + ","
        res += "{species},{cp},{hp[1]},{level},{dust},{family}".format(**pokemon) + ","
        ivs = list(find_ivs(pokemon))
        ivs.sort(key=sum)
        if not ivs:
            res += ",,,"
        else:
            res += "{0:.1f},{1:.1f},{2[0]},{2[1]},{2[2]},{3[0]},{3[1]},{3[2]}".format(
                sum(ivs[0]) / 45.0 * 100.0,
                sum(ivs[-1]) / 45.0 * 100.0,
                ivs[0],
                ivs[-1])
        return res

def main(argv):
    args = parse_args(argv)

    pool = multiprocessing.Pool()

    print("filename,species,cp,maxhp,level,dust,family,minperf,maxperf,miniv_a,miniv_d,miniv_s,maxiv_a,maxiv_d,maxiv_s")
    for row in pool.map(FileProcessor(args.level).process_file, args.imgs):
        print(row)

if __name__ == '__main__':
    import sys
    exit(main(sys.argv[1:]))

# print(list(find_ivs({'family': u'Eevee', 'level': 26.0, 'hp': (85, 85), 'dust': 4000, 'cp': 747, 'species': u'Eevee'})))
# => [(7, 14, 15), (10, 7, 15), (11, 5, 15)]
