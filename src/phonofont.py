import fontforge
from fontTools.ttLib import TTFont
from fontTools.feaLib.builder import addOpenTypeFeatures
from pathlib import Path

ft_font = TTFont('fonts/Andika/AndikaNewBasic-R.ttf')
addOpenTypeFeatures(ft_font, 'src/rules.fea', tables=['GSUB'])
Path('artifact').mkdir(parents=True, exist_ok=True)
ft_font.save('artifact/output.ttf')
