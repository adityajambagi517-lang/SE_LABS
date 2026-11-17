@'
# Lab 7 – Fuzz Testing: Traffic Fine Calculator

## Objective
To identify input validation bugs using Python Hypothesis and pytest.

## Project Files

| File | Description |
|---|---|
| traffic_fine.py | Traffic fine calculator implementation |
| test_traffic_fine.py | Hypothesis-based fuzz tests |
| README.md | Lab documentation |
| evidence/ | Screenshots of test results and execution |

## Functions Tested

1. `parse_ticket_id()` – Parses traffic ticket IDs.
2. `total_fines()` – Calculates total fines with a maximum cap of 10,000.
3. `speed_excess()` – Calculates the percentage by which speed exceeds the limit.

## Tools Used
- Python
- pytest
- Hypothesis

## Installation

```bash
python -m pip install pytest hypothesis