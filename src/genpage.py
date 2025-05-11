from markdown import *
import os

def generate_page(markdown_path, template_path, dest_path):
    print(f"Generating page from:\n{markdown_path}\nto:\n{dest_path}\nusing:{template_path}")
    md, template = "", ""
    with open(markdown_path) as markdown_file:
        md = markdown_file.read()
    with open(template_path) as template_file:
        template = template_file.read()
    #print(md)
    #return
    title = extract_title(md)
    content = markdown_to_html_node(md).to_html()
    html = template.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", content)
    #print(html)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True) #Thanks ChatGPT
    with open(dest_path, 'w') as html_file:
        html_file.write(html)

def generate_pages_recursively(source_path,template_path,dest_path,basepath):
    for item in os.listdir(source_path):
        item_path = f"{source_path}{item}"
        if all([os.path.isfile(item_path), len(item)>=3, item[-3:] == ".md"]):
            md, template = "", ""
            with open(item_path) as markdown_file:
                md = markdown_file.read()
            with open(template_path) as template_file:
                template = template_file.read()
            #print(md)
            #return
            title = extract_title(md)
            content = markdown_to_html_node(md).to_html()
            html = template.replace("{{ Title }}", title)
            html = html.replace("{{ Content }}", content)
            html = html.replace('href="/',f'href="{basepath}')
            html = html.replace('src="/',f'src="{basepath}')
            next_dest = f"{dest_path}{item[:-3]}.html"
            os.makedirs(os.path.dirname(next_dest), exist_ok=True) #Thanks ChatGPT
            with open(next_dest, 'w') as html_file:
                html_file.write(html)
        elif not os.path.isfile(source_path):
            next_source = f"{source_path}{item}/"
            next_dest = f"{dest_path}{item}/"
            generate_pages_recursively(next_source,template_path,next_dest,basepath)
        
    
#markdown_path = "/home/arc/Statsitegen/content/index.md"
#template_path = "/home/arc/Statsitegen/template.html"
#dest_path = "/home/arc/Statsitegen/public/index.html"

#markdown_path = r"C:\Users\DNarc\OneDrive\Desktop\Statsitegen\content\index.md"
#template_path = r"C:\Users\DNarc\OneDrive\Desktop\Statsitegen\template.html"

#generate_page(markdown_path, template_path, dest_path)