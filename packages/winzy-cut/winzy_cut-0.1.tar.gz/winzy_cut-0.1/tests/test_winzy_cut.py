import pytest
import winzy_cut as w

def test_cut():
    text = "apple,banana,orange\n1,2,3\nx,y,z"
    expected_output = "apple\n1\nx"
    assert w.cut_text(text, ",", [1]) == expected_output
