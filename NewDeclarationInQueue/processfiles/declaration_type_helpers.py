import re
from pdfminer.high_level import extract_text

from pdf_model.parse_lib.helpers import isEmptyLine


def shouldUseOcr(pdf_file_path):
    extracted_text = extract_text(pdf_file_path)
    phase_1_format = re.sub(' +', ' ', re.sub('\n+', '\n', extracted_text.strip()))
    lines = phase_1_format.split('\n')
    phase_2 = []
    for line in lines:
        if isEmptyLine(line):
            continue
        phase_2.append(line)
    phase_2_format = '\n'.join(phase_2)

    print(len(phase_2_format))
    if len(phase_2_format) > 100:
        return False

    return True
