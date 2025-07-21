# Moves.py  – drop-in replacement
import pathlib
from typing import List, Tuple


class Moves:

    def __init__(self, txt_path: pathlib.Path, dims: Tuple[int, int]):
        self.dims = dims  # (rows, cols)
        self.rules = self._load_rules(txt_path)

    def _load_rules(self, txt_path: pathlib.Path) -> List[Tuple[int, int]]:
        """Load move rules from a text file. Each line: dr,dc"""
        rules = []
        with open(txt_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split(",")
                if len(parts) == 2:
                    try:
                        dr = int(parts[0])
                        dc = int(parts[1])
                        rules.append((dr, dc))
                    except ValueError:
                        pass  # ignore invalid lines
        return rules

    def get_moves(self, r: int, c: int) -> List[Tuple[int, int]]:
        """Get all possible moves from a given position."""
        moves = []
        max_r, max_c = self.dims
        for dr, dc in self.rules:
            nr, nc = r + dr, c + dc
            if 0 <= nr < max_r and 0 <= nc < max_c:
                moves.append((nr, nc))
        return moves
