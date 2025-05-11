from enum import Enum
import re
from htmlnode import *
from textnode import *
from misc import *

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code"
    QUOTE = "blockquote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks] #gets rid of leading/trailing whitespace _and_ excessive newlines
    blocks = [block for block in blocks if block != ""]
    return blocks

def block_to_block_type(block):
    heading_pattern = re.compile(r"^#{1,6} .*", re.DOTALL)  #The initial ^ means the hashtags must start at the beginning of the
    #string, which prevents a.) leading text, including b.) more than 6 hashtags, since 6+n hashtags would
    #match from the (n+1)th hashtag.  Hashtags are allowed in the text following the mandatory space. The re.DOTALL allows newlines
    #in the text.  This function assumes that block is a string processed by markdown_to_blocks, which strips leading and trailing
    #newlines and spaces, which means I can and should revise these re patterns
    code_pattern = re.compile(r"^```.+```$", re.DOTALL) #DOTALL makes . match everything including newlines
    quote_pattern = re.compile(r"^(>.*\n?)+$") #The . will catch everything except a newline (and allows > after the initial >)
    #The \n catches the newline after each line of code, and the ? is there because the last line won't have a newline.
    unordered_pattern = re.compile(r"^(- .*\n?)+$")
    ordered_pattern = re.compile(r"^((\d+)\. .*\n?)+$")
    patterns = {heading_pattern:BlockType.HEADING,
                code_pattern: BlockType.CODE,
                quote_pattern: BlockType.QUOTE,
                unordered_pattern: BlockType.UNORDERED_LIST,
                ordered_pattern: BlockType.ORDERED_LIST}
    
    for pattern in patterns:
        if not re.fullmatch(pattern, block): continue
        if pattern == ordered_pattern:
            line_numbers = re.findall(r"^(\d+)\. .*\n?$", block, re.MULTILINE)
            expected = 1
            for number in line_numbers:
                if int(number) != expected: return BlockType.PARAGRAPH
                expected += 1
            return BlockType.ORDERED_LIST
        return patterns[pattern]
    return BlockType.PARAGRAPH

'''
Headings start with 1-6 # characters, followed by a space and then the heading text.

Code blocks must start with 3 backticks and end with 3 backticks.

Every line in a quote block must start with a > character.

Every line in an unordered list block must start with a - character, followed by a space.

Every line in an ordered list block must start with a number followed by a . character and

a space. The number must start at 1 and increment by 1 for each line.

If none of the above conditions are met, the block is a normal paragraph.
'''
def block_to_block_type_withstringmethods(block):
    def is_heading(block): #Note this allows an empty text section after the required space.
        i = 0
        while(i <= min(5, len(block)-2) and block[i] == "#"):
            if block[i+1] == " ": return True
            i += 1
        return False

    if is_heading(block):
        return BlockType.HEADING
    if len(block) >= 7 and block[:3] == block[-3:] == "```":
        return BlockType.CODE
    lines = block.split("\n")
    quote = True
    for line in lines:
        if line[0] != ">":
            quote = False
            break
    if quote == True: return BlockType.QUOTE
    unordered = True
    for line in lines:
        if len(line) > 1 and line[0:2] != "- ":
            unordered = False
            break
    if unordered == True: return BlockType.UNORDERED_LIST
    #ordered = True
    expected_digits = 1
    for line in lines:
        if ". " not in line: return BlockType.PARAGRAPH
        digits = line[: line.index(". ")]
        try:
            digits = int(digits)
        except:
            return BlockType.PARAGRAPH
        if digits != expected_digits: return BlockType.PARAGRAPH
        expected_digits += 1
    return BlockType.ORDERED_LIST
        
def markdown_to_html_node(md):
    blocks = markdown_to_blocks(md)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = ParentNode(block_type.value, None)
        if block_type == BlockType.PARAGRAPH:
            block = block.replace("\n", " ")
            textnodes = text_to_textnodes(block)
            block_node.children = [text_node_to_html_node(node) for node in textnodes]            
        if block_type == BlockType.QUOTE:
            start_index = 1 + int(block[1]==" ")
            block = block[start_index:]
            block = block.replace("\n> ", " ") #Try this first, then the next line.  If a quote line starts with "> ", then
            block = block.replace("\n>", " ")  #both characters are the delimiter and must be eliminated.
            textnodes = text_to_textnodes(block)
            block_node.children = [text_node_to_html_node(node) for node in textnodes]
        if block_type == BlockType.CODE:
            block_node.tag = "pre"
            text = block[3:-3]
            if text[0] == "\n": text = text[1:]
            block_node.children = [LeafNode("code",text)]
        if block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            lines = [line[2:] for line in lines]
            block_node.children = []
            for line in lines:
                textnodes = text_to_textnodes(line)
                line_nodes = [text_node_to_html_node(node) for node in textnodes]
                block_node.children += [ParentNode("li",line_nodes)]
        if block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            lines = [line[line.index(".")+2:] for line in lines] 
            block_node.children = []
            for line in lines:
                textnodes = text_to_textnodes(line)
                line_nodes = [text_node_to_html_node(node) for node in textnodes]
                block_node.children += [ParentNode("li",line_nodes)]
        if block_type == BlockType.HEADING:
            heading_level = 1
            while block[heading_level] == "#":
                heading_level += 1
            block_node.tag = f"h{int(heading_level)}"
            block = block.replace("\n", " ")
            block = block[heading_level+1:]
            textnodes = text_to_textnodes(block)
            block_node.children = [text_node_to_html_node(node) for node in textnodes]
            
        block_nodes.append(block_node)
    
    return ParentNode("div", block_nodes)
    
def extract_title(md):
    #print(markdown_to_blocks(md))
    #for block in markdown_to_blocks(md):
    #    print(
    html_node = markdown_to_html_node(md)
    #print(html_node)
    html = html_node.to_html()
    #print(html)
    h1_header = re.findall(r"<h1>(.*?)</h1>", html)
    if len(h1_header) == 0: raise Exception("There is no h1 header.")
    if len(h1_header) > 1: raise Exception("There is more than 1 h1 header.")
    
    return h1_header[0]
    