import winzy
import os
import sys

def wc(text):
    """
    Mimics the functionality of the 'wc' command in Linux.

    Arguments:
    text: The input text to be processed.

    Returns:
    A tuple containing the number of lines, words, and characters.
    """
    lines = text.split("\n")
    word_count = sum(len(line.split()) for line in lines)
    char_count = sum(len(line) for line in lines)

    return len(lines), word_count, char_count



def create_parser(subparser):
    parser = subparser.add_parser("wc", description="Mimics the functionality of the 'wc' command")
    # Add subprser arguments here.
    parser.add_argument("text", help="Text from console", nargs="*", default=None)

    return parser


class HelloWorld:
    """ An example plugin """
    __name__ = "wc"

    @winzy.hookimpl
    def register_commands(self, subparser):
        parser = create_parser(subparser)
        parser.set_defaults(func=self.wc_com)

    def wc_com(self, args):
        # this routine will be called when "winzy 'wc' is called."

        text = " ".join(args.text)

        file_path = os.path.abspath(text)

        if os.path.isfile(file_path):
            try:
                with open(file_path, "r") as file:
                    text = file.read()
            except FileNotFoundError:
                pass

        if not text:
            text = sys.stdin.read()

        result = wc(text)
        print(result)
    
    def hello(self, args):
        # this routine will be called when "winzy "wc is called."
        print("Hello! This is an example ``winzy`` plugin.")

wc_plugin = HelloWorld()
