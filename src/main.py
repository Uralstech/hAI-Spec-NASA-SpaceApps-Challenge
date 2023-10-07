from requests import get, Response
from os import mkdir, listdir, remove
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

# Older version of a standard
PDF_1: str = "https://standards.nasa.gov/sites/default/files/standards/NASA/D-w/CHANGE-1/1/Historical/nasa-std-5005.pdf"

# Next version of the standard
PDF_2: str = "https://standards.nasa.gov/sites/default/files/standards/NASA/D-w/CHANGE-1/1/Historical/nasa-std-5005b.pdf"

# Get name, filepath of PDF 1 and 2
PDF_1_NAME: str = PDF_1.split("/")[-1]
PDF_2_NAME: str = PDF_2.split("/")[-1]
PDF_1_PATH: str = join(DOCUMENT_CACHE, PDF_1_NAME)
PDF_2_PATH: str = join(DOCUMENT_CACHE, PDF_2_NAME)
PDF_1_NAME_WITHOUT_EXTENSION: str = PDF_1_NAME.split(".")[0]
PDF_2_NAME_WITHOUT_EXTENSION: str = PDF_2_NAME.split(".")[0]
PDF_1_FORMATTED_PICKLE: str = join(PICKLE_CACHE, f"{PDF_1_NAME_WITHOUT_EXTENSION}.pickle")
PDF_2_FORMATTED_PICKLE: str = join(PICKLE_CACHE, f"{PDF_2_NAME_WITHOUT_EXTENSION}.pickle")

# Get path for output dir and names for the prompt files.
OUTPUT_DIR = join(HERE, "Outputs/")
OUTPUT: str = join(OUTPUT_DIR, "Prompt_{0}_{1}.txt")

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

                        # Check if the next line should be appended to the section number
                        if append_next_line:
                            section_match: Match[str] | None = match(r'^([A-Z]+(,? [A-Z]+)?)+$', line)
                            if section_match:
                                current_section = line
                                sections[current_section] = current_section
                            
                            append_next_line = False
                            continue

                        # Identify section numbers using a regular expression
                        section_match: Match[str] | None = match(r'^(\d+)\.$', line)
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
else:
    for file in listdir(OUTPUT_DIR):
        standard: str = "_".join(file[7:].split("_")[:-1])
        if standard == PDF_1_NAME_WITHOUT_EXTENSION:
            remove(join(OUTPUT_DIR, file))

if not isfile(PDF_1_PATH):
    print("Downloading PDF_1...")
    cache_pdf(PDF_1, PDF_1_PATH)

if not isfile(PDF_2_PATH):
    print("Downloading PDF_2...")
    cache_pdf(PDF_2, PDF_2_PATH)

# Format the standards

print("Formatting the PDFs...")

pdf_1: dict[str, str]
pdf_2: dict[str, str]
if isfile(PDF_1_FORMATTED_PICKLE):
    with open(PDF_1_FORMATTED_PICKLE, "rb") as file:
        pdf_1 = load(file)
elif PICKLE:
    pdf_1 = format_pdf(PDF_1_PATH)

    with open(PDF_1_FORMATTED_PICKLE, "wb") as file:
        dump(pdf_1, file)
else:
    pdf_1 = format_pdf(PDF_1_PATH)

if isfile(PDF_2_FORMATTED_PICKLE):
    with open(PDF_2_FORMATTED_PICKLE, "rb") as file:
        pdf_2 = load(file)
elif PICKLE:
    pdf_2 = format_pdf(PDF_2_PATH)

    with open(PDF_2_FORMATTED_PICKLE, "wb") as file:
        dump(pdf_2, file)
else:
    pdf_2 = format_pdf(PDF_2_PATH)

print("Generating prompts...")

index: int = 0
pdf_2_sections = pdf_2.keys()
for key, value in pdf_1.items():
    for section in pdf_2_sections:
        # Check if the section from v-A is there in v-B
        if key.split(",")[0].split()[0].strip() in section:
            # If so, write a new prompt file.
            with open(str.format(OUTPUT, PDF_1_NAME_WITHOUT_EXTENSION, index), "w", encoding="utf-8") as file:
                file.write(f"I am making an AI and need a dataset. I have these two pages of different versions of a document.\n\nVERSION A:\n{pdf_1[key]}\n\nVERSION B:\n{pdf_2[section]}\n\nI want you to compare the two versions, then create a dataset entry in the format described below:\n\n\\### Instruction:\n[Please put the page of version A here]\n\n\\### Output:\nSuggesting Changes: [Yes / No, depending on if there are changes between the pages]\nCurrent Language: [The language in version A that has been changed in version B]\nSuggested Language: [The language in version B that replaced the language in version A]\nReason For Change: [The possible reason for the change between version A and B]\n\nPlease set \"Suggested Changes\" as \"No\" if the two pages are completely different and not related in any way.")
            index += 1
            break

print("Done!")