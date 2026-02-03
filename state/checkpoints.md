# Active Checkpoints

Max 10 active checkpoints. Oldest is removed when an 11th unique topic is added.

| # | Topic | Last Updated | Summary |
|---|-------|--------------|---------|
| 1 | spanskbert-expansion | 2026-02-03 | 2 nya appar + 9 nya kategorier i alla appar |

---

## How to Resume

Say any of:
- "fortsatt med [topic]"
- "visa mina checkpoints"
- "load [topic]"

Claude reads `state/checkpoints/{topic}.md` and picks up where you left off.
