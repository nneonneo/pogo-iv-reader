# -*- coding: utf-8 -*-

from __future__ import print_function, division
from PIL import Image
import math

from imgdata import *
from pokedata import *
from common import Rectangle, Point
import tesserocr

tessapi = tesserocr.PyTessBaseAPI(psm=tesserocr.PSM.SINGLE_LINE)
def ocr_line(im, chars):
    tessapi.SetVariable("tessedit_char_whitelist", chars);
    tessapi.SetImage(im)
    tessapi.SetPageSegMode(tesserocr.PSM.SINGLE_LINE)
    return tessapi.GetUTF8Text()

def read_level(im, trainer_level):
    circle_r = MeterBounds.w / 2
    circle_center = Point(MeterBounds.x + circle_r, MeterBounds.y + circle_r)
    ballr = MeterBallRadius

    # half-levels start from 0
    hlvl_max = trainer_level * 2 + 1
    cpm_min = LevelStats[0]["cpmulti"]
    cpm_max = LevelStats[hlvl_max+1]["cpmulti"]
    # silly bruteforce to find the level ball
    for hlvl in range(hlvl_max+1):
        cpm = LevelStats[hlvl]["cpmulti"]
        angle = math.pi * ((cpm - cpm_min) / (cpm_max - cpm_min))
        center = Point(int(round(circle_center.x + circle_r * -math.cos(angle))),
                       int(round(circle_center.y + circle_r * -math.sin(angle))))

        # count white pixels in neighborhood
        simg = im.crop((center.x-ballr, center.y-ballr,
                        center.x+ballr+1, center.y+ballr+1))
        count = sum(simg.convert('L').histogram()[250:])
        # test to see if enough white pixels exist
        if count >= 0.90 * (ballr * ballr * math.pi):
            return (hlvl + 2) / 2

def read_cp(im):
    txtim = im.crop(CPBounds.to_bounds()).convert('L')
    lut = [0] * 250 + [255] * 6
    txtim = txtim.point(lut)
    line = ocr_line(txtim, 'CP0123456789').replace(' ', '').strip().upper()
    line = line.lstrip('C').lstrip('P')
    return int(line)

def read_hp(im):
    txtim = im.crop(HPBounds.to_bounds()).convert('L')
    line = ocr_line(txtim, 'HP0123456789/').replace(' ', '').strip().upper()
    line = line.lstrip('H').lstrip('P')
    curhp, maxhp = line.split('/')
    return int(curhp), int(maxhp)

def read_dust(im):
    txtim = im.crop(DustBounds.to_bounds()).convert('L')
    line = ocr_line(txtim, '0123456789').replace(' ', '').strip().upper()
    return int(line)

def read_species(im):
    # We can't *directly* observe the species, so we piece it together
    # from the candy (family) name and the evolve candy required.
    txtim = im.crop(CandyNameBounds.to_bounds()).convert('L')
    line = ocr_line(txtim, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    family = line.strip().replace(' ', '')[:-5].upper().title()

    # Deal with special-case family names
    if family.startswith('Nidoran'):
        if 'z' in family:
            family = u'Nidoran♂'
        elif family[7] == 'q':
            family = u'Nidoran♀'
        else:
            raise ValueError("can't figure out nidoran gender: %r" % family)
    elif family.startswith('Farfetch'):
        family = u"Farfetch'd"
    elif family.startswith('Mr') and 'ime' in family:
        family = u'Mr. Mime'
    elif family == 'Ratfata':
        family = u'Rattata'

    # Deal with the Eevee multi-evolve
    if family == 'Eevee':
        txtim = im.crop(TypeBounds.to_bounds()).convert('L')
        line = ocr_line(txtim, 'NormalWaterFireElectric')
        line = line.strip().replace(' ', '').upper().title()
        if line == 'Normal':
            return u'Eevee'
        elif line == 'Water':
            return u'Vaporeon'
        elif line == 'Fire':
            return u'Flareon'
        elif line == 'Electric':
            return u'Jolteon'

    buttonpx = im.getpixel(EvolveButtonPixel)
    if all(c >= 245 for c in buttonpx):
        # Evolve button not present
        candy = 0
    else:
        txtim = im.crop(EvolveCandyBounds.to_bounds()).convert('L')
        line = ocr_line(txtim, '0123456789')
        line = line.strip().replace(' ', '').upper().replace('O', '0')
        # Deal with occlusion from the big button...
        line = line[:2]
        if line == '10':
            candy = 100
        elif line == '40':
            candy = 400
        else:
            candy = int(line)
    famdat = PokemonFamilies[PokemonByName[family]['id']]
    return PokemonById[famdat[candy]]['name']

def read_data(im, trainer_level):
    return {'level': read_level(im, trainer_level),
            'cp': read_cp(im),
            'hp': read_hp(im),
            'dust': read_dust(im),
            'species': read_species(im)}

def parse_args(argv):
    import argparse
    parser = argparse.ArgumentParser(description="Read pokemon stats from a screenshot")
    parser.add_argument('level', type=int, help='trainer level')
    parser.add_argument('imgs', nargs='+', help='image filenames')
    return parser.parse_args(argv)

def main(argv):
    args = parse_args(argv)

    for imfn in args.imgs:
        print(imfn, read_data(Image.open(imfn), args.level))

if __name__ == '__main__':
    import sys
    exit(main(sys.argv[1:]))
