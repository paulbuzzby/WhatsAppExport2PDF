from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.rl_config import defaultPageSize
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register font 'font_file' is location of symbola.ttf file

font_file = 'fonts/Symbola_hint.ttf'
symbola_font = TTFont('Symbola', font_file)
pdfmetrics.registerFont(symbola_font)

width, height = defaultPageSize
pdf_content = "It's 😂emoji time \u263A \U0001F61C. Let's add some😀 cool emotions \U0001F48F \u270C. And some more \u2764 \U0001F436"

styles = getSampleStyleSheet()
styles["Title"].fontName = 'Symbola'
para = Paragraph(pdf_content, styles["Title"])
canv = canvas.Canvas('emoji.pdf')

para.wrap(width, height)
para.drawOn(canv, 0, height/2)

canv.save()