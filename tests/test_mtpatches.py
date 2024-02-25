import os
import sys
import unittest

TESTS_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = os.path.dirname(TESTS_DIR)
TESTS_DATA_DIR = os.path.join(TESTS_DIR, "data")

if __name__ == "__main__":
    # Allow it to run without pytest.
    sys.path.insert(0, REPO_DIR)

from pyenliven.mtpatches import (  # noqa F402
    get_shallowest_files_sub,
    diff_only_head,
    find_mod,
    find_modpack,
)


class TestMTPatches(unittest.TestCase):
    def test_get_shallowest_files_sub(self):
        sub = get_shallowest_files_sub(
            os.path.join(TESTS_DATA_DIR, "base")
        )
        self.assertEqual(sub, os.path.join("unused", "sub", "has_file"))
        # ^ should be "has_file" dir, since that contains
        #   "shallowest_in_base.txt"

    def test_get_shallowest_files_not_in_sub(self):
        sub = get_shallowest_files_sub(
            os.path.join(TESTS_DATA_DIR, "base", "unused", "sub", "has_file"),
            log_level=1,
        )
        self.assertEqual(sub, "")
        # ^ should be "has_file" dir, since that contains
        #   "shallowest_in_base.txt"

    def test_diff_only_head__different_file(self):
        base = os.path.join(TESTS_DATA_DIR, "base", "unused", "sub")
        head = os.path.join(TESTS_DATA_DIR, "head", "unused", "sub")
        # ^ use deeper dir to skip new file in head/unused/
        #   (See test_diff_only_head__new_file for that).
        diffs = diff_only_head(
            base,
            head,
        )
        self.assertEqual(
            diffs,
            [
                {
                    'rel': os.path.join("has_file", "shallowest_in_base.txt"),
                    'code': 1,
                },
            ]
        )

    def test_diff_only_head__new_file(self):
        base = os.path.join(TESTS_DATA_DIR, "base")
        head = os.path.join(TESTS_DATA_DIR, "head")
        diffs = diff_only_head(
            base,
            head,
        )
        self.assertEqual(
            diffs,
            [
                {
                    'rel': os.path.join("unused", "sub", "has_file",
                                        "shallowest_in_base.txt"),
                    'code': 1,
                },
                {
                    'rel': os.path.join("unused", "shallower_file.txt"),
                    'code': 1,
                    'new': True,
                },
            ]
        )

    def test_diff_only_head__same(self):
        base = os.path.join(TESTS_DATA_DIR, "base-same")
        head = os.path.join(TESTS_DATA_DIR, "head-same")
        diffs = diff_only_head(
            base,
            head,
        )
        # Same except ignore extra_file_to_ignore.txt:
        self.assertFalse(diffs)  # assert same (ignoring base extra file(s))

    def test_find_mod(self):
        game_path = os.path.join(TESTS_DATA_DIR, "mod_game")
        self.assertEqual(
            find_mod(game_path, "wrong_mod"),
            None
        )
        self.assertEqual(
            find_mod(game_path, "mod1"),
            os.path.join("mods", "extra_parent", "modpack1", "mod1")
        )
        self.assertEqual(
            find_mod(os.path.join(TESTS_DATA_DIR, "modpack_game"), "mod2"),
            os.path.join("mods", "extra_parent", "modpack2", "mod2")
        )

        self.assertEqual(
            find_mod(os.path.join(game_path, "mods", "extra_parent",
                                  "modpack1", "mod1"),
                     "mod1"),  # Yes, should still find mod1 ("") if root
            ""
        )
        self.assertEqual(
            find_mod(os.path.join(game_path, "mods"), "mod1"),
            os.path.join("extra_parent", "modpack1", "mod1"),
        )

    def test_find_modpack(self):
        game_path = os.path.join(TESTS_DATA_DIR, "modpack_game")
        self.assertEqual(
            find_modpack(game_path, "wrong_modpack"),
            None
        )
        self.assertEqual(
            find_modpack(game_path, "modpack1"),
            os.path.join("mods", "extra_parent", "modpack1")
        )
        self.assertEqual(
            find_modpack(os.path.join(TESTS_DATA_DIR, "modpack_game"),
                         "modpack2"),
            os.path.join("mods", "extra_parent", "modpack2")
        )

        self.assertEqual(
            find_modpack(os.path.join(game_path, "mods", "extra_parent",
                                      "modpack1"),
                         "modpack1"),  # Yes, still find mod1 ("") if root
            ""
        )
        self.assertEqual(
            find_modpack(os.path.join(game_path, "mods", "extra_parent",
                                      "modpack2"),
                         "modpack2"),  # Yes, still find mod1 ("") if root
            ""
        )

        self.assertEqual(
            find_modpack(os.path.join(game_path, "mods"), "modpack1"),
            os.path.join("extra_parent", "modpack1"),
        )


if __name__ == "__main__":
    unittest.main()
