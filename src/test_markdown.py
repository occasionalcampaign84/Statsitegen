from markdown import *
import unittest

class MyMarkdownTests(unittest.TestCase):
    def test_my_tests_1(self):

        blocks = ["#### Heading",
          """``` Code
more code
done. ```""",
          """>why
>do
>quotes""",
          """- unordered
- list""",
          """1. Ordered
2. list
3. with four
4. lines.""",
"sdklfjiwe"]

        answers = [BlockType.HEADING,
                    BlockType.CODE,
                    BlockType.QUOTE,
                    BlockType.UNORDERED_LIST,
                    BlockType.ORDERED_LIST,
                    BlockType.PARAGRAPH]

        for (block,expected) in zip(blocks, answers):
            actual = block_to_block_type(block)
            self.assertTrue(
                actual == expected, f"Expected:\n {repr(expected)}\n Actual:\n {repr(actual)}"
            )
            
    def test_my_tests_2(self):

        blocks = ["```#### Heading",
"``` Code single line ```",
"####### invalid heading",
"""1. incorrectly
 2. ordered
3. list.
"""]

        answers = [BlockType.PARAGRAPH,
                    BlockType.CODE,
                    BlockType.PARAGRAPH,
                    BlockType.PARAGRAPH]

        for (block,expected) in zip(blocks, answers):
            actual = block_to_block_type(block)
            self.assertTrue(
                actual == expected, f"Expected:\n {repr(expected)}\n Actual:\n {repr(actual)}"
            )
            
    def test_block_to_block_types(self):
        blocks = ["# heading", "```\ncode\n```", "> quote\n> more quote", "- list\n- items",
                  "1. list\n2. items", "paragraph"]
        expecteds = [BlockType.HEADING, BlockType.CODE, BlockType.QUOTE, BlockType.UNORDERED_LIST,
                     BlockType.ORDERED_LIST, BlockType.PARAGRAPH]
        for (block, expected) in zip(blocks, expecteds):
            self.assertEqual(block_to_block_type(block), expected)
            self.assertEqual(block_to_block_type_withstringmethods(block), expected)        

class TestMarkdownToBlocks(unittest.TestCase):        
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        expected = [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ]
        blocks = markdown_to_blocks(md)
        self.assertTrue(
            blocks == expected, f"Expected:\n {repr(expected)}\n Actual:\n {repr(blocks)}"
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        expected = [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ]
        blocks = markdown_to_blocks(md)
        self.assertTrue(expected == blocks, f"Expected:\n {repr(expected)}\n Actual:\n {repr(blocks)}")

class TestMarkdownToHtml(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

class TestExtractTitle(unittest.TestCase):
    def testmy1(self):
        x = ["""
        # Header 1
        """,
             """ alkslskdfj
``` alksdf j
laskdf
```

# Header
with two lines

## Header 2"""
             ]
        for item in x:
            print(extract_title(item))
        #print(block_to_block_type('## Header\nwith two lines'))

if __name__ == "__main__":
    unittest.main()

