from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.rl_config import defaultPageSize
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from emojipy import Emoji
import re

import emoji as em


# Pdf doesn't need any unicode inside <image>'s alt attribute
Emoji.unicode_alt = False


def replace_with_emoji_pdf(text, size):
    """
    Reportlab's Paragraph doesn't accept normal html <image> tag's attributes
    like 'class', 'alt'. Its a little hack to remove those attrbs
    """

    text = Emoji.to_image(text)
    text = text.replace('class="emojione"', 'height=%s width=%s' %
                        (size, size))
    return re.sub('alt="'+Emoji.shortcode_regexp+'"', '', text)

# Register font 'font_file' is location of symbola.ttf file

font_file = 'Symbola_hint.ttf'
symbola_font = TTFont('Symbola', font_file)
pdfmetrics.registerFont(symbola_font)

width, height = defaultPageSize
pdf_content = "It's emoji time \u263A \U0001F61C. Let's add some 😂😂 cool emotions \U0001F48F \u270C. And some more \u2764 \U0001F436"

styles = getSampleStyleSheet()
styles["Title"].fontName = 'Symbola'
style = styles["Title"]
content = replace_with_emoji_pdf(Emoji.to_image(pdf_content), style.fontSize)

para = Paragraph(content, style)
canv = canvas.Canvas('emoji.pdf')

para.wrap(width, height)
para.drawOn(canv, 0, height/2)

canv.save()