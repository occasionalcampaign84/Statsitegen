import shutil, os

def copy(source, dest):
	for item in os.listdir(source):
		source_path = f"{source}{item}"
		dest_path = f"{dest}{item}"
		if not os.path.isfile(source_path):
			#source_path += "/"
			if not os.path.exists(dest_path):
				os.mkdir(dest_path)
			copy(f"{source_path}/", f"{dest_path}/")
		else:
			shutil.copy(source_path, dest_path)


def display(path):
	for item in os.listdir(path):
		item_path = f"{path}{item}"
		if not os.path.isfile(item_path):
			display(f"{item_path}/")
		else:
			print(item_path)

def main():
	source = "/home/arc/Statsitegen/static/"
	destination = "/home/arc/Statsitegen/public/"
	#source = "/home/arc/worldbanc/private/"
	#destination = "/home/arc/worldbanc/private_copytest/"
	if os.path.exists(destination):
		shutil.rmtree(destination)
	os.mkdir(destination)
	copy(source,destination)


main()
