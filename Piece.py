from Board import Board
from Command import Command
from State import State
import cv2


class Piece:
    def __init__(self, piece_id: str, init_state: State):
        """Initialize a piece with ID and initial state."""
        self.piece_id = piece_id
        self._state = init_state

    def on_command(self, cmd: Command, now_ms: int):
        """
        מקבל פקודה (למשל תזוזה) ומעביר אותה למצב הנוכחי.
        אם הפקודה אפשרית, מעדכן את המצב.
        """
        if self.is_command_possible(cmd):
            self._state = self._state.process_command(cmd, now_ms)
            self._state.update(now_ms)

    def is_command_possible(self, cmd: Command) -> bool:
        """
        בודק האם הפקודה אפשרית עבור הכלי (למשל, האם הכלי לא בתנועה).
        אפשר להרחיב את הלוגיקה לפי הצורך.
        """
        # דוגמה: אפשר לבצע פקודה רק אם אין פקודה נוכחית או שהמצב מאפשר מעבר
        return self._state.can_transition(cmd.timestamp)

    def reset(self, start_ms: int):
        """
        מאתחל את הכלי למצב התחלתי (למשל, לאחר אכילה או תחילת משחק).
        """
        self._state.reset(None)  # אפשר להעביר פקודה התחלתית אם צריך

    def update(self, now_ms: int):
        """
        מעדכן את מצב הכלי לפי הזמן (למשל, מקדם אנימציה/פיזיקה).
        """
        self._state = self._state.update(now_ms)

    def draw_on_board(self, board, now_ms: int):
        """
        מצייר את הכלי על הלוח, כולל שכבת קירור (cooldown) אם צריך.
        """
        img = self._state._graphics.get_img()
        pos = self._state._physics.get_pos()
        # ציור הכלי על הלוח (בהנחה שללוח יש img)
        img.draw_on(board.img, pos[0], pos[1])
        # אפשר להוסיף כאן ציור של שכבת קירור/המתנה אם הכלי לא פנוי
        if not self._state.can_transition(now_ms):
            # דוגמה: ציור חצי שקוף מעל הכלי
            overlay = img  # אפשר ליצור תמונה שקופה בגודל הכלי
            # כאן אפשר להוסיף קוד ליצירת overlay ולצייר אותו על board.img
