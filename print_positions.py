#!/usr/bin/env python3
"""Utility script for turning multiple FEN strings into PNG diagrams."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import List, Optional

from PIL import Image, ImageDraw

# ---------------------------------------------------------------------------
# User configurable settings
# ---------------------------------------------------------------------------

# Location of the folder containing the piece PNG files.
PIECES_FOLDER = Path("pieces")

# Text file that holds one FEN entry per line.
FEN_INPUT_FILE = Path("chess_board_printer.txt")

# Output filename template. "{name}" will be replaced with the diagram name.
OUTPUT_NAME_TEMPLATE = "position_{name}.png"

# Size of each square in pixels. Final images are 8 * square_size on each side (default 4000×4000).
SQUARE_SIZE = 500

# Toggle whether the chess board should be rendered behind the pieces.
# Set to False to export only the pieces on a transparent background.
INCLUDE_BOARD = True

# Board colors used when INCLUDE_BOARD is True.
LIGHT_SQUARE_COLOR = "#ffffff"
DARK_SQUARE_COLOR = "#c1c1c1"


# Maps FEN characters to matching piece image filenames
FEN_TO_FILENAME = {
    'P': 'pawn_white.png',
    'N': 'knight_white.png',
    'B': 'bishop_white.png',
    'R': 'rook_white.png',
    'Q': 'queen_white.png',
    'K': 'king_white.png',
    'p': 'pawn_black.png',
    'n': 'knight_black.png',
    'b': 'bishop_black.png',
    'r': 'rook_black.png',
    'q': 'queen_black.png',
    'k': 'king_black.png',
}


def hex_to_rgba(hex_color: str, alpha: int = 255) -> tuple[int, int, int, int]:
    """Convert a hex color string ("#rrggbb") to an RGBA tuple."""

    color = hex_color.lstrip('#')
    if len(color) != 6:
        raise ValueError(f"Color '{hex_color}' must be in #rrggbb format.")
    r = int(color[0:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:6], 16)
    return (r, g, b, alpha)

def parse_fen(piece_placement: str) -> List[List[Optional[str]]]:
    """Parse the piece-placement portion of a FEN string into an 8x8 grid."""

    ranks = piece_placement.split('/')
    if len(ranks) != 8:
        raise ValueError("FEN must have 8 ranks separated by '/'.")

    board: List[List[Optional[str]]] = []
    for rank_str in ranks:
        row: List[Optional[str]] = []
        for char in rank_str:
            if char.isdigit():
                # A digit signals that many empty squares in a row.
                row.extend([None] * int(char))
            else:
                # Single piece letter (e.g. "P" or "k").
                row.append(char)
        if len(row) != 8:
            raise ValueError("One rank in FEN does not sum to 8 squares.")
        board.append(row)
    return board


def strip_to_piece_placement(fen_string: str) -> str:
    """Return only the piece-placement part of a FEN string."""

    return fen_string.split(' ')[0]


def fen_to_png(
    fen_string: str,
    square_size: int = SQUARE_SIZE,
    output_file: os.PathLike[str] | str = "diagram.png",
    include_board: bool = INCLUDE_BOARD,
    light_color: str = LIGHT_SQUARE_COLOR,
    dark_color: str = DARK_SQUARE_COLOR,
    pieces_folder: Path | str = PIECES_FOLDER,
) -> None:
    """Create a single chess diagram (PNG) from a FEN string."""

    piece_placement = strip_to_piece_placement(fen_string)
    board = parse_fen(piece_placement)

    image_size = (8 * square_size, 8 * square_size)

    if include_board:
        out_img = Image.new('RGBA', image_size, hex_to_rgba(light_color))
        draw = ImageDraw.Draw(out_img)
        dark = hex_to_rgba(dark_color)
        for rank in range(8):
            for file in range(8):
                if (rank + file) % 2 == 1:
                    x0 = file * square_size
                    y0 = rank * square_size
                    x1 = x0 + square_size
                    y1 = y0 + square_size
                    draw.rectangle([x0, y0, x1, y1], fill=dark)
    else:
        # Transparent background when the board is not required.
        out_img = Image.new('RGBA', image_size, (0, 0, 0, 0))

    pieces_folder = Path(pieces_folder)

    # Paste each piece at the correct rank/file position.
    for r, rank in enumerate(board):
        for f, piece in enumerate(rank):
            if piece is None:
                continue
            filename = FEN_TO_FILENAME.get(piece)
            if not filename:
                continue
            piece_path = pieces_folder / filename
            piece_img = Image.open(piece_path).convert('RGBA')
            piece_img = piece_img.resize((square_size, square_size), Image.LANCZOS)
            x_offset = f * square_size
            y_offset = r * square_size
            out_img.alpha_composite(piece_img, (x_offset, y_offset))

    out_img.save(output_file, 'PNG')
    print(f"Saved: {output_file}")

def sanitize_name(name: str) -> str:
    """Return a filesystem-friendly representation of *name*."""

    return re.sub(r'[^A-Za-z0-9_\-]+', '', name)


def process_fen_file(
    filename: Path | str = FEN_INPUT_FILE,
    square_size: int = SQUARE_SIZE,
    include_board: bool = INCLUDE_BOARD,
) -> None:
    """Process each "FEN -> Name;" line in *filename* into individual PNGs."""

    file_path = Path(filename)
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return

    lines = file_path.read_text(encoding='utf-8').splitlines()

    for i, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue  # ignore empty or comment lines
        if '->' not in line:
            continue

        fen_part, name_part = line.split('->', 1)
        fen_part = fen_part.strip()
        name_part = name_part.strip()
        if name_part.endswith(';'):
            name_part = name_part[:-1].strip()

        safe_name = sanitize_name(name_part)
        if not safe_name:
            safe_name = f"diagram_{i}"
        output_file = OUTPUT_NAME_TEMPLATE.format(name=safe_name)

        try:
            fen_to_png(
                fen_part,
                square_size=square_size,
                output_file=output_file,
                include_board=include_board,
            )
        except ValueError as error:
            print(f"[Line {i}] FEN error: {error}")
        except Exception as error:
            print(f"[Line {i}] Error: {error}")


def main() -> None:
    """Entry point when running this module as a script."""

    process_fen_file()


if __name__ == '__main__':
    main()
