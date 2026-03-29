#!/usr/bin/env python3
"""Minimal markdown blog generator."""

import os
import re
import shutil
from datetime import datetime

import mistune
import yaml
from jinja2 import Environment, FileSystemLoader


# --- Config ---

def load_config(path="config.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)


# --- Markdown parsing ---

def parse_front_matter(text):
    """Extract YAML front matter and body from markdown text."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", text, re.DOTALL)
    if match:
        meta = yaml.safe_load(match.group(1))
        body = match.group(2)
    else:
        meta = {}
        body = text
    return meta, body


def make_markdown_renderer():
    """Create a mistune markdown renderer."""
    return mistune.html


# --- File scanning ---

def scan_content(directory):
    """Scan a directory for .md files and return parsed content."""
    items = []
    if not os.path.isdir(directory):
        return items
    for filename in sorted(os.listdir(directory)):
        if not filename.endswith(".md"):
            continue
        filepath = os.path.join(directory, filename)
        with open(filepath) as f:
            text = f.read()
        meta, body = parse_front_matter(text)
        slug = meta.get("slug", filename.removesuffix(".md"))
        items.append({
            "meta": meta,
            "body": body,
            "slug": slug,
            "title": meta.get("title", slug.replace("-", " ").title()),
            "date": meta.get("date"),
        })
    return items


# --- Build ---

def build():
    config = load_config()
    md = make_markdown_renderer()

    # Clean and create output directory
    if os.path.exists("output"):
        shutil.rmtree("output")
    os.makedirs("output")

    # Read base CSS from template file and substitute config values
    template_css_path = os.path.join("templates", "style.css")
    with open(template_css_path) as f:
        base_css = f.read()

    style = config["style"]
    css = base_css.replace("FILL_IN_font_family", style["font_family"])
    css = css.replace("FILL_IN_font_size", style["font_size"])
    css = css.replace("FILL_IN_line_height", style["line_height"])
    css = css.replace("FILL_IN_max_width", style["max_width"])
    css = css.replace("FILL_IN_background", style["background"])
    css = css.replace("FILL_IN_text_color", style["text_color"])
    css = css.replace("FILL_IN_link_color", style["link_color"])

    # Write CSS
    with open(os.path.join("output", "style.css"), "w") as f:
        f.write(css)

    # Scan content
    posts = scan_content("posts")
    pages = scan_content("pages")

    # Convert markdown to HTML and compute reading stats
    for post in posts:
        post["html"] = md(post["body"])
        word_count = len(post["body"].split())
        post["word_count"] = word_count
        post["read_time"] = round(word_count / 150)
    for page in pages:
        page["html"] = md(page["body"])

    # Sort posts by date (newest first)
    posts.sort(key=lambda p: str(p.get("date", "")), reverse=True)

    # Set up Jinja2
    env = Environment(loader=FileSystemLoader("templates"))
    layout = env.get_template("layout.html")

    # Prepare page list for nav
    page_list = [{"slug": p["slug"], "title": p["title"]} for p in pages]

    # Render posts
    for post in posts:
        output = layout.render(
            config=config,
            title=post["title"],
            pages=page_list,
            content=f'<div class="post-meta">{post["date"]} — {post["word_count"]} words — {post["read_time"]} min read</div>\n{post["html"]}',
        )
        with open(os.path.join("output", f"{post['slug']}.html"), "w") as f:
            f.write(output)

    # Render pages
    for page in pages:
        output = layout.render(
            config=config,
            title=page["title"],
            pages=page_list,
            content=page["html"],
        )
        with open(os.path.join("output", f"{page['slug']}.html"), "w") as f:
            f.write(output)

    # Render index grouped by month/year
    post_list_html = ''
    current_key = None
    for post in posts:
        date = post.get("date")
        if date:
            dt = datetime.strptime(str(date), "%Y-%m-%d")
            key = dt.strftime("%B %Y")
        else:
            key = "Unknown"
        if key != current_key:
            if current_key is not None:
                post_list_html += '</ul>\n'
            post_list_html += f'<h2 class="month-heading">{key}</h2>\n<ul class="post-list">\n'
            current_key = key
        meta_str = f'<span class="post-meta-inline">{post["read_time"]} min read</span>' if post.get("read_time") else ""
        post_list_html += f'  <li><a href="{post["slug"]}.html">{post["title"]}</a>{meta_str}</li>\n'
    if current_key is not None:
        post_list_html += '</ul>\n'

    output = layout.render(
        config=config,
        title=None,
        pages=page_list,
        content=post_list_html,
    )
    with open(os.path.join("output", "index.html"), "w") as f:
        f.write(output)

    print(f"Built {len(posts)} post(s) and {len(pages)} page(s) → output/")


if __name__ == "__main__":
    build()
