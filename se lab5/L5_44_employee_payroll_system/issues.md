# Lab 5: Static Code Analysis — Issue Report

## 1. Objective

Analyze the Employee Payroll System using Pylint, Bandit, and Flake8, fix the identified issues, and verify the improvements.

## 2. Issues Identified and Fixes

| Issue | Tool | Type | Fix applied |
|---|---|---|---|
| Mutable default argument `[]` | Pylint | Bug | Replaced with `None` and initialized inside the function |
| Missing function docstrings | Pylint | Code quality | Added docstrings |
| Invalid function naming | Pylint | Style | Changed `processSalary` to `process_salary` |
| Bare exception handler | Pylint, Flake8, Bandit | Error handling | Removed the broad exception handler and validated inputs |
| Unsafe `eval()` | Pylint, Bandit | Security | Replaced with direct salary calculation |
| MD5 hashing | Bandit | Security | Replaced MD5 with SHA-256 |
| Insecure random token generation | Bandit | Security | Used the `secrets` module |
| Shell command execution | Bandit | Security | Removed `os.system()` |
| Hardcoded payroll key exposure | Manual review | Security | Removed the hardcoded key and its print statement |
| Unused imports and variables | Pylint, Flake8 | Code quality | Removed unused items |
| Missing file encoding and resource management | Pylint | Reliability | Used a context manager and UTF-8 encoding |
| Long line and missing final newline | Flake8 | Formatting | Corrected formatting |

## 3. Before-and-After Results

| Tool | Before | After |
|---|---|---|
| Pylint | 5.32/10 | 10.00/10 |
| Bandit | 5 findings | 0 findings |
| Flake8 | 7 reported issues | No issues reported |

## 4. Conclusion

Static analysis helped identify code-quality, security, and formatting problems in the Employee Payroll System. After applying the fixes, the program executed successfully, Pylint achieved a score of 10.00/10, Bandit reported no issues, and Flake8 reported no issues.