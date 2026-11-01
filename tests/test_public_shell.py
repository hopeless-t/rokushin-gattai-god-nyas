import unittest

from godnyas import GodNyasSet


class Stub:
    def __init__(self, suffix):
        self.suffix = suffix

    def invoke(self, task):
        return f"{task}{self.suffix}"


class Composer:
    def compose(self, task, *, parts):
        value = task
        for part in parts:
            value = part.invoke(value)
        return value


class PublicShellTest(unittest.TestCase):
    def test_opaque_parts_compose(self):
        result = GodNyasSet(parts=[Stub("a"), Stub("b")], composer=Composer()).run("x")
        self.assertEqual(result.value, "xab")
        self.assertEqual(result.receipt.part_count, 2)


if __name__ == "__main__":
    unittest.main()
