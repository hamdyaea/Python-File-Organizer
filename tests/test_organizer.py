# Developer: Hamdy Abou El Anein
# Contact: info@daylightlinux.ch
# SPDX-License-Identifier: GPL-3.0-only
import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

spec = importlib.util.spec_from_file_location("organizer", Path(__file__).resolve().parents[1] / "organizer.py")
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)

class OrganizerTests(unittest.TestCase):
    def test_dry_run_does_not_move(self):
        with TemporaryDirectory() as folder:
            directory = Path(folder)
            source = directory / "image.JPG"
            source.write_text("test")
            self.assertEqual(app.organize(directory), (0, 0))
            self.assertTrue(source.exists())
    def test_apply_moves_without_overwrite(self):
        with TemporaryDirectory() as folder:
            directory = Path(folder)
            (directory / "image.jpg").write_text("new")
            (directory / "Images").mkdir()
            (directory / "Images" / "image.jpg").write_text("old")
            self.assertEqual(app.organize(directory, apply=True), (0, 1))
            self.assertEqual((directory / "Images" / "image.jpg").read_text(), "old")
    def test_apply_organizes_file(self):
        with TemporaryDirectory() as folder:
            directory = Path(folder)
            (directory / "note.txt").write_text("content")
            self.assertEqual(app.organize(directory, apply=True), (1, 0))
            self.assertEqual((directory / "Documents" / "note.txt").read_text(), "content")
            self.assertFalse((directory / "note.txt").exists())

if __name__ == "__main__":
    unittest.main()
