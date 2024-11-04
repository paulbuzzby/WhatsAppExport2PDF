import re
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import utils
from reportlab.lib.units import cm





# Register an emoji-compatible font (download NotoColorEmoji.ttf if needed)
pdfmetrics.registerFont(TTFont('Symbola', 'fonts/Symbola_hint.ttf'))

# Regular expression to parse each line
message_pattern = r"\[(.*?)\] (.*?): (.*)"



def get_image(path, width=1*cm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))



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
    return f"<font color=#51b0bc>{text}</font>"

def set_background_color(c, width, height, color):
    c.setFillColor(color)
    c.rect(0, 0, width, height, fill=1)

def add_background(canvas, doc):
    width, height = doc.pagesize
    set_background_color(canvas, width, height, color='#16a58d')  # Replace with your desired color


def create_pdf(chat_data, output_filename):
    doc = SimpleDocTemplate(output_filename, pagesize=A4, leftMargin=0, rightMargin=0)
    styles = getSampleStyleSheet()
    #background colour #16a58d

    
    
    # Custom styles with emoji font
    left_bubble_style = ParagraphStyle(
        "LeftBubble",
        parent=styles["Normal"],
        fontName="Symbola",
        backColor=HexColor(0x363636),# colors.gray,
        textColor=colors.white,
        borderPadding=5,
        borderRadius=15, 
        borderWidth=2,
        borderColor=HexColor(0x363636),
        leftIndent=30,
        rightIndent=120,
        leading=14,
    )    

    right_bubble_style = ParagraphStyle(
        "RightBubble",
        parent=styles["Normal"],
        fontName="Symbola",
        backColor=HexColor(0x005c4b),# colors.darkgreen,#.peachpuff,
        textColor=colors.white,
        borderPadding=5,
        borderRadius=15, 
        borderWidth=2,
        borderColor=HexColor(0x005c4b),
        leftIndent=120,
        rightIndent=30,
        alignment=2,
        leading=14,
    )

    story = []
    #story.append(get_image("data/00000617-PHOTO-2023-11-20-11-58-59.jpg", width=4*cm))
    for timestamp, sender, message in chat_data:
        # Replace new lines with <br/> for Paragraph rendering
        message = message.replace("\n", "<br/>")
        
        #style = right_bubble_style if "Paul Busby" in sender else left_bubble_style
        style = left_bubble_style if "Paul Busby" in sender else right_bubble_style
        bubble = Paragraph(f"<b>{senderFontLeft(sender)}</b>: <br/><br/>{message} <br/> <strong><i>{fontsize(timestamp,8)}</i></strong>" , style)

        story.append(bubble)
        story.append(Spacer(1, 15))

    #doc.build(story)
    doc.build(story, onFirstPage=add_background, onLaterPages=add_background)

# Example usage
chat_data = parse_chat("data/testchat.txt")
create_pdf(chat_data, "WhatsappExportRender.pdf")
