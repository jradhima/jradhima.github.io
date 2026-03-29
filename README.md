# blogipy

A minimal markdown blog generator. Write posts in Markdown, get a static site with syntax highlighting and copy buttons.

## Installation

```bash
pip install .
```

Or using uv:

```bash
uv pip install .
```

## Creating a new post

```bash
blogipy new "My Post Title"
```

This creates a new markdown file in `posts/` with front matter and a basic template.

## Building the site

```bash
blogipy build
```

Open `output/index.html` in your browser.

## Project Structure

```
├── blogipy/           # Python package
│   ├── cli.py         # Command line interface
│   ├── new.py         # Post generator
│   └── build.py       # Site builder
├── config.yaml        # Site title, fonts, colors
├── templates/         # HTML template
├── posts/             # Blog posts (.md files with front matter)
├── pages/             # Static pages (About, etc.)
└── output/            # Generated site
```

## Adding Pages

Create a `.md` file in `pages/`:

```markdown
---
title: About
---

# About

This page is linked in the nav bar.
```

## Configuration

Edit `config.yaml`:

```yaml
site:
  title: "My Blog"
  description: "A simple blog"

style:
  font_family: "system-ui, -apple-system, sans-serif"
  font_size: "18px"
  line_height: "1.7"
  max_width: "720px"
  background: "#ffffff"
  text_color: "#333333"
  link_color: "#0066cc"
```

Code highlighting is handled by highlight.js with the "atom-one-light" theme.