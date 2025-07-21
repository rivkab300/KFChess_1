from typing import Tuple, Optional
from Command import Command
import math
class Physics:
    SLIDE_CELLS_PER_SEC = 4.0        # tweak to make all pieces slower/faster

    def __init__(self, start_cell: Tuple[int, int],
                 board: "Board", speed_m_s: float = 1.0):
        """Initialize physics with starting cell, board, and speed."""
        self.board = board
        self.speed_m_s = speed_m_s
        self.cell_size = (board.cell_H_pix, board.cell_W_pix)
        self.start_cell = start_cell
        self.current_cell = start_cell
        self.target_cell = start_cell
        self.cmd: Optional[Command] = None
        self.start_time_ms = 0
        self.last_update_ms = 0
        self.pos = self._cell_to_pixel(start_cell)
        self.is_moving = False

    def _cell_to_pixel(self, cell: Tuple[int, int]) -> Tuple[int, int]:
        """Convert cell coordinates to pixel coordinates."""
        r, c = cell
        return (c * self.cell_size[1], r * self.cell_size[0])
    
    def reset(self, cmd: Command):
        """Reset physics state with a new command."""
        self.cmd = cmd
        self.start_time_ms = cmd.timestamp
        self.last_update_ms = cmd.timestamp
        if cmd.type == "Move" and len(cmd.params) == 2:
            # נניח ש־params מכיל [from, to] כמו ["e2", "e4"]
            # כאן אפשר להמיר את המחרוזות למיקום לוח (r, c)
            # לדוגמה: מחרוזת "e4" → (4, 4) (בהתאם למיפוי שלך)
            self.target_cell = self._parse_cell(cmd.params[1])
            self.is_moving = True
        else:
            self.target_cell = self.current_cell
            self.is_moving = False

    def _parse_cell(self, cell_str: str) -> Tuple[int, int]:
        """Parse cell string like 'e4' to (row, col)."""
        col = ord(cell_str[0].lower()) - ord('a')
        row = int(cell_str[1]) - 1
        return (row, col)
    
    def update(self, now_ms: int):
        """Update physics state based on current time."""
        if not self.is_moving:
            return
        elapsed_sec = (now_ms - self.start_time_ms) / 1000.0
        start_px = self._cell_to_pixel(self.current_cell)
        target_px = self._cell_to_pixel(self.target_cell)
        dist_px = math.hypot(target_px[0] - start_px[0], target_px[1] - start_px[1])
        total_time_sec = dist_px / (self.cell_size[0] * self.SLIDE_CELLS_PER_SEC)
        #אם את רוצה שבמהירות גבוהה מאוד (או כאשר total_time_sec קטן מאוד) הכלי יגיע מיד ליעד, צריך לעדכן את הלוגיקה ב־u
        # update כך ש־current_cell יתעדכן ל־target_cell גם אם הזמן שחלף קטן מאוד.
        # or total_time_sec <= 0:  שנוי שהוצע בעקבות טסט כושל
        if elapsed_sec >= total_time_sec or total_time_sec <= 0:
            self.pos = target_px
            self.current_cell = self.target_cell
            self.is_moving = False
        else:
            # תנועה ליניארית בין נקודות
            ratio = elapsed_sec / total_time_sec if total_time_sec > 0 else 1
            self.pos = (
                int(start_px[0] + (target_px[0] - start_px[0]) * ratio),
                int(start_px[1] + (target_px[1] - start_px[1]) * ratio)
            )
        self.last_update_ms = now_ms

    def can_be_captured(self) -> bool: 
        """Check if this piece can be captured."""
        # דוגמה: אפשר ללכוד רק אם לא בתנועה
        return not self.is_moving
        
    def can_capture(self) -> bool:     
        """Check if this piece can capture other pieces."""
        # דוגמה: אפשר ללכוד רק אם לא בתנועה
        return not self.is_moving

    def get_pos(self) -> Tuple[int, int]:
        """
        Current pixel-space upper-left corner of the sprite.
        Uses the sub-pixel coordinate computed in update();
        falls back to the square's origin before the first update().
        """
        return self.pos