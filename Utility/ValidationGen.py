###############################
# This is a work in progress. #
###############################

from requests import get, Response
from os import mkdir, remove
from os.path import dirname, abspath, join, isdir, isfile
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams, LTPage
from pdfminer.layout import LTTextBoxHorizontal
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from re import match, Match
from pickle import load, dump

HERE: str = dirname(abspath(__file__))
DOCUMENT_CACHE: str = join(HERE, ".DocsCache/")
PICKLE_CACHE: str = join(HERE, ".PickleCache/")

# Set to False if pickling is not needed
PICKLE: bool = True

# Latest version of a standard
PDF_1: str = "https://standards.nasa.gov/sites/default/files/standards/NASA/Baseline-w/CHANGE-1/1/nasa-std-5018_revalidated.pdf"

# Get filename, filepath, name and pickle filepath of PDF 1
PDF_1_FILE: str = PDF_1.split("/")[-1]
PDF_1_PATH: str = join(DOCUMENT_CACHE, PDF_1_FILE)
PDF_1_NAME: str = PDF_1_FILE.split(".")[0]
PDF_1_PICKLE: str = join(PICKLE_CACHE, f"{PDF_1_NAME}.pickle")

# Get path for output dir and names for the dataset.
OUTPUT_DIR: str = join(HERE, "Dataset/")
OUTPUT_FILE: str = join(OUTPUT_DIR, "val.csv")

# Regex patterns
REGEX_SPLIT_SECTION_1: str = r'^(\d+)\.(\d+)$'
REGEX_SPLIT_SECTION_2: str = r'^([a-zA-Z]+(,? [a-zA-Z]+)?)+$'
REGEX_FULL_SECTION: str = r'^(\d+)\.(\d+)\s+([a-zA-Z]+(,? [a-zA-Z]+)?)+$'

# Downloads the pdf.
def cache_pdf(pdf: str, path: str) -> None:
    """
    Downloads the standard's PDF from the NASA website.

    Args:
        pdf (str): The link to the PDF.
        path (str): The path to store the PDF.
    """
    request: Response = get(pdf, stream=True)
    with open(path, "wb") as file:
        for chunk in request.iter_content(None):
            file.write(chunk)
    
    if not request.ok:
        remove(path)
        raise Exception("PDF download erred out!")

def format_pdf(pdf: str) -> dict[str, str]:
    """
    Formats the standard's PDF into a dictionary of sections.

    Args:
        pdf (str): The path to the PDF.
    
    Returns:
        dict[str, str] where:
            Key -> Section name, e.g. "SCOPE", "APPLICABLE DOCUMENTS".
            Value -> Content of the section.
    """

    with open(pdf, 'rb') as document:
        # Create resource manager
        resource_manager: PDFResourceManager = PDFResourceManager()

        # Set parameters for analysis
        laparams: LAParams = LAParams()

        # Create a PDF page aggregator object
        device: PDFPageAggregator = PDFPageAggregator(resource_manager, laparams=laparams)
        interpreter: PDFPageInterpreter = PDFPageInterpreter(resource_manager, device)

        sections: dict[str, str] = {}
        current_section: str | None = None
        append_next_line: bool = False

        # Loop through each page
        for page in PDFPage.get_pages(document):
            interpreter.process_page(page)
            layout: LTPage = device.get_result()

            for element in layout:
                if isinstance(element, LTTextBoxHorizontal):
                    lines: list[str] = element.get_text().split('\n')
                    for line in lines:
                        line = line.strip()
                        # Skip empty lines
                        if not line:
                            continue

                        section_match: Match[str] | None = match(REGEX_FULL_SECTION, line)
                        if section_match and not append_next_line:
                            current_section = line
                            sections[current_section] = current_section
                            continue
                        else:
                            # Check if the next line should be appended to the section number
                            if append_next_line:
                                append_next_line = False

                                section_match: Match[str] | None = match(REGEX_SPLIT_SECTION_2, line)
                                if section_match:
                                    current_section = line
                                    sections[current_section] = current_section
                                    continue

                            # Identify section numbers using a regular expression
                            section_match: Match[str] | None = match(REGEX_SPLIT_SECTION_1, line)
                            if section_match:
                                append_next_line = True
                                continue

                        # Add content to the current section
                        if current_section and not append_next_line:
                            sections[current_section] += "\n" + line

    return sections

if PICKLE and not isdir(PICKLE_CACHE):
    mkdir(PICKLE_CACHE)

# Check if the folders and files we need exist
if not isdir(DOCUMENT_CACHE):
    mkdir(DOCUMENT_CACHE)

if not isdir(OUTPUT_DIR):
    mkdir(OUTPUT_DIR)

if not isfile(PDF_1_PATH):
    print("Downloading PDF_1...")
    cache_pdf(PDF_1, PDF_1_PATH)

# Format the standard

print("Formatting the PDFs...")

pdf_1: dict[str, str]
if isfile(PDF_1_PICKLE):
    with open(PDF_1_PICKLE, "rb") as file:
        pdf_1 = load(file)
elif PICKLE:
    pdf_1 = format_pdf(PDF_1_PATH)

    with open(PDF_1_PICKLE, "wb") as file:
        dump(pdf_1, file)
else:
    pdf_1 = format_pdf(PDF_1_PATH)

print("Generating prompts...")

with open(OUTPUT_FILE, "w") as file:
    text: str = "Text\n"
    for value in pdf_1.values():
        text += "\"" + value.replace('\n', '\\n').replace('"', '""') + "\"\n"
    
    file.write(text.strip())

print("Done!")