"""
CUSTOM SCRIPT WRITER
- text file to pdf with custom formatting

Created by Holy and Mai on January 2025

"""

import re
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import argparse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Command line arguments
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='File path of target txt file (from current directory)')
    parser.add_argument('--output', type=str, default='output.pdf', help='File path of output pdf file (from current directory)')
    parser.add_argument('--subscript', type=str, default='Property of User', help='Text at the bottom of each page')
    parser.add_argument('--font', type=str, default='CodeNewRoman', choices=['JetBrains','UbuntuMono','CourierPrime','CodeNewRoman'], help='Font family used to render all text')
    args = parser.parse_args()

# Register Custom Fonts

#JetBrains
pdfmetrics.registerFont(TTFont('JetBrains-Regular', 'JetBrainsMono-Regular.ttf'))
pdfmetrics.registerFont(TTFont('JetBrains-Bold', 'JetBrainsMono-Bold.ttf'))
pdfmetrics.registerFont(TTFont('JetBrains-Italic', 'JetBrainsMono-Italic.ttf'))

#Ubuntu
pdfmetrics.registerFont(TTFont('UbuntuMono-Regular', 'UbuntuMono-Regular.ttf'))
pdfmetrics.registerFont(TTFont('UbuntuMono-Bold', 'UbuntuMono-Bold.ttf'))
pdfmetrics.registerFont(TTFont('UbuntuMono-Italic', 'UbuntuMono-Italic.ttf'))

#CourierPrime
pdfmetrics.registerFont(TTFont('CourierPrime-Regular', 'CourierPrime-Regular.ttf'))
pdfmetrics.registerFont(TTFont('CourierPrime-Bold', 'CourierPrime-Bold.ttf'))
pdfmetrics.registerFont(TTFont('CourierPrime-Italic', 'CourierPrime-Italic.ttf'))

#CodeNewRoman
pdfmetrics.registerFont(TTFont('CodeNewRoman-Regular', 'CodeNewRoman-Regular.ttf'))
pdfmetrics.registerFont(TTFont('CodeNewRoman-Bold', 'CodeNewRoman-Bold.ttf'))
pdfmetrics.registerFont(TTFont('CodeNewRoman-Italic', 'CodeNewRoman-Italic.ttf'))


# Define font families
FONT_FAMILIES = {
    'JetBrains': {
        'title': ('JetBrains-Bold', 20),
        'normal': ('JetBrains-Regular', 12),
        'italic': ('JetBrains-Italic', 12),
    },
    'UbuntuMono': {
        'title': ('UbuntuMono-Bold', 20),
        'normal': ('UbuntuMono-Regular', 12),
        'italic': ('UbuntuMono-Italic', 12),
    },
    'CourierPrime': {
        'title': ('CourierPrime-Bold', 20),
        'normal': ('CourierPrime-Regular', 12),
        'italic': ('CourierPrime-Italic', 12),
    },
    'CodeNewRoman': {
        'title': ('CodeNewRoman-Bold', 20),
        'normal': ('CodeNewRoman-Regular', 12),
        'italic': ('CodeNewRoman-Italic', 12),
    }
}

# Get selected font family
selected_fonts = FONT_FAMILIES[args.font]

# Margins
left_margin = 105
right_margin = 525
bottom_margin = 70
dialogue_left_margin = 200
dialogue_right_margin = 434
character_left_margin = 294
character_right_margin = 525
parenthetical_left_margin = 252
parenthetical_right_margin = 392

line_height = 16

# Script Syntax and formatting
def process_line(line):
    line = line.strip()
    
    if line.startswith('/'):
        return selected_fonts['title'], line[1:].strip(), 'regular'
    elif line.startswith('.'):
        return selected_fonts['normal'], line[1:].strip().upper(), 'regular'
    elif line.startswith('@'):
        return selected_fonts['normal'], line[1:].strip().upper(), 'character'
    elif line.startswith('('):
        return selected_fonts['normal'], line[0:].strip(), 'parenthetical'
    elif line.startswith('#'):
        return None, None, None
    elif line.startswith("'"):
        return selected_fonts['normal'], line[1:].strip(), 'dialogue'
    elif line.startswith("title:") or line.startswith("author:"):
        return None, None, None
    else:
        return selected_fonts['normal'], line.strip(), 'regular'

# End current page and add footer
def newPage(c, page_number, header):
    width, height = A4
    c.setFont(selected_fonts['title'][0], selected_fonts['normal'][1]-2)
    c.drawRightString(width - 40, 30, f"{page_number}")
    c.drawCentredString(width / 2, 30, args.subscript)
    c.drawCentredString(width / 2, height - 30, f"{header}")
    c.showPage()

