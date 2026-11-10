# CodeAlpha Secure Coding Review

A Flask secure-code-review exercise comparing an intentionally vulnerable training sample with a remediated implementation.

## Structure
- `vulnerable/app.py` — deliberately insecure code for local review only; do not deploy or expose it to a network.
- `fixed/app.py` — example remediated implementation.
- `REVIEW.md` — findings mapped to CWE and OWASP categories.

## Setup
```bash
python -m venv .venv
# Activate the environment, then:
pip install -r requirements.txt
```

Set `ADMIN_PASSWORD` before starting the fixed app if you want the sample admin account initialized. Set `SECRET_KEY` to a strong random value for a stable session key.

## Security note
The vulnerable application intentionally demonstrates common flaws. Run it only in an isolated local lab. The fixed example is educational and should receive a project-specific security review before production use.