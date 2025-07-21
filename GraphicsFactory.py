import pathlib

from Graphics import Graphics


class GraphicsFactory:
    def load(self,
             sprites_dir: pathlib.Path,
             cfg: dict,
             cell_size: tuple[int, int]) -> Graphics:
        """Load graphics from sprites directory with configuration."""
        """
        יוצר אובייקט Graphics חדש לפי הגדרות:
        - sprites_dir: תיקיית הספרייטים (תמונות הכלים/אנימציות)
        - cfg: מילון הגדרות (למשל fps, loop)
        - cell_size: גודל תא בלוח (פיקסלים)
        """
        fps = cfg.get("fps", 6.0)
        loop = cfg.get("loop", True)
        return Graphics(
            sprites_folder=sprites_dir,
            cell_size=cell_size,
            loop=loop,
            fps=fps
        )
    