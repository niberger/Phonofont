# Based on https://github.com/trishume/numderline/blob/master/patcher.py
# and https://github.com/powerline/fontpatcher/blob/develop/scripts/powerline-fontpatcher
# Used under the MIT license

import sys
import argparse
import re
import fontforge
from fontTools.ttLib import TTFont
from fontTools.feaLib.builder import addOpenTypeFeatures
from pathlib import Path

FONT_NAME_RE = re.compile(r'^([^-]*)(?:(-.*))?$')

def get_argparser(ArgumentParser=argparse.ArgumentParser):
    parser = ArgumentParser(
        description=('Phonofonte font patcher '
                     'Requires FontForge with Python bindings. '
                     'Stores the patched font as a new, renamed font file by default.')
    )
    parser.add_argument('target_fonts', help='font files to patch', metavar='font',
                        nargs='*', type=argparse.FileType('rb'))
    return parser
    
def out_path(name):
    Path('artifact').mkdir(parents=True, exist_ok=True)
    return 'artifact/{0}.ttf'.format(name)

def patch_one_font(font):
    font.encoding = 'ISO10646'
    mod_name = 'Photofonte'
    font.familyname += ' with '+mod_name
    font.fullname += ' with '+mod_name
    fontname, style = FONT_NAME_RE.match(font.fontname).groups()
    font.fontname = fontname + 'with' + mod_name
    if style is not None:
        font.fontname += style
    font.appendSFNTName(
        'English (US)', 'Preferred Family', font.familyname)
    font.appendSFNTName(
        'English (US)', 'Compatible Full', font.fullname)
    
    # 0xE900 starts an area spanning until 0xF000 that as far as I can tell nothing
    # popular uses. I checked the Apple glyph browser and Nerd Font.
    # Uses an array because of python closure capture semantics
    encoding_alloc = [0xE900]

    feature = """
languagesystem DFLT dflt;
languagesystem latn dflt;

feature calt {
    sub b r by seven;
    sub seven by uni1E07 uni1E5F;

    sub B r by six;
    sub six by uni1E06 uni1E5F;

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

    Path('tmp').mkdir(parents=True, exist_ok=True)
    font.generate('tmp/tmp.ttf')
    ft_font = TTFont('tmp/tmp.ttf')
    addOpenTypeFeatures(ft_font, 'mods.fea', tables=['GSUB'])
    # replacement to comply with SIL Open Font License
    out_name = font.fullname.replace('Source ', 'Sauce ')
    ft_font.save(out_path(out_name))
    print("> Created '{}'".format(out_name))
    return out_name

def patch_fonts(target_files):
    res = []
    for target_file in target_files:
        target_font = fontforge.open(target_file.name)
        try:
            res.append(patch_one_font(target_font))
        finally:
            target_font.close()
    return res

def main(argv):
    args = get_argparser().parse_args(argv)
    return patch_fonts(args.target_fonts)

main(sys.argv[1:])