# Automation

| Script | Purpose |
|---|---|
| `bootstrap_github.py` | Creates labels (`.github/labels.yml`), milestones v0.1 to v1.0 and the 28 backlog issues (`backlog/initial-backlog.csv`) with the GitHub CLI. Dry run by default. |
| `../platforms/microsoft-purview/scripts/*.ps1` | Lab policy creation and sanitised configuration export |
| `../synthetic-data-generator` (`python -m dlpgen`) | Corpus generation and validators, also run in CI |

```bash
gh auth login
python automation/bootstrap_github.py --repo <owner>/<repo>          # review the commands
python automation/bootstrap_github.py --repo <owner>/<repo> --apply
```

Planned (backlog): regression runner (#29), configuration drift check (#30), exception reconciliation (#24), KPI computation (#25).
