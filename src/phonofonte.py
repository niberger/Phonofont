# Based on https://github.com/trishume/numderline/blob/master/patcher.py
# and https://github.com/powerline/fontpatcher/blob/develop/scripts/powerline-fontpatcher
# Used under the MIT license

import sys
import argparse
from fontTools.ttLib.tables._g_l_y_f import Glyph
from fontTools.ttLib import TTFont
from fontTools.feaLib.builder import addOpenTypeFeatures
from pathlib import Path

def get_argparser(ArgumentParser=argparse.ArgumentParser):
    parser = ArgumentParser(
        description=('Phonofonte font patcher '
                     'Requires FontForge with Python bindings. '
                     'Stores the patched font as a new, renamed font file by default.')
    )
    parser.add_argument('target_font_path', help='font file to patch', metavar='font',
                        type=argparse.FileType('rb'))
    parser.add_argument('new_font_name', help='name of the produced font', metavar='name',
                        type=str)
    return parser

def add_temp_glyph(font, name, original="a"):
    #first decompile the objects
    numGlyphs = font["maxp"].numGlyphs
    locations = font["loca"].locations
    glyphs = font["glyf"].glyphs
    glyphOrder = font["glyf"].glyphOrder
    metrics = font["hmtx"].metrics

    #then modify them
    locations.append(locations[numGlyphs])
    font["maxp"].numGlyphs = numGlyphs + 1
    glyphs[name] = glyphs[original]
    glyphOrder.append(name)
    metrics[name] = metrics[original]

def patch_font(target_font_path, new_font_name):
    font = TTFont(target_font_path.name)
    font['name'].setName(new_font_name,1,3,1,1033)

    add_temp_glyph(font, "tmp0")

    feature = """
languagesystem DFLT dflt;
languagesystem latn dflt;

feature calt {
    sub a m by tmp0;
    sub tmp0 by uni1E06 uni1E5F;

    sub B r by six;
    sub six by uni1E06 uni1E5F;
#
#    sub d r by  d_r;
#    sub d_r by uni1E0F uni1E5F;
#
#    sub D r by D_r;
#    sub D_r by uni1E0E uni1E5F;
#
#    sub t r by t_r;
#    sub t_r by uni1E6F uni1E5F;
#
#    sub T r by T_r;
#    sub T_r by uni1E6E uni1E5F;
} calt;
"""[1:]
    with open('mods.fea', 'w') as f:
        f.write(feature)

    addOpenTypeFeatures(font, 'mods.fea', tables=['GSUB'])
    font.save(f"{new_font_name}.ttf")
    font.close()
    print("> Created '{}'".format(new_font_name))

def main(argv):
    args = get_argparser().parse_args(argv)
    return patch_font(args.target_font_path, args.new_font_name)

main(sys.argv[1:])