from common.constants import HTML_REGEX
from string import ascii_letters, digits


def clean_html(text):
    return HTML_REGEX.sub("", text)

def make_filename_safe(filename: str) -> str:
    valid_chars = f"-_.()!+='’&,~{ascii_letters}{digits} "
    reformatted = [char if char in valid_chars else "_" for char in filename]
    return "".join(reformatted)
