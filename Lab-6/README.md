# Lab 6 – Code and Branch Coverage Analysis
## Traffic Fine Calculator

**Course:** Software Engineering  
**Lab:** 6 – Code and Branch Coverage Analysis  
**Application:** Traffic Fine Calculator

## Objective
Measure and improve test completeness using line coverage and branch coverage. The tests exercise the speeding fine calculation, driving-licence action rules, and total-penalty calculation.

## Application functions
- `speeding_fine(speed, limit, zone)`: calculates a fine using speed excess and road zone.
- `license_action(points, is_commercial, repeat_offender)`: returns the applicable licence action.
- `total_penalty(fines)`: totals fines, rejects negative values, and caps the total at ₹10,000.

## Requirements
- Python 3.x
- pytest
- coverage.py

Install dependencies:
```powershell
py -m pip install pytest coverage
```

## Line coverage
```powershell
py -m coverage erase
py -m coverage run -m pytest -q CodeCoverageTest_traffic_fine.py
py -m coverage report -m traffic_fine.py
```
Recorded report result: 15 tests passed; 100% line coverage.

## Branch coverage
```powershell
py -m coverage erase
py -m coverage run --branch -m pytest -q BranchCoverageTest_traffic_fine.py
py -m coverage report -m traffic_fine.py
```
Recorded report result: 20 tests passed; 100% branch coverage.

See `evidence/coverage-results.md` for coverage evidence.