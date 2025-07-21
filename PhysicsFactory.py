from Board import Board
from Physics import Physics


class PhysicsFactory:      # very light for now
    def __init__(self, board: Board): 
        """
        Initialize physics factory with board.
        שומר הפניה ללוח, כדי שכל אובייקט Physics שניצור יקבל את אותו לוח.
        """
        self.board = board

        
    def create(self, start_cell, cfg) -> Physics:
        """
        Create a physics object with the given configuration.
        start_cell: מיקום התחלתי של הכלי (tuple של (row, col))
        cfg: קונפיגורציה (למשל מהירות) - מצופה להיות dict או אובייקט עם מאפיינים רלוונטיים.
        """
        # נניח ש-cfg הוא dict עם מפתח speed_m_s, ואם לא קיים - ברירת מחדל 1.0
        speed = cfg.get("speed_m_s", 1.0) if isinstance(cfg, dict) else 1.0
        return Physics(start_cell, self.board, speed_m_s=speed)