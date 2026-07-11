import unittest

from update import parse


class ParseTest(unittest.TestCase):
    def test_extracts_and_validates_namespaced_entries(self):
        xml = b'<ArrayOfstring xmlns="urn:test"><string>192.0.2.1</string><string>192.0.2.0/24</string></ArrayOfstring>'
        self.assertEqual(parse(xml, 4), ["192.0.2.1", "192.0.2.0/24"])
        with self.assertRaises(ValueError):
            parse(xml, 6)


if __name__ == "__main__":
    unittest.main()
