# Contributing

This repository holds one person's résumé, so most contributions belong somewhere else. Here is where each kind of help lands best.

## Want to work on open source with me?

Head to **[vibey](https://github.com/the-vibey-project/vibey)**. Its [contributing guide](https://github.com/the-vibey-project/vibey/blob/develop/CONTRIBUTING.md) walks through setup, the branch model and the quality gates command by command. Good first contributions are a new engine adapter, a skill plugin, or an issue describing what surprised you when you ran it on a real repository. If you'd like to help in a broader way, see [vibewithadam.matthewsteinberger.com/join-me](https://vibewithadam.matthewsteinberger.com/join-me).

## Found a problem with this résumé?

Please [open an issue](https://github.com/adammatthewsteinberger/resume/issues) for a broken link, a figure that has gone stale, or a formatting problem in one of the generated files. Every claim here should be traceable to a public repository, a package index, or a document I can produce; if you can't trace one, that's worth an issue too.

## Want to reuse the builder?

`tools/build_resume.py` is MIT-licensed. Fork the repository, replace the data at the top of the file with your own, and run:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python tools/build_resume.py            # add --no-pdf if Chrome isn't installed
```

It writes the README, plain-text, Word and PDF résumés (one set per framing in `VARIANTS`), `resume.json` in the [JSON Resume](https://jsonresume.org/schema) format, `llms.txt` and `CITATION.cff`. The PDF step drives headless Google Chrome; set `CHROME=/path/to/chrome` if it lives somewhere unusual.

Two conventions keep the outputs honest:

- **Facts live once.** Each experience bullet is written in `EXPERIENCE` and referenced by key. A variant chooses the title, summary, order and which bullets appear. It never rewrites a fact.
- **Generated files are never edited by hand.** Change the data, rebuild, and commit the builder and its outputs together.

The résumé text itself is CC BY 4.0 (see [LICENSE-CONTENT.md](LICENSE-CONTENT.md)). Please don't present my work history as your own.
