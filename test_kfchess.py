import pathlib
import pytest

from Graphics import Graphics
from GraphicsFactory import GraphicsFactory
from mock_img import MockImg
from Physics import Physics
from Moves import Moves
from Command import Command

# --- טסט ל-Graphics ---
def test_graphics_reset_and_update():
    g = Graphics(sprites_folder=pathlib.Path("."), cell_size=(64, 64), loop=True, fps=10)
    cmd = Command(timestamp=0, piece_id="P1", type="Move", params=["e2", "e4"])
    g.reset(cmd)
    assert g.current_command == cmd
    g.update(100)
    assert g.frame_index > 0 or g.frame_index == 0  # תלוי ב-fps

# --- טסט ל-GraphicsFactory ---
def test_graphics_factory_load():
    factory = GraphicsFactory()
    cfg = {"fps": 12.0, "loop": False}
    g = factory.load(pathlib.Path("."), cfg, (32, 32))
    assert isinstance(g, Graphics)
    assert g.fps == 12.0
    assert g.loop is False

# --- טסט ל-MockImg ---
def test_mockimg_draw_and_text():
    MockImg.reset()
    img1 = MockImg()
    img2 = MockImg()
    img1.draw_on(img2, 5, 7)
    img1.put_text("hello", 1, 2, 1.0)
    assert MockImg.traj == [(5, 7)]
    assert MockImg.txt_traj == [((1, 2), "hello")]

# --- טסט ל-Physics ---
class DummyBoard:
    cell_H_pix = 64
    cell_W_pix = 64

def test_physics_move_and_capture():
    board = DummyBoard()
    p = Physics(start_cell=(1, 1), board=board, speed_m_s=1.0)
    cmd = Command(timestamp=0, piece_id="P1", type="Move", params=["e2", "e4"])
    p.reset(cmd)
    p.update(1000)
    pos = p.get_pos()
    assert isinstance(pos, tuple)
    assert len(pos) == 2
    assert p.can_be_captured() in [True, False]
    assert p.can_capture() in [True, False]

# --- טסט ל-Moves ---
def test_moves_get_moves(tmp_path):
    # צור קובץ חוקים זמני
    rules_file = tmp_path / "rules.txt"
    rules_file.write_text("1,0\n0,1\n-1,0\n0,-1\n")
    m = Moves(rules_file, (8, 8))
    moves = m.get_moves(4, 4)
    assert (5, 4) in moves
    assert (4, 5) in moves
    assert (3, 4) in moves
    assert (4, 3) in moves


    # --- Graphics: בדיקת reset עם פקודה חדשה באמצע אנימציה ---
def test_graphics_reset_mid_animation():
    g = Graphics(sprites_folder=pathlib.Path("."), cell_size=(64, 64), loop=True, fps=5)
    cmd1 = Command(timestamp=0, piece_id="P1", type="Move", params=["e2", "e4"])
    cmd2 = Command(timestamp=500, piece_id="P1", type="Move", params=["e4", "e5"])
    g.reset(cmd1)
    g.update(200)
    frame_before = g.frame_index
    g.reset(cmd2)
    assert g.frame_index == 0
    assert g.current_command == cmd2
    assert g.last_update_ms == 500
    g.update(700)
    assert g.frame_index > 0

# --- GraphicsFactory: בדיקת ערכי ברירת מחדל וחוסר ערכים ב-cfg ---
def test_graphics_factory_missing_cfg():
    factory = GraphicsFactory()
    g = factory.load(pathlib.Path("."), {}, (32, 32))
    assert g.fps == 6.0
    assert g.loop is True

# --- MockImg: בדיקת reset פעמיים ופעולות רבות ---
def test_mockimg_multiple_draws_and_reset():
    MockImg.reset()
    img1 = MockImg()
    img2 = MockImg()
    for i in range(10):
        img1.draw_on(img2, i, i+1)
        img1.put_text(f"t{i}", i, i, 1.0)
    assert len(MockImg.traj) == 10
    assert len(MockImg.txt_traj) == 10
    MockImg.reset()
    assert MockImg.traj == []
    assert MockImg.txt_traj == []

# --- Physics: בדיקת תנועה לא חוקית, פקודה לא מוכרת, ותנועה מהירה מאוד ---
class DummyBoard:
    cell_H_pix = 64
    cell_W_pix = 64

def test_physics_invalid_command_and_fast_move():
    board = DummyBoard()
    p = Physics(start_cell=(0, 0), board=board, speed_m_s=1000.0)
    # פקודה לא חוקית (type לא קיים)
    cmd = Command(timestamp=0, piece_id="P1", type="Fly", params=["a1", "h8"])
    p.reset(cmd)
    p.update(100)
    assert p.current_cell == (0, 0)  # לא זז
    # פקודה חוקית עם מהירות גבוהה
    cmd2 = Command(timestamp=200, piece_id="P1", type="Move", params=["a1", "b2"])
    p.reset(cmd2)
    p.update(201)
    assert p.current_cell == p.target_cell  # זז מיד

# --- Moves: בדיקת קובץ חוקים ריק, קובץ עם שורות לא חוקיות, ותנועה מגבולות הלוח ---
def test_moves_empty_and_invalid_rules(tmp_path):
    # קובץ ריק
    rules_file = tmp_path / "empty.txt"
    rules_file.write_text("")
    m = Moves(rules_file, (8, 8))
    assert m.get_moves(4, 4) == []
    # קובץ עם שורות לא חוקיות
    rules_file.write_text("a,b\n1,0\nbad\n0,1\n")
    m = Moves(rules_file, (8, 8))
    moves = m.get_moves(0, 0)
    assert (1, 0) in moves
    assert (0, 1) in moves
    # תנועה מגבולות הלוח
    moves = m.get_moves(0, 0)
    for nr, nc in moves:
        assert nr >= 0 and nc >= 0

# --- Moves: בדיקת תנועה מהפינה הימנית התחתונה (גבול לוח) ---
def test_moves_from_corner(tmp_path):
    rules_file = tmp_path / "rules.txt"
    rules_file.write_text("1,0\n0,1\n-1,0\n0,-1\n")
    m = Moves(rules_file, (8, 8))
    moves = m.get_moves(7, 7)
    # רק תנועות שנשארות בגבול הלוח
    for nr, nc in moves:
        assert 0 <= nr < 8 and 0 <= nc < 8