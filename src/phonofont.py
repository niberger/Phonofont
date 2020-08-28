import fontforge
from fontTools.ttLib import TTFont
from fontTools.feaLib.builder import addOpenTypeFeatures

ft_font = TTFont('fonts/Andika/AndikaNewBasic-R.ttf')
addOpenTypeFeatures(ft_font, 'src/rules.fea', tables=['GSUB'])
ft_font.save('artifact/output.ttf')
