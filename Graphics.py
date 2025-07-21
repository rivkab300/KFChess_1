import pathlib
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import copy
from img import Img
from Command import Command



class Graphics:
    def __init__(self,
                 sprites_folder: pathlib.Path,
                 cell_size: tuple[int, int],        # NEW
                 loop: bool = True,
                 fps: float = 6.0):
        """Initialize graphics with sprites folder, cell size, loop setting, and FPS."""
        self.sprites_folder = sprites_folder
        self.cell_size = cell_size
        self.loop = loop
        self.fps = fps
        self.current_command = None
        self.frame_index = 0
        self.last_update_ms = 0

    def copy(self):
        """Create a shallow copy of the graphics object."""
        return copy.copy(self)

    def reset(self, cmd: Command):
        """Reset the animation with a new command."""
        self.current_command = cmd
        self.frame_index = 0
        self.last_update_ms = cmd.timestamp

    def update(self, now_ms: int):
        """Advance animation frame based on game-loop time, not wall time."""
        if self.current_command is None:
            return
        elapsed = now_ms - self.last_update_ms
        frame_advance = int(elapsed / (1000 / self.fps))
        if frame_advance > 0:
            self.frame_index += frame_advance
            self.last_update_ms += frame_advance * (1000 / self.fps)
            # אם יש לולאה, אפשר לאפס את frame_index בהתאם לאורך האנימציה

    def get_img(self) -> Img:
        """Get the current frame image."""
        # כאן יש לטעון את התמונה המתאימה לפי frame_index והפקודה הנוכחית
        # דוגמה גנרית:
        if self.current_command is None:
            return Img.blank(self.cell_size)
        # אפשר להוסיף כאן טעינת תמונה אמיתית לפי סוג הפקודה
        return Img.load_from_folder(self.sprites_folder, self.current_command.type, self.frame_index) 