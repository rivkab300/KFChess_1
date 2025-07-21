from Command import Command
from Moves import Moves
from Graphics import Graphics
from Physics import Physics
from State import State
from typing import Dict
import time
from typing import Dict, Optional


class State:
    def __init__(self, moves: Moves, graphics: Graphics, physics: Physics):
        """Initialize state with moves, graphics, and physics components."""
        """
        מאתחל מצב (State) עם רכיבי מהלכים, גרפיקה ופיזיקה.
        transitions: מילון מעבר בין מצבים לפי אירועים (event).
        """
        self._moves = moves
        self._graphics = graphics
        self._physics = physics
        self.transitions: Dict[str, "State"] = {}
        self._current_command: Optional[Command] = None


    def set_transition(self, event: str, target: State):
        """Set a transition from this state to another state on an event."""
        # event= "Move"
        """
        קובע מעבר ממצב זה למצב אחר על פי אירוע (event).
        לדוג' event="Move" יעביר ל-state אחר.
        """
        self.transitions[event] = target

    def reset(self, cmd: Command):
        """
        מאתחל את המצב עם פקודה חדשה (למשל, התחלת תנועה).
        """
        self._current_command = cmd
        self._graphics.reset(cmd)
        self._physics.reset(cmd)

    def update(self, now_ms: int) -> State:
        """Update the state based on current time."""
        self._graphics.reset(now_ms)
        cmd = self._physics.reset(now_ms)
        if cmd is not None:
            return self.process_command(cmd)

        return self
        # """
        # מעדכן את המצב לפי הזמן הנוכחי.
        # - מעדכן גרפיקה ופיזיקה.
        # - בודק אם יש פקודה חדשה (למשל, סיום תנועה) ומעביר למצב הבא אם צריך.
        # """
        # self._graphics.update(now_ms)
        # self._physics.update(now_ms)
        # # דוגמה: אם הפיזיקה סיימה תנועה, אפשר לעבור למצב הבא
        # if self.can_transition(now_ms):
        #     cmd = self.get_command()
        #     if cmd and cmd.type in self.transitions:
        #         next_state = self.transitions[cmd.type]
        #         next_state.reset(cmd)
        #         return next_state
        # return self

    def process_command(self, cmd: Command, now_ms: int) -> State:
        """Get the next state after processing a command."""
        # Command = QBMe5e8
        # transitions = {
        #     "Move" : state_move
        #     "Jump" : state_jmp
        # }
        # res = self.transitions[cmd.type]
        # if res is None:
        #     return None

        # res.reset(cmd.timestamp)
        # return res
        """
        מעבד פקודה ומחזיר את המצב הבא (אם יש מעבר).
        """
        if cmd.type in self.transitions:
            next_state = self.transitions[cmd.type]
            next_state.reset(cmd)
            return next_state
        return self


    def can_transition(self, now_ms: int) -> bool:           # customise per state
        """Check if the state can transition."""
        """
        בודק האם אפשר לעבור למצב אחר (למשל, האם התנועה הסתיימה).
        כאן אפשר להגדיר לוגיקה מותאמת לכל מצב.
        """
        # דוגמה: מעבר אפשרי רק אם הפיזיקה לא בתנועה
        return not self._physics.is_moving


    def get_command(self) -> Command:
        """Get the current command for this state."""
        """
        מחזיר את הפקודה הנוכחית של המצב (אם יש).
        """
        return self._current_command