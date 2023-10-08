"""
Utility to download and create GPT prompts for 2 different versions of a NASA standard.
"""

from requests import get, Response
from os import mkdir, remove
from os.path import dirname, abspath, join, isdir, isfile
from pickle import load, dump
from shutil import rmtree
from argparse import ArgumentParser
from Common.common import format_pdf

# Source and cache paths
HERE: str = dirname(abspath(__file__))
DOCUMENT_CACHE: str = join(HERE, ".DocsCache/")
PICKLE_CACHE: str = join(HERE, ".PickleCache/")

# Set to False if pickling is not needed
PICKLE: bool = True

# Older version of a standard
PDF_1: str = "https://standards.nasa.gov/sites/default/files/standards/NASA/C/0/Historical/nasa-std-5009b.pdf"

# Next version of the standard
PDF_2: str = "https://standards.nasa.gov/sites/default/files/standards/NASA/C/0/2023-08-03-NASA-STD-5009C-Approved.pdf"

# Sets command-line arguments
parser = ArgumentParser()
parser.add_argument("-p1", "--pdf_1", type=str, help="The link to pdf_1.", required=False)
parser.add_argument("-p2", "--pdf_2", type=str, help="The link to pdf_2.", required=False)
parser.add_argument("--no_pickle", help="Do not load pickle.", action="store_true")
args = parser.parse_args()

PDF_1 = args.pdf_1 if args.pdf_1 else PDF_1
PDF_2 = args.pdf_2 if args.pdf_2 else PDF_2
REMAKE_PICKLE: bool = parser.no_pickle

# Get PDF filename
PDF_1_FILE: str = PDF_1.split("/")[-1]
PDF_2_FILE: str = PDF_2.split("/")[-1]

# Get PDF filepath
PDF_1_PATH: str = join(DOCUMENT_CACHE, PDF_1_FILE)
PDF_2_PATH: str = join(DOCUMENT_CACHE, PDF_2_FILE)

# Get PDF name
PDF_1_NAME: str = PDF_1_FILE.split(".")[0]
PDF_2_NAME: str = PDF_2_FILE.split(".")[0]

# Get pickle path
PDF_1_PICKLE: str = join(PICKLE_CACHE, f"{PDF_1_NAME}.pickle")
PDF_2_PICKLE: str = join(PICKLE_CACHE, f"{PDF_2_NAME}.pickle")

# Get path for output dirs and names for the prompt files.
ALL_OUTPUT_DIR: str = join(HERE, "Outputs/")
SUB_OUTPUT_DIR: str = join(ALL_OUTPUT_DIR, PDF_1_NAME)
OUTPUT: str = join(SUB_OUTPUT_DIR, "Prompt_{0}_{1}.txt")

def cache_pdf(pdf: str, path: str) -> None:
    """
    Downloads the standard's PDF from the NASA website.

    Args:
        pdf (str): The link to the PDF.
        path (str): The path to store the PDF.
    """

    # Download request
    request: Response = get(pdf, stream=True)
    with open(path, "wb") as file:
        for chunk in request.iter_content(None):
            file.write(chunk)
    
    # Check errors
    if not request.ok:
        # Delete corrupt/empty PDF.
        remove(path)

        raise Exception("PDF download erred out!")

def load_and_format_pdf(pdf: str) -> dict[str, str]:
    """
    Loads and formats a standard's PDF from its filepath.

    Args:
        pdf (str): The path to the PDF.
    
    Returns:
        dict[str, str] where:
            Key -> Section name, e.g. "SCOPE", "APPLICABLE DOCUMENTS".
            Value -> Content of the section.
    """

    with open(pdf, "rb") as file:
        return format_pdf(file)

# Setup working directory by creating folders if they don't exist
if PICKLE and not isdir(PICKLE_CACHE):
    mkdir(PICKLE_CACHE)

if not isdir(DOCUMENT_CACHE):
    mkdir(DOCUMENT_CACHE)

if not isdir(ALL_OUTPUT_DIR):
    mkdir(ALL_OUTPUT_DIR)

if not isdir(SUB_OUTPUT_DIR):
    mkdir(SUB_OUTPUT_DIR)
else:
    rmtree(SUB_OUTPUT_DIR)
    mkdir(SUB_OUTPUT_DIR)

# Download PDFs if they don't exist
if not isfile(PDF_1_PATH):
    print("Downloading PDF_1...")
    cache_pdf(PDF_1, PDF_1_PATH)

if not isfile(PDF_2_PATH):
    print("Downloading PDF_2...")
    cache_pdf(PDF_2, PDF_2_PATH)

# Format the standards or load pickle
pdf_1: dict[str, str]
pdf_2: dict[str, str]

if isfile(PDF_1_PICKLE) and not REMAKE_PICKLE:
    with open(PDF_1_PICKLE, "rb") as file:
        pdf_1 = load(file)
elif PICKLE:
    print("Formatting the PDF 1...")
    pdf_1 = load_and_format_pdf(PDF_1_PATH)

    with open(PDF_1_PICKLE, "wb") as file:
        dump(pdf_1, file)
else:
    pdf_1 = load_and_format_pdf(PDF_1_PATH)

if isfile(PDF_2_PICKLE) and not REMAKE_PICKLE:
    with open(PDF_2_PICKLE, "rb") as file:
        pdf_2 = load(file)
elif PICKLE:
    print("Formatting the PDF 2...")
    pdf_2 = load_and_format_pdf(PDF_2_PATH)

    with open(PDF_2_PICKLE, "wb") as file:
        dump(pdf_2, file)
else:
    pdf_2 = load_and_format_pdf(PDF_2_PATH)

# Generate prompts

print("Generating prompts...")
index: int = 0
pdf_2_sections = pdf_2.keys()
for key, value in pdf_1.items():
    # Check if the section from v-A is there in v-B
    for section in pdf_2_sections:
        if key.split(",")[0].split()[0].strip() in section:
            # If so, write a new prompt file.
            with open(str.format(OUTPUT, PDF_1_NAME, index), "w", encoding="utf-8") as file:
                file.write(f"I am making an AI and need a dataset. I have these two pages of different versions of a document.\n\nVERSION A:\n{value}\n\nVERSION B:\n{pdf_2[section]}\n\nI want you to compare the two versions but ignore changes such as: title changes, then create a dataset entry in the format described below:\n\n\### Output:\nSuggesting Changes: [Yes / No, set to Yes only if there are any changes to be suggested!]\n\n[Below are the main parameters. If there are no changes, set them to 'N/A'.]\nCurrent Language: [The language in version A that has been changed in version B]\nSuggested Language: [The language in version B that replaced the language in version A]\nReason For Change: [The possible reason for the change between version A and B]")
            index += 1
            break

print("Done!")