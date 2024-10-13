# import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from r2t.r2t import parse_ignore_pattern  


def test_parse_ignore_pattern():
    pattern, is_negation = parse_ignore_pattern("*.py")
    assert not is_negation
    assert pattern.search("test.py")
    assert not pattern.search("test.txt")

# Add more tests here
