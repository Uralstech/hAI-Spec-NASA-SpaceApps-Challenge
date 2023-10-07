from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams, LTPage
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal
from re import match, Match

import os.path as path

HERE: str = path.dirname(path.abspath(__file__))
CACHE: str = path.join(HERE, ".DocsCache/")

PDF_1: str = "https://standards.nasa.gov/sites/default/files/standards/NASA/B/0/Historical/nasa_std_5009.pdf"
PDF_2: str = "https://standards.nasa.gov/sites/default/files/standards/NASA/B/0/Historical/nasa-std-5009a.pdf"
PDF_1_NAME: str = PDF_1.split("/")[-1]
PDF_2_NAME: str = PDF_2.split("/")[-1]
PDF_1_PATH: str = path.join(CACHE, PDF_1_NAME)
PDF_2_PATH: str = path.join(CACHE, PDF_2_NAME)

with open(PDF_1_PATH, 'rb') as document:
    # Create resource manager
    resource_manager: PDFResourceManager = PDFResourceManager()

    # Set parameters for analysis
    laparams: LAParams = LAParams()

    # Create a PDF page aggregator object
    device: PDFPageAggregator = PDFPageAggregator(resource_manager, laparams=laparams)
    interpreter: PDFPageInterpreter = PDFPageInterpreter(resource_manager, device)

    sections: dict[str, str] = {}
    current_section: str | None = None

    # Loop through each page
    for page in PDFPage.get_pages(document):
        interpreter.process_page(page)
        layout: LTPage = device.get_result()

        for element in layout:
            if isinstance(element, LTTextBoxHorizontal):
                lines: list[str] = element.get_text().split('\n')
                for line in lines:
                    # Identify sections using a regular expression
                    section_match: Match[str] | None = match(r'^\d+\.\s+(.*)', line)
                    if section_match:
                        current_section = line
                        sections[line] = line
                        continue
                    
                    if current_section:
                        sections[current_section] += "\n" + line

# Print the extracted sections and subsections
for section in sections:
    print(f"Section:\nSTART\n{section}\nEND")