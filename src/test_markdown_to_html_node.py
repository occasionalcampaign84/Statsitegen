from markdown import *


md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        
'''<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>
This is another paragraph with <i>italic</i> text and <code>code</code>
here</p></div>'''

md2 = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
"<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"


md_mine = """
## Headings require a bit of special processing.

> This is a **block quote** with
>extra inline
>stuff in
>it.

- An _unordered_ list
- requires _tags_ on each line.

1. So does an **ordered** list.
2. ...that's it.


"""
'''
print(markdown_to_html_node(md).to_html())
print()
print(markdown_to_html_node(md2).to_html())
print()
print(markdown_to_html_node(md_mine).to_html())
'''