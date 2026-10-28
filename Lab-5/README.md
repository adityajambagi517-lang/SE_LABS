# Lab 5: Static Code Analysis

**Student:** Aditya Basavaraj Jambagi  
**SRN:** PES2UG24C030

## Objective
Improve Python code quality, security, and formatting using PyLint, Bandit, and Flake8.

## Files
- `address_book.py` — updated address-book program.
- `README.md` — lab notes and commands.

## Changes made
- Replaced unsafe pickle-based backup/restore with JSON and basic structure validation.
- Replaced MD5-based contact identifiers with SHA-256.
- Removed an unused hard-coded password.
- Improved function naming, docstrings, exception handling, and formatting.
- Added an entry-point guard so the demo runs only when the file is executed directly.

## Run the program
```bash
python address_book.py
```

## Run static analysis
Install tools:
```bash
python -m pip install pylint bandit flake8
```

Run each tool and save its output:
```bash
pylint address_book.py > pylint_report.txt
bandit -r address_book.py -f txt -o bandit_report.txt
flake8 address_book.py > flake8_report.txt
```

Review the actual generated reports before submitting; results can vary with tool versions.

## Repositories
- Original repository: https://github.com/SETAPESU26/L5_27_address_book
- Updated fork: https://github.com/adityajambagi517-lang/L5_27_address_book
