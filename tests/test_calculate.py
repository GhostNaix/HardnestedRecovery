import os.path
import pathlib
from FlipperNested.main import FlipperNested

def test_calculate_hard():
    file = str(pathlib.Path(__file__).parent.resolve()) + "/.clean_nonces"
    if os.path.isfile(file):
        keys = FlipperNested.calculate_keys_hard(0x773D6B86, file)
        assert keys == "89eca97f8c2a;"
