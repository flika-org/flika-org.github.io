---
layout: default
title: Tutorial Creation
category: Developer
---
# Tutorial Creation

## Use an IPython Notebook
The simplest way to create a tutorial to go on our site is to use amarkdown file from an IPython Notebook.  A pure HTML tutorial is also an option, but would cause many headaches.

### Step 1. YAML data
To clarify what type of tutorial you are writing, specify information about your tutorial at the top of your markdown file

	---
	title: Your Tutorial Title Here
	category: category name (or [list, of, names])
	permalink: /path/to/html (optional)
	---

The title specified will show up at the top of your tutorial, category will define under what subset(s) your category shows up, and permalink isn't used yet

### Step 2. File Naming Convention
Because Jekyll uses very specific naming conventions to categorize markdown files, it is necessary to save the file as a complex name. However, the naming convention also provides date and title information. So I don't mind it much.  Your markdown file needs to be named in the follwing format

	YEAR-MONTH-DAY-Title-Here.md

Where the YEAR is given as a 4 digit number, MONTH and DAY as 2 digit numbers, and all dashes in title are replaced by spaces. This title is not visible to the user and will not show up on the site. It is specifically for file naming.

## Step 3. Put it in the _posts folder.
Really! It's that simple. Put your markdown file in the _posts folder and we'll sort it away for you.