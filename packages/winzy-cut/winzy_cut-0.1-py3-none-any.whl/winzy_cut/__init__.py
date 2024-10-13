import winzy


import winzy
import sys

def cut_text(text, delimiter="\t", fields=None):
    """
    Mimics the functionality of the 'cut' command in Linux.

    Arguments:
    text: The input text to be processed.
    delimiter: The delimiter used to separate fields (default is tab).
    fields: A list of field numbers or ranges to be extracted.
            Example: [1, 3-5, 7] will extract fields 1, 3, 4, 5, and 7.

    Returns:
    A string containing the extracted fields.
    """
    lines = text.split("\n")
    result = []

    for line in lines:
        fields_list = line.split(delimiter)
        extracted_fields = []

        if fields:
            if "," in fields:
                fields = fields.split(",")
            # print(fields)
            for field in fields:
                if "-" in str(field):
                    start, end = map(int, field.split("-"))
                    extracted_fields.extend(fields_list[start - 1 : end])
                else:
                    try:
                        extracted_fields.append(fields_list[int(field) - 1])
                    except IndexError:
                        continue
        else:
            extracted_fields = fields_list

        result.append(delimiter.join(extracted_fields))

    return "\n".join(result)


class HelloWorld:
    __name__ = "cut"

    @winzy.hookimpl
    def register_commands(self, subparser):
        hello_parser = subparser.add_parser("cut", description="Mimics the functionality of the 'cut' command")
        hello_parser.add_argument("text", help="Text from console", nargs="*", default=None)
        hello_parser.add_argument(
        "--delimiter",
        "-d",
        default="\t",
        help="Delimiter character (for cut operation)", )

        hello_parser.add_argument(
        "--fields",
        "-f",
        nargs="+",
        type=str,
        help="Fields to extract (for cut operation)",
        )
        
        # Add subprser arguments here.
        hello_parser.set_defaults(func=self.hello)
    
    def hello(self, args):
        if args.text:
            text = " ".join(args.text)
        else:
            text = sys.stdin.read()
        result = cut_text(text, args.delimiter, args.fields)
        print(result)

cut_plugin = HelloWorld()
