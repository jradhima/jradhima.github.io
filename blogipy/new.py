"""Create new blog posts."""

import os
import re
from datetime import date


def slugify(title):
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower().replace("'", "")).strip("-")
    return slug or "post"


def new_post(title):
    slug = slugify(title)
    today = date.today().isoformat()
    os.makedirs("posts", exist_ok=True)
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
