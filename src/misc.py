import re
from textnode import *

def extract_markdown_images(text):
   return re.findall(r"!\[(.*?)\]\((.*?)\)", text) 

def extract_markdown_links(text):
   return re.findall(r"\[(.*?\)]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        x = old_node.text
        #images = re.findall(r"([^!]+)!\[(.*?)\]\((.*?)\)", x) #This fails to find images without a leading text.
        images = re.findall(r"([^!]*)!\[(.*?)\]\((.*?)\)", x)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            text,alt,url = image
            if text != "": new_nodes.append(TextNode(text,TextType.NORMAL))
            new_nodes.append(TextNode(alt,TextType.IMAGE,url))
        # trailing is any trailing text    
        trailing = re.sub(r"([^!]*)!\[(.*?)\]\((.*?)\)", "", x)
        if trailing != "":
            new_nodes.append(TextNode(trailing,TextType.NORMAL))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        #if old_node.text_type == TextType.IMAGE: #ignore images.  This depends on the fact that text_to_textnodes calls 
        #    new_nodes.append(old_node)           #split_nodes_image first.  I should fix split_nodes_link to filter out images. 
        #    continue
        #links = re.findall(r"([^\[]+)\[(.*?)\]\((.*?)\)",x) #This forbids links with no leading text
        x = old_node.text
        links = re.findall(r"([^\[]*)\[(.*?)\]\((.*?)\)",x)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            text,alt,url = link
            if text != "" and text[-1] == "!": #ignore images
                new_nodes.append(old_node)
                continue
            if text != "": new_nodes.append(TextNode(text,TextType.NORMAL))
            new_nodes.append(TextNode(alt,TextType.LINK,url))
        # trailing is any trailing text 
        trailing = re.sub(r"([^\[]*)\[(.*?)\]\((.*?)\)", "", x)
        if trailing != "":
            new_nodes.append(TextNode(trailing,TextType.NORMAL))
    return new_nodes


def text_to_textnodes(text):
    nodes = split_nodes_link(
            split_nodes_image([TextNode(text,TextType.NORMAL)]))  #If link were nested inside image instead of the reverse,
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)     #then link would identify images as links 
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)    #unless I updated it to ignore ![...]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)      #Maybe I should do that
    return nodes

#x = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
#print(text_to_textnodes(x))

'''def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks] #gets rid of leading/trailinng whitespace _and_ excessive newlines
    blocks = [block for block in blocks if block != ""]
    return blocks'''
    

#x = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)"
#print(re.findall(r"([^!]+)!\[(.*?)\]\((.*?)\)", x))

#x = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
#print(re.findall(r"([^\[]+)\[(.*?)\]\((.*?)\)",x))