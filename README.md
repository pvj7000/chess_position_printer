# chess_position_printer

A small Pillow-based helper that turns lists of FEN strings into PNG diagrams.

<img width="500" height="500" alt="position_queens-gambit-2" src="https://github.com/user-attachments/assets/d873df2c-31f7-4fff-a40f-59af1ae0537d" />

example: queen's gambit

### ♟️ About This Project

This Python script uses the **Pillow** library to generate **custom chess board diagrams** as PNG images.  
It allows you to visualize and print chess positions from FEN strings, design unique piece styles, and export diagrams for use in books, websites, or training materials.  
The script is lightweight, open-source, and perfect for **developers, chess teachers, and enthusiasts** who want to automate or personalize chess illustrations with clean, printable output.

**Tags:** `#chess #python #pillow #diagram-generator #chessboard #chess-diagram #image-generator #open-source #fen #board-visualizer`


## Requirements

- Python 3.9 or newer.
- [Pillow](https://pypi.org/project/pillow/) (`pip install pillow`).

## Preparing your inputs

1. Add one position per line inside `chess_board_printer.txt` using the format:
   ```
   <FEN string> -> <diagram name>;
   ```
   Lines starting with `#` are ignored so you can keep notes in the same file.
2. Keep your piece icons (1000×1000 PNGs work well) inside the `pieces/` folder.
   The filenames must match the defaults listed in `print_positions.py`.

## Generating diagrams

Run the script from the project root:

```bash
python print_positions.py
```

Each valid entry creates `position_<diagram name>.png` in the same directory.

## Tweaking the output

All tunable values live at the top of `print_positions.py` and can be edited in place:

- `SQUARE_SIZE` controls the resolution of every board square (default 500px, resulting in 4000×4000 output).
- `INCLUDE_BOARD` toggles between a coloured board and a transparent background
  (set it to `False` for transparent output).
- `LIGHT_SQUARE_COLOR` and `DARK_SQUARE_COLOR` define the board palette.
- `OUTPUT_NAME_TEMPLATE` lets you change the naming scheme of the generated PNGs.

## Swapping piece sets

To use different artwork, replace the PNGs inside the `pieces/` folder with your
own files—keep the filenames identical so the FEN lookup table continues to work.
You can create sub-folders with alternative sets; just point `PIECES_FOLDER` to
the desired directory before running the script.
