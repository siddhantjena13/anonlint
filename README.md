# anonlint

Catches identity leaks in your paper before you submit it to a double-blind venue.

> **Status: pre-alpha.** Under active development. Not yet usable.

## The problem

Double-blind review only works if the paper is actually anonymous. Authors remember to
remove their names from the title page. They forget the rest:

- The `/Author` field your PDF exporter silently filled in with your account name
- "In our previous work [7]" — a self-citation phrased as a signature
- An image path like `/Users/jsmith/uw-thesis/figure3.png` baked into the LaTeX
- A linked code repo whose commit history carries your name and institutional email
- Acknowledgements and grant numbers that are publicly searchable back to you

None of these are hard to fix. They're just easy to miss — and a reviewer who notices
can desk reject the paper before anyone reads the science. At a venue that runs once a
year, that mistake costs a year.

## What it does

Point it at your paper. It reports every likely leak, exactly where it is, and how to
fix it.

```
$ anonlint paper.pdf --venue iclr-2027

ERROR   metadata.pdf_author      /Author field contains "Jane Smith"
                                 fix: exiftool -Author= paper.pdf
WARNING cite.self_reference      p.4, ch.210 — "in our previous work [7]"
                                 fix: rephrase as third-person citation
```

Findings carry a confidence score, and severity is decided per venue — the same finding
can be a hard error at one conference and a note at another.

anonlint reports and advises. It never edits your paper.

## Privacy

Your unsubmitted paper is not uploaded anywhere. Ever.

The checking core performs no file or network access of its own, which lets it compile to
WebAssembly and run entirely inside your browser tab. Open devtools and confirm: zero
network requests. The CLI is local by construction.

This is a hard requirement, not a feature. A tool that asks researchers to upload
unpublished work has already failed.

## Non-goals

- Not a grammar, style, or formatting checker. Anonymity only.
- Not a guarantee. It reduces careless mistakes; it cannot certify anonymity, and it
  won't pretend to.
- Not a de-anonymization tool. No authorship inference from writing style.

## Install

Not published yet. From source:

```bash
git clone https://github.com/YOURNAME/anonlint
cd anonlint
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

## License

MIT