def create_pdf(input_file, output_file):
    c = canvas.Canvas(output_file, pagesize=A4)
    width, height = A4
    toc = []
    chapter_positions = {}
    content_lines = []
    current_page = 1

    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            # Make title page before line processing
            if line.startswith("title:"):
                Title = line[6:].strip()
                c.setTitle(Title)
                c.setFont(selected_fonts['title'][0], 25)
                c.drawCentredString(298, height - 350, Title.upper())
                c.setFont(selected_fonts['title'][0], selected_fonts['normal'][1]-2)
                c.drawCentredString(298, 30, args.subscript)
            
            if line.startswith("author:"):
                c.setAuthor(line[7:].strip())
                c.setFont(selected_fonts['normal'][0], selected_fonts['normal'][1])
                c.drawCentredString(298, height - 382, "Written by")
                c.setFont(selected_fonts['normal'][0], selected_fonts['normal'][1] + 4)
                c.drawCentredString(298, height - 414, line[7:].strip())
                c.showPage()
                current_page += 1
            
            font, text, margin_type = process_line(line)
            if text is None:
                continue
            
            if font == selected_fonts['title']:
                toc.append((text, f"chapter_{len(toc) + 1}"))
            content_lines.append((font, text, margin_type))

    # Add Table of Contents
    print(f"Creating Table of Contents...")
    c.setFont(selected_fonts['title'][0], selected_fonts['title'][1])
    c.drawString(left_margin, height - 60, "Table of Contents")
    c.setFont(selected_fonts['normal'][0], selected_fonts['normal'][1])
    toc_y_position = height - 80
    
    for chapter, link in toc:
        if toc_y_position - line_height < bottom_margin:
            newPage(c, current_page, Title)
            current_page += 1
            toc_y_position = height - 60
            c.setFont(selected_fonts['normal'][0], selected_fonts['normal'][1])
        c.drawString(left_margin, toc_y_position, chapter)
        c.linkAbsolute(link, link, (left_margin, toc_y_position - 2, right_margin, toc_y_position + line_height))
        toc_y_position -= line_height
    
    newPage(c, current_page, Title) # Start a new page for the main content
    current_page += 1
    
    # Render the main content
    print(f"Rendering Main Content...")
    y_position = height - 60

    for font, text, margin_type in content_lines:
        if line.startswith("title:"):
            continue
        if line.startswith("author:"):
            continue
        if text.startswith("="):
            newPage(c, current_page, Title)
            current_page += 1
            y_position = height - 60
            c.setFont(font[0], font[1])
            continue
		
        # Margins
        current_margin_left = {
            'dialogue': dialogue_left_margin,
            'character': character_left_margin,
            'parenthetical': parenthetical_left_margin
        }.get(margin_type, left_margin)
        current_margin_right = {
            'dialogue': dialogue_right_margin,
            'character': character_right_margin,
            'parenthetical': parenthetical_right_margin
        }.get(margin_type, right_margin)

        c.setFont(font[0], font[1])
        
        # Check if the line will fit on the current page, else create a new page
        if y_position - line_height < 60:
            newPage(c, current_page, Title)
            current_page += 1
            y_position = height - 60  # Reset y_position for the new page
            c.setFont(font[0], font[1])
        
        # Handle tab characters explicitly
        text_with_tabs = text.replace("\t", 2 * "    ")
        
        # Draw the text within the set margins
        max_line_width = current_margin_right - current_margin_left
        if c.stringWidth(text_with_tabs, font[0], font[1]) > max_line_width:
            words = text_with_tabs.split(' ')
            current_line = ''
            for word in words:
                if y_position - line_height < 60:
                    newPage(c, current_page, Title)  # Start a new page
                    current_page += 1
                    y_position = height - 60
                    c.setFont(font[0], font[1])
                if c.stringWidth(current_line + word, font[0], font[1]) <= max_line_width:
                    current_line += word + ' '
                else:
                    c.drawString(current_margin_left, y_position, current_line.strip())
                    y_position -= line_height
                    current_line = word + ' '
            c.drawString(current_margin_left, y_position, current_line.strip())
        else:
            c.drawString(current_margin_left, y_position, text_with_tabs)
        
        # Record the bookmark for chapter titles
        if font == selected_fonts['title']:
            chapter_id = next(i + 1 for i, (ch, _) in enumerate(toc) if ch == text)
            c.bookmarkPage(f"chapter_{chapter_id}")
            c.addOutlineEntry(text, f"chapter_{chapter_id}", level=0)
            chapter_positions[text] = (current_page, y_position)
        
        y_position -= line_height
        
    newPage(c, current_page, Title)

    c.save()

# Input and output file paths
input_txt_file = args.input  # Your input text file
output_pdf_file = args.output  # Output PDF file

# Generate PDF from the text file
create_pdf(input_txt_file, output_pdf_file)
print(f"PDF created successfully: {output_pdf_file}")
