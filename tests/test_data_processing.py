import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "software"))
from dashboard import mock_sample, write_csv, summarize


def test_mock_sample_ranges():
    s = mock_sample(1.0)
    assert 46 < s.v_in < 50
    assert 11.5 < s.v_out < 12.5
    assert 0.8 < s.efficiency < 1.0
    assert s.mode == "BUCK"


def test_csv_roundtrip(tmp_path):
    samples = [mock_sample(i * 0.05) for i in range(10)]
    p = tmp_path / "t.csv"
    write_csv(samples, str(p))
    assert p.read_text().splitlines()[0].startswith("t,")


def test_summarize():
    samples = [mock_sample(i) for i in range(20)]
    s = summarize(samples)
    assert s["eff_avg"] > 0.8
    assert s["faults"] == 0
