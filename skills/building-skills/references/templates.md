# Templates

Copy these, then cut every line the new skill does not need.

## SKILL.md

```markdown
---
name: processing-invoices
description: Extracts line items, totals and due dates from invoice PDFs and writes them to a CSV. Use when the user has invoices, bills or receipts to read, total or reconcile, even if they never say "invoice".
---

# Processing invoices

One sentence on what this procedure produces.

## Steps

1. The first step, as a command where one exists:
   `python3 scripts/extract.py --input <pdf> --output items.csv`
2. The check that proves the step worked.

## Gotchas

- What an agent gets wrong here without being told.
```

## Test file: `evals/skills/<name>.json` in the hub

```json
{
  "skill": "processing-invoices",
  "runs": 3,
  "threshold": 0.5,
  "should_trigger": [
    "Total up the bills in this folder",
    "Pull the line items out of invoice-0423.pdf into a spreadsheet"
  ],
  "should_not_trigger": [
    "Write an invoice template for my clients",
    "Explain how PDF compression works"
  ],
  "quality": [
    {
      "prompt": "Extract the line items from fixtures/invoice.pdf",
      "expect": "items.csv has one row per line item and a total that matches the PDF"
    }
  ]
}
```
