import winzy
import os
import sys

def extract_text_from_file(text, in_line_no, out_line_no, skip_blank_lines=False):
    """
    Extracts text from a file based on input and output line numbers.

    Arguments:
    text: File content
    in_line_no: Line number to start extracting text (inclusive).
    out_line_no: Line number to end extracting text (inclusive).
    skip_blank_lines: If true, blank lines are skipped

    Returns:
    A string containing the text from in_line_no to out_line_no.
    """

    lines = text.split("\n")
    if skip_blank_lines:
        lines = [line for line in lines if len(line) !=0]

    total_lines = len(lines)

    if out_line_no is None:
        out_line_no = total_lines

    if in_line_no is None:
        in_line_no = 1

    if (
        in_line_no < 1
        or out_line_no < 1
        or in_line_no > total_lines
        or out_line_no > total_lines
    ):
        return "Invalid line numbers provided."

    if in_line_no > out_line_no:
        return "Input line number should be less than or equal to output line number."

    extracted_lines = lines[in_line_no - 1 : out_line_no]
    extracted_text = "\n".join(extracted_lines)
    return extracted_text


class HelloWorld:
    name = "extract"

    @winzy.hookimpl
    def register_commands(self, subparser):
        hello_parser = subparser.add_parser("extract", description="Extracts text from a file based on input and output line numbers")
        hello_parser.add_argument("file", help="Path to the file", nargs="*", default=None)
        hello_parser.add_argument(
        "--in_line", "-i", type=int, help="Starting line number (for extract operation)")
        hello_parser.add_argument(
        "--out_line", "-o", type=int, help="Ending line number (for extract operation)")
        hello_parser.add_argument(
        "--skip-blank-lines", "-s", action='store_true', help="If given blank lines are skipped")

        # Add subprser arguments here.
        hello_parser.set_defaults(func=self.extract)

    def extract(self, args):
        # this routine will be called when "winzy "extract is called."
        text = "".join(args.file)

        file_path = os.path.abspath(text)


        if os.path.isfile(file_path):
            try:
                with open(file_path, "r") as file:
                    text = file.read()
            except FileNotFoundError:
                pass

        if not text:
            text = sys.stdin.read()

        result = extract_text_from_file(text, args.in_line, args.out_line, args.skip_blank_lines)
        print(result)

    def hello(self, args):
        # this routine will be called when "winzy "extract is called."
        print("Hello! This is an example ``winzy`` plugin.")


extract_plugin = HelloWorld()
