# MkDocs Documentation

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Installations

```bash
pip install mkdocs
pip install mkdocs-awesome-nav
```

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs serve &` - Start server in background process.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

    To stop the background server, use `pkill -f mkdocs` on Unix-based systems.

## Project layout

```bash
    mkdocs.yml          # The configuration file.
    docs/
        index.md        # RahmSD documentation homepage.
        notes/          # RahmSD development notes.
        evaluations/    # RahmSD software evaluation notes.
        mkdocs/         # MkDocs documentation.
        ...             # Other markdown pages, images and other files.
```
