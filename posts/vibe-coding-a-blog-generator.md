---
title: "vibe coding a minimalist blog generator"
date: 2026-03-29
---

# vibe coding a minimalist blog generator

Vibe coding is definitely one of the most important concepts of the last year. LLMs have improved dramatically as code generators. I remain an AGI sceptic, however I also feel that this misses the point **entirely**.

Just like Google revolutionized the internet, these tools have revolutionized the programming discipline. There is no way that people will ever go back to programming one-keystroke-at-a-time. The short-term productivity gains are already too much to ignore. The verdict on whether this will be long-lasting is still out. It is possible that in a few years, we will have learned from the shortcomings of this technology and understand how to use it better.


## using agents as tutors

There has been some discourse on whether using agents stunts your growth. I think that if you use them as pure code-generating machines and just ship code at superhuman speed, this outcome is bound to happen. There is no way you can get better at writing code without writing code.

At the same time, a lot of the skill in programming comes from learning patterns. Students exiting university know that the job market expects different things from them. Nobody really cares if you can invert a binary tree and if I'm honest, I don't know if I can one-shot it correctly. However, very few companies pay people to perform this type of task. For the vast majority of people, daily programming life will revolve around industrialized programming patterns.

By this, I mean real-life software patterns, like HTTP servers and REST APIs. HTTP requests are not really a computer science topic (it's basically a protocol or a specification) and you can definitely write an HTTP server to host a blog without knowing the underlying concepts. Agents are a gift for whomever wants to learn software engineering patterns. Examples can include:
- how do event bus architectures work
- how does session authentication work
- how does an orchestrator like airflow work
- ...

Some will argue that open source can teach you all of this already. In addition, they would say that there is an abundance of articles, blogs, books, videos, literally anything you can imagine of, that already covers most of these. They are correct but each of these options might have a drawback. Opening the airflow codebase on github and trying to understand how it works is a tough task for most people.

Agents can provide a conversational workflow for this problem: you prompt them with your question and then ask them a question or even a minimal implementation that fulfills some basic requirements. Leave the laptop and after a few minutes, you have a very manageable version of what you want to learn about. Too complicated or large? Just ask for simplifications. This workflow can supplement the normal learning resources and speed up learning significantly.


## blog post generator (why I'm writing this post)

There exists an abundance of choice when it comes to static site generators. Hugo, Jekyll, Pelican, and probably easily more than 10 high quality options. The problem I have with them is that they are too complex. They provide a very feature-complete group of functions but all I actually want is to take a bunch of markdown files, style them so they do not appear as relics from 1998 and then output them with an index page.

When I tried to customize some small part of my Hugo blog, I had to work with weird modularized code, a number of folders I had no idea what they did, complex CSS code and in general, a whole lot of things I didn't ask for. In addition, the options were so many that I found myself spending more time browsing themes than writing posts.

I have wanted to try out [opencode](https://opencode.ai/) and the capabilities of open source llms so I installed it, selected `Mimo v2 pro free` as the model and prompted away. My prompt looked something like this
```bash
i want to create a markdown based blog generator in python, it should be
- minimal
- support syntax highlighting for code snippets
- have a copy button for the snippets
- be as simple and minimalist as possible
what are my options?
```
The agent replied with some options, ranging from simple to complex and after a bit of back-and-forth plus some testing, debugging, and refining the end result, it is available [here](https://github.com/jradhima/jradhima.github.io). In the process, I looked at the code written, understood how it works and now have an idea of how such a system is implemented. This is, of course, one of the simplest examples possible: it's basically a script that loads files and then, in a loop, transforms and writes them to an output location. Regardless, the principle still applies because 2 things happened in a very short timeframe:
- I read and understood a minimal implementation
- I now use it to solve a real need without unnecessary complexity

## some details on the generator

The final version of the code uses [mistune](https://mistune.lepture.com/en/latest/index.html) to render html and [highlight.js](https://highlightjs.org/) to highlight the code snippets. It just works and if I want to modify it, I can either prompt an agent to perform some small modifications or just implement them myself. The code itself is pretty short, at less than 150 lines of code for the main `blogipy/build.py` file (including empty lines and comments). There is also 50 lines of jinja template for the html part, and 170 lines of css for the styling. Unsurprisingly, css is the largest part of the codebase and one of the reasons why I didn't want to hand-write the code.

It is pretty amazing how the cost of custom-made software has decreased dramatically. It literally took 1.5 minutes to get a working version and another 10 minutes to finetune it to my preferences. The HTML page you are reading is the end result of a bunch of matrix multiplications of an open source model, hosted for free. This is mind-blowing.

## closing

Generating average-quality code has almost zero cost now. You can use this to ship code but you can also use this to augment your learning with on-the-fly tailored tutorials and an agent that is willing to explain all the details to you. It seems like a great opportunity in a field where so much of the knowledge is not scientific but practical and experience based. The options are limitless, you effectively have a free, on-demand tutor.
