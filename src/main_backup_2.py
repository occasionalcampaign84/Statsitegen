import shutil, os
from genpage import generate_page

def copy(source, dest):
	os.mkdir(dest)
	for item in os.listdir(source):
		source_path = f"{source}{item}"
		dest_path = f"{dest}{item}"
		if os.path.isfile(source_path):
			shutil.copy(source_path, dest_path)
		else:
			copy(f"{source_path}/", f"{dest_path}/")


def display(path):
	for item in os.listdir(path):
		item_path = f"{path}{item}"
		if not os.path.isfile(item_path):
			display(f"{item_path}/")
		else:
			print(item_path)

#markdown_path = "/home/arc/Statsitegen/content/index.md"
markdown_paths = [
"/home/arc/Statsitegen/content/index.md",
"/home/arc/Statsitegen/content/blog/glorfindel/index.md",
"/home/arc/Statsitegen/content/blog/tom/index.md",
"/home/arc/Statsitegen/content/blog/majesty/index.md",
"/home/arc/Statsitegen/content/contact/index.md",
]
template_path = "/home/arc/Statsitegen/template.html"
#dest_path = "/home/arc/Statsitegen/public/index.html"
def main():
	source = "/home/arc/Statsitegen/static/"
	destination = "/home/arc/Statsitegen/public/"
	#source = "/home/arc/worldbanc/private/"
	#destination = "/home/arc/worldbanc/private_copytest/"
	if os.path.exists(destination):
		shutil.rmtree(destination)
	copy(source,destination)
	for mdpath in markdown_paths:
		dest_path = mdpath.replace("/content/","/public/")
		dest_path = dest_path.replace(".md", ".html")
		generate_page(mdpath, template_path, dest_path)

main()
