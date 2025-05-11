import shutil, os, sys
from genpage import generate_page, generate_pages_recursively

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


template_path = "/home/arc/Statsitegen/template.html"
def main():
	basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
	#print("basepath = ", basepath)
	static_source = "/home/arc/Statsitegen/static/"
	markdown_source = "/home/arc/Statsitegen/content/"
	destination = "/home/arc/Statsitegen/docs/"
	#destination = "/home/arc/Statsitegen/public/"
	#source = "/home/arc/worldbanc/private/"
	#destination = "/home/arc/worldbanc/private_copytest/"
	if os.path.exists(destination):
		shutil.rmtree(destination)
	copy(static_source,destination)
	generate_pages_recursively(markdown_source,template_path,destination,basepath)
main()
