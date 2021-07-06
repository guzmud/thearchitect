import argparse
from pathlib import Path
import secrets
import subprocess
import tempfile

import proquint

from models import Piece


def get_secret_token():
    token = "{}{}".format(
        proquint.hex2quint_str(secrets.token_hex(4)).replace('-',''),
        proquint.hex2quint_str(secrets.token_hex(4)).replace('-',''),
    )
    return token


def parameters_placeholder():
    return '"foobar-{}"'.format(get_secret_token())


def translate(
    piece: Path,
    parameters: dict = dict(),
):
    secrets_map = {}
    c_code = list()

    # loading piece from json file
    piece = Piece.from_json(piece)

    # map inputs with provided parameters
    # PoC using a placeholder while recipes aren't implemented
    inputs_map = {
        input: parameters.get(input, parameters_placeholder())
        for input in piece.inputs
    }

    # include the various headers
    for header in piece.headers:
        header_line = f"#include <{header}>"
        c_code.append(header_line)
    if piece.headers:
        c_code.append("\r\n")

    # initialise the various variables with random names
    for variable in piece.variables:
        is_ptr = variable.name[0] == '*'

        if is_ptr:
            variable.name = variable.name[1:]

        secret = get_secret_token()
        while secret in secrets_map.values():
            secret = get_secret_token()
        secrets_map[variable.name] = secret

        if is_ptr:
            secret = f"*{secret}"
        variable_line = f"{variable.type} {secret}"
        if variable.value:
            variable_line += f" = {variable.value}"
        variable_line += ';'
        c_code.append(variable_line)

    if piece.variables:
        c_code.append("\r\n")

    # starting main function
    c_code.append("int main()")
    c_code.append("{")

    # add setup code with replaced input values and variable names
    for code in piece.setupcode:
        for input in inputs_map:
            code = code.replace(input, inputs_map[input])
        for variable in secrets_map:
            code = code.replace(variable, secrets_map[variable])
        c_code.append(f"\t{code}")

    # add core code with replaced input values and variable names
    for code in piece.corecode:
        for input in inputs_map:
            code = code.replace(input, inputs_map[input])
        for variable in secrets_map:
            code = code.replace(variable, secrets_map[variable])
        c_code.append(f"\t{code}")

    # add teardown code with replaced input values and variable names
    for code in piece.teardowncode:
        for input in inputs_map:
            code = code.replace(input, inputs_map[input])
        for variable in secrets_map:
            code = code.replace(variable, secrets_map[variable])
        c_code.append(f"\t{code}")

    # wrapping up main function
    c_code.append("\treturn 0;")
    c_code.append("}")

    c_code = '\r\n'.join(c_code)
    # c_code = c_code.encode()

    return c_code


def routine(piece, products):
    print(piece)
    code = translate(piece)

    with tempfile.TemporaryDirectory() as input_folder:
        input_path = Path(input_folder) / piece.name.replace('.json', '.c')
        with input_path.open("w") as cfile:
            cfile.write(code)

        output_path = Path(products) / piece.name.replace('.json', '.exe')

        args = ["x86_64-w64-mingw32-gcc", "-o", output_path.as_posix(), input_path.as_posix()]
        sobject = subprocess.run(args, capture_output=True, check=False)
        if sobject.returncode != 0:
            print(sobject.__dict__)

    return output_path


def main(pieces, products):
    pieces = Path(pieces)
    for piece in pieces.glob('*.json'):
        output_path = routine(piece, products)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="I am the Architect. I've been waiting for you."
    )
    parser.add_argument(
        '--pieces',
        help='path towards the pieces root folder',
        type=Path,
    )
    parser.add_argument(
        '--products',
        help='path towards the products (output) folder',
        type=Path,
    )
    args = parser.parse_args()

    main(args.pieces, args.products)
