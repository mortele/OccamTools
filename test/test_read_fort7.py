import os
import sys
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from read_fort7 import Fort7  # noqa: E402


def _load_example_fort7():
    file_name = os.path.join(os.path.dirname(__file__), '..', 'data',
                             'example_fort.7')
    fort7 = Fort7(file_name)
    fort7.read_file()
    return fort7, file_name


def test_read_fort7_file():
    new_file_name = os.path.join(os.path.dirname(__file__), '..', 'data',
                                 'example_fort_new.7')

    fort7, file_name = _load_example_fort7()
    assert fort7.title == 'example-fort.1'

    with open(file_name, 'r') as in_file, open(new_file_name, 'w') as out_file:
        for line in in_file:
            if 'title' in line:
                line = 'title: new_title\n'
            out_file.write(line)
    fort7 = Fort7(file_name)
    fort7.read_file(new_file_name)
    assert fort7.title == 'new_title'
    os.remove(new_file_name)


def test_read_fort7_array_length():
    fort7, _ = _load_example_fort7()
    print(fort7.step)
    assert fort7.step.shape[0] == 11
    assert fort7.step[-1] == 100


def test_read_fort7_values():
    fort7, _ = _load_example_fort7()
    assert (fort7.kinetic_energy[-1]
            == pytest.approx(30.761054436014966, abs=1e-15))
    assert (fort7.kinetic_energy[2]
            == pytest.approx(31.428657349367572, abs=1e-15))
    assert (fort7.pressure_pf_0[7]
            == pytest.approx(-30.651382977837372, abs=1e-15))
    expected = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    assert all([s == e for s, e in zip(fort7.step, expected)])