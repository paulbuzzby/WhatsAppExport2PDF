import os
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_pdf_path):
    # Extract the base filename without the extension
    base_filename = os.path.splitext(os.path.basename(input_pdf_path))[0]
    
    # Read the PDF file
    pdf_reader = PdfReader(input_pdf_path)
    
    # Split each page into a new PDF
    for page_num in range(len(pdf_reader.pages)):
        pdf_writer = PdfWriter()
        
        # Add the single page to the writer
        pdf_writer.add_page(pdf_reader.pages[page_num])
        
        # Create a new filename based on the original filename and page number
        output_pdf_path = f"{base_filename}_page_{page_num + 1}.pdf"
        
        # Write the single page to a new PDF file
        with open(output_pdf_path, "wb") as output_pdf:
            pdf_writer.write(output_pdf)
        
        print(f"Created: {output_pdf_path}")

# Example usage
split_pdf("data/WhatsAnalyze.pdf")
