# Secure Code Review: Flask app

Language: Python (Flask). Method: manual review plus static analysis (Bandit). `vulnerable/app.py` is deliberately insecure; `fixed/app.py` is the remediated version.

| # | Finding | Location | CWE | OWASP 2021 | Severity | Fix |
|---|---|---|---|---|---|---|
| 1 | SQL injection via f-string query | `/login` | CWE-89 | A03 Injection | Critical | Parameterised queries |
| 2 | OS command injection (`shell=True`) | `/ping` | CWE-78 | A03 Injection | Critical | Validate host, pass args as list, no shell |
| 3 | Insecure deserialization (`pickle.loads`) | `/load` | CWE-502 | A08 Integrity Failures | Critical | Accept JSON only |
| 4 | Template injection / XSS | `/hello` | CWE-1336 / CWE-79 | A03 Injection | High | Pass user input as template variable |
| 5 | Path traversal | `/download` | CWE-22 | A01 Broken Access Control | High | `send_from_directory` |
| 6 | Missing auth / IDOR | `/user/<id>` | CWE-639 / CWE-306 | A01 Broken Access Control | High | Require login, check ownership |
| 7 | Weak password hashing (unsalted MD5) | `/init`, `/login` | CWE-328 | A02 Cryptographic Failures | High | Salted password hashing |
| 8 | Hardcoded secret key and default admin password | top of file, `/init` | CWE-798 | A05 Misconfiguration | High | Environment variables or random key |
| 9 | Debug mode on, bound to 0.0.0.0 | `app.run` | CWE-489 | A05 Misconfiguration | High | Disable debug; bind localhost |

## How to reproduce (local, test only)
```bash
pip install flask bandit
bandit -r vulnerable/
bandit -r fixed/
python vulnerable/app.py
```

The vulnerable app is intentionally insecure and must only be run locally in an isolated test environment. Do not deploy it or expose it to a network.

## Best practices
Parameterise queries; never pass user input to a shell, `eval` or `pickle`; escape output; enforce authentication and authorisation on every route; salt and hash passwords; keep secrets out of source; disable debug in production; keep dependencies updated.
