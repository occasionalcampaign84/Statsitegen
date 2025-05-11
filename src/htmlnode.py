#from textnode import *

class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None: return ""
        #print(self.props)
        return " " + " ".join(f"{key}=\"{value}\"" for key,value in self.props.items())
    
    def __repr__(self):
        tag = "tag: None" if self.tag == None else self.tag
        value = "value: None" if self.value == None else self.value
        children = "children: None" if self.children == None else self.children
        props = "props: None" if self.props == None else self.props
        return f"HTMLNode({tag}, {value}, {children}, {props})"
        '''string = ""
        for key, value in self.__dict__.items(): #all its attributes
            if key == "children" and value != None:
                string += f"children: {len(self.children)}\n"
                #string += f"{key} = {value.__repr__(level+1)}\n"
            else:
                string += f"{key} = {value}\n"
        return string'''
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag,None,children,props)
        
    def to_html(self):
        if self.tag == None:
            raise ValueError("no tag")
        if self.children == None:
            raise ValueError("no children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
        