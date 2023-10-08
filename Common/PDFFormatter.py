from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams, LTPage
from pdfminer.layout import LTTextBoxHorizontal
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from re import match, Match
from io import BytesIO

# Regex patterns
REGEX_SPLIT_SECTION_1: str = r'^\d+\.\d+(\.\d+)?\s*$'
REGEX_SPLIT_SECTION_2: str = r'^([a-zA-Z]+(?:\s*,\s*[a-zA-Z]+)*)$'
REGEX_FULL_SECTION: str = r'^(\d+)\.(\d+)\s*([a-zA-Z]+(?:\s*,\s*[a-zA-Z]+)*)$'
REGEX_FULL_SECTION_SN: str = r'^\d+\.\d+(\.\d+)?\s*'
REGEX_TITLE: str = r"^\s*NASA-STD-5\d\d\d\w?\s*$"
REGEX_PAGE: str = r"^\s*(\d+)\s+of\s+(\d+)\s*$"

# Splits sections that are too big
def __split_and_trim(sections: dict[str, str]) -> tuple[dict[str, list[str]], list[str]]:
    split_sections: dict[str, list[str]] = {}
    for i in sections.keys():
        section: list[str] = sections[i].split("\n")
        if len(section) > 100:
            split = section[100:]
            if len(split) > 100:
                split_sections[i] = __split_and_trim({i : "\n".join(split)})[1]
                split_sections[i].insert(0, "\n".join(split[:100]))
            else:
                split_sections[i] = ["\n".join(split)]

    return split_sections, tuple(split_sections.values())[0]

def format_pdf(document: BytesIO) -> dict[str, str]:
    """
    Formats the standard's PDF into a dictionary of sections.

    Args:
        document (str): The opened pdf.
    
    Returns:
        dict[str, str] where:
            Key -> Section name, e.g. "SCOPE", "APPLICABLE DOCUMENTS".
            Value -> Content of the section.
    """

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
                    if not line or len(line) < 10 or match(REGEX_TITLE, line) or match(REGEX_PAGE, line):
                        continue

                    section_match: Match[str] | None = match(REGEX_FULL_SECTION, line)
                    if section_match and not append_next_line:
                        current_section = line[match(REGEX_FULL_SECTION_SN, line).end():]
                        sections[current_section] = current_section
                        continue
                    else:
                        # Check if the next line should be appended to the section number
                        if append_next_line:
                            section_match: Match[str] | None = match(REGEX_SPLIT_SECTION_2, line)
                            if section_match:
                                current_section = line
                                sections[current_section] = current_section

                            append_next_line = False
                            continue

                        # Identify section numbers using a regular expression
                        section_match: Match[str] | None = match(REGEX_SPLIT_SECTION_1, line)
                        if section_match:
                            append_next_line = True
                            continue

                    # Add content to the current section
                    if current_section and not append_next_line:
                        sections[current_section] += "\n" + line

    split_data = __split_and_trim(sections)[0]
    for key, value in split_data.items():
        del sections[key]
        padding = " "
        for split in value:
            sections[key + padding] = split
            padding += " "

    return sections