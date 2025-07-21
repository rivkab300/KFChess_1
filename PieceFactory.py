import pathlib
from typing import Dict, Tuple
import json
from Board import Board
from GraphicsFactory import GraphicsFactory
from Moves import Moves
from PhysicsFactory import PhysicsFactory
from Piece import Piece
from State import State


class PieceFactory:
    def __init__(self, board: Board, pieces_root: pathlib.Path):
        """Initialize piece factory with board and 
        generates the library of piece templates from the pieces directory.."""
        """
        מאתחל את המפעל לכלים:
        - board: הלוח עליו הכלים יפעלו
        - pieces_root: תיקיית האב של כל סוגי הכלים (לכל סוג תיקיית משנה)
        בונה ספריית תבניות (state machine) לכל סוג כלי.
        """
        self.board = board
        self.pieces_root = pieces_root
        self.graphics_factory = GraphicsFactory()
        self.physics_factory = PhysicsFactory(board)
        self.templates: Dict[str, State] = {}
        # בנה תבניות לכל סוגי הכלים
        for piece_type_dir in pieces_root.iterdir():
            if piece_type_dir.is_dir():
                self.templates[piece_type_dir.name] = self._build_state_machine(piece_type_dir)

    def _build_state_machine(self, piece_dir: pathlib.Path) -> State:
        """Build a state machine for a piece from its directory."""
        """
        בונה מכונת מצבים (state machine) לכלי לפי התיקייה שלו.
        טוען חוקים, גרפיקה ופיזיקה מהתיקייה.
        """
        # טען חוקים
        moves_path = piece_dir / "moves.txt"
        moves = Moves(moves_path, (self.board.H_cells, self.board.W_cells))
        # טען גרפיקה
        sprites_dir = piece_dir / "sprites"
        cfg = {}  # אפשר לטעון קובץ הגדרות אם יש
        cell_size = (self.board.cell_H_pix, self.board.cell_W_pix)
        graphics = self.graphics_factory.load(sprites_dir, cfg, cell_size)
        # טען פיזיקה
        physics = self.physics_factory.create((0, 0), {})  # מיקום התחלתי דמה, יוחלף ביצירת הכלי
        # בנה מצב ראשי
        state = State(moves, graphics, physics)
        # אפשר להוסיף כאן set_transition למצבים נוספים (למשל "Jump", "Idle" וכו')
        return state

    # PieceFactory.py  – replace create_piece(...)
    def create_piece(self, p_type: str, cell: Tuple[int, int]) -> Piece:
        """Create a piece of the specified type at the given cell."""
        """
        יוצר כלי חדש מסוג p_type במיקום cell.
        משכפל את תבנית ה-state המתאימה, ומעדכן את הפיזיקה למיקום הנכון.
        """
        if p_type not in self.templates:
            raise ValueError(f"Unknown piece type: {p_type}")
        # שכפול עמוק של ה-state (כדי שכל כלי יהיה עצמאי)
        import copy
        state = copy.deepcopy(self.templates[p_type])
        # עדכן את הפיזיקה למיקום המבוקש
        state._physics.current_cell = cell
        state._physics.target_cell = cell
        state._physics.pos = state._physics._cell_to_pixel(cell)
        return Piece(piece_id=p_type, init_state=state)