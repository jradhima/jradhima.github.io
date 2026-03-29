"""Create new blog posts."""

import os
from datetime import date


def slugify(title):
    return title.lower().replace(" ", "-")


def new_post(title):
    slug = slugify(title)
    today = date.today().isoformat()
    filepath = os.path.join("posts", f"{slug}.md")

    if os.path.exists(filepath):
        print(f"Post already exists: {filepath}")
        return

    content = f"""---
title: "{title}"
date: {today}
---

# {title}

some intro text here

## key idea

main content goes here

## closing

final thoughts here
"""

    with open(filepath, "w") as f:
        f.write(content)

    print(f"Created {filepath}")
