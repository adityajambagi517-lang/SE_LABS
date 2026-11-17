# Lab 6 – Coverage evidence

The following results were captured from the Windows PowerShell terminal after running the commands in the parent README.

## Line coverage

```powershell
py -m coverage erase
py -m coverage run -m pytest -q CodeCoverageTest_traffic_fine.py
py -m coverage report -m traffic_fine.py
```

Terminal result:

```text
15 passed in 0.08s

Name             Stmts   Miss   Cover   Missing
traffic_fine.py     35      0   100%
TOTAL               35      0   100%
```

## Branch coverage

```powershell
py -m coverage erase
py -m coverage run --branch -m pytest -q BranchCoverageTest_traffic_fine.py
py -m coverage report -m traffic_fine.py
```

Terminal result:

```text
20 passed in 0.13s

Name             Stmts   Miss   Branch   BrPart   Cover   Missing
traffic_fine.py     35      0      26       0     100%
TOTAL               35      0      26       0     100%
```

## Summary

| Measurement | Result |
|---|---:|
| Line-coverage tests | 15 passed |
| Line coverage | 100% |
| Branch-coverage tests | 20 passed |
| Branch outcomes | 26 covered, 0 partial |
| Branch coverage | 100% |

The terminal screenshot provided for this lab shows both reports in one PowerShell session. This Markdown evidence preserves the readable command/output record in the repository.
