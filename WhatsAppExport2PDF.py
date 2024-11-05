import re
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import utils
from reportlab.lib.units import cm, mm
from reportlab.platypus.flowables import Flowable

import PIL as pil
from PIL import Image as pilImage
from PIL import ImageFont as pilImageFont
from PIL import ImageDraw as pilImageDraw
from wordcloud import WordCloud
import os

import numpy as np
import random

import datetime
import emoji

# Register an emoji-compatible font (download NotoColorEmoji.ttf if needed)
pdfmetrics.registerFont(TTFont('Symbola', 'fonts/Symbola_hint.ttf'))
pdfmetrics.registerFont(TTFont('Helvetica', 'fonts/Helvetica.ttf'))
pdfmetrics.registerFont(TTFont('Chivo', 'fonts/Chivo-Thin.ttf'))

pageWidth = 1480
pageHeight = 2100
lineWidth = 20

# Regular expression to parse each line
message_pattern = r"\[(.*?)\] (.*?): (.*)"

class HorizontalLine(Flowable):
    def __init__(self, width):
        super().__init__()
        self.width = width

    def draw(self):
        self.canv.line(0, 0, self.width-40, 0)


def get_image(path, width=1*cm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))

def drawMonth(img, month, mask=False):
  font = pilImageFont.truetype("fonts/Chivo-Black.otf", 200)

  draw = pilImageDraw.Draw(img)
  bbox = draw.textbbox((0, 0), month.upper(), font=font)
  width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]

  x = round((pageWidth - width)/2)
  y = round((pageHeight - height)/2)

  if mask:
    draw.text((x, y - lineWidth), month.upper(), 255, font=font)
    #draw.line([x, y + height, x + width, y + height], 255, width=lineWidth)

  else:
    draw.text((x, y - lineWidth), month.upper(), 0, font=font)
    #draw.line([x, y + height, x + width, y + height], 0, width=lineWidth)

  return img

def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(40, 100)

def CreateMonthImage(month, year, monthText = None):

    monthImgPath = os.path.join("data", "monthImage_" + str(month)+ str(year) + ".png")


    if monthText is not None:
        
        img = pilImage.new("L", (pageWidth, pageHeight), 0)
        img = drawMonth(img, month, mask=True)
        mask = np.array(img)
        print("Generating wordCloud for {}".format(month))
        wordcloud = WordCloud(background_color="white", max_font_size=200, relative_scaling=.75, mask=mask)
        wordcloud.generate(monthText)
        wordcloud.recolor(color_func=grey_color_func, random_state=3)
        wordcloud.to_file(monthImgPath)

        img = pilImage.open(monthImgPath)
        img = drawMonth(img, month, mask=False)
        img.save(monthImgPath)

    else:
        img = pilImage.new("L", (pageWidth, pageHeight), 255)
        img = drawMonth(img, month, mask=False)
        img.save(monthImgPath)

    return monthImgPath
    

def parse_chat(filename):
    chat_data = []
    with open(filename, "r", encoding="utf-8") as file:
        current_message = ""
        timestamp = ""
        sender = ""

        for line in file:
            match = re.match(message_pattern, line)
            if match:
                if current_message:
                    chat_data.append((timestamp, sender, current_message.strip()))
                timestamp, sender, message = match.groups()
                current_message = message
            else:
                current_message += "\n" + line.strip()
        
        if current_message:
            chat_data.append((timestamp, sender, current_message.strip()))

    return chat_data

def fontsize(text, size=10) :
    return f"<font size={size} color=#adaeaf>{text}</font>"

def senderFontLeft(text) :
    #return f"<font color=#51b0bc>{text}</font>"
    return f"<font name='Helvetica-Bold'>{text}</font>"

def set_background_color(c, width, height, color):
    c.setFillColor(color)
    c.rect(0, 0, width, height, fill=1)

def add_background(canvas, doc):
    width, height = doc.pagesize
    set_background_color(canvas, width, height, color='#16a58d')  # Replace with your desired color

def remove_angle_brackets(text):
    # Define the regular expression pattern
    pattern = r'<attached: [^>]+>'
    
    # Function to remove the angle brackets from the matched pattern
    def replacer(match):
        return match.group(0)[1:-1]  # Remove the first and last character (< and >)
    
    # Use re.sub to replace the matched patterns
    cleaned_text = re.sub(pattern, replacer, text)
    return cleaned_text.replace('<', '(').replace('>', ')')

def wrap_emojis(text):
    return ''.join([f"<font name='Symbola'>{char}</font>" if emoji.is_emoji(char) else char for char in text])


def create_pdf(chat_data, output_filename):
    doc = SimpleDocTemplate(output_filename, pagesize=A4, leftMargin=14*mm, rightMargin=14*mm, topMargin=8*mm, bottomMargin=8*mm)
    styles = getSampleStyleSheet()
    #background colour #16a58d
        
    
    normalStyle = ParagraphStyle(
        "Normal",
        parent=styles["Normal"],
        fontName="Chivo",
        backColor=colors.white,#.peachpuff,
        textColor=colors.black,
    )

    custom_bold_style = ParagraphStyle(
        name='CustomBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=14
    )
    

    story = []
    lastTimestamp = None
    currentTimestamp = None
    currentMonth = None

    monthlyText = ""

    for timestamp, sender, message in chat_data:

        timestamp_temp = timestamp[:10]
        

        day, month, year = re.split("[-/\.]", timestamp_temp, 2)
        date = datetime.date(int(year), int(month), int(day))

        if currentMonth is None or currentMonth != date.month:
            if currentMonth is not None : 
                story.append(PageBreak())
            monthImgPath = CreateMonthImage(date.strftime("%B"), date.year)            
            story.append(get_image(monthImgPath, width=18*cm))
            story.append(PageBreak())
            currentMonth = date.month

            if lastTimestamp is not None:
                CreateMonthImage(lastTimestamp.strftime("%B"), lastTimestamp.year,monthlyText)
                monthlyText = ""

        if currentTimestamp is None or currentTimestamp != date:
            
            story.append(Spacer(1, 5))
            story.append(Paragraph(f"<b>{fontsize(date.strftime('%A, %B %d, %Y'),16)}</b>", custom_bold_style))
            story.append(Spacer(1, 8))
            story.append(HorizontalLine(doc.width))            
            
            currentTimestamp = date
        
        monthlyText += message
        #message = message.replace("\n", "<br/>")
        message = message.replace("\n", " ")        
        style = normalStyle
                

        message = wrap_emojis(remove_angle_brackets(message))

        bubble = Paragraph(f"{senderFontLeft(sender)}: {message}" , style)
        

        story.append(bubble)
        lastTimestamp = date

    CreateMonthImage(lastTimestamp.strftime("%B"), lastTimestamp.year,monthlyText)
    #doc.build(story)
    doc.build(story)#, onFirstPage=add_background, onLaterPages=add_background)

# Example usage
if __name__ == '__main__':
    #CreateMonthImage("November", 2023)
    print("Starting to process WhatsApp chat data")
    chat_data = parse_chat("data/_chat.txt")
    print("Parcing done, creating PDF")
    create_pdf(chat_data, "WhatsappExportRender.pdf")
    print("PDF created successfully")
