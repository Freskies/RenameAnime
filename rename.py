import glob
import pathlib
import os


class Rename:

	@staticmethod
	def __legal_line(line: str) -> bool:
		"""
		Check if the line is legal
		the line is legal when every char is in legal_char.txt
		:rtype: object
		:param line: the line to check
		:return: true if the line is legal
		"""
		if len(line) < 1:
			return False

		with open("legal_char.txt", 'r', encoding='utf-8') as f:
			legal_char = f.read()

		for c in line:
			if not c.lower() in legal_char:
				return False
		return True

	@staticmethod
	def __get_lines(path: str) -> list:
		"""
		Get lines from file
		it deletes the last character in every line ('\n')
		:param path: the absolute path of the file
		:return: list of lines
		"""
		with open(f"{path}/name.txt", 'r', encoding='utf-8') as f:
			lines = f.readlines()

		return [line[:-1] for line in lines]

	@staticmethod
	def exist_file(path: str) -> bool:
		"""
		Check if the file exist
		:rtype: object
		:param path: absolute path of the file
		:return: true if the file exist
		"""
		try:
			Rename.__get_lines(path)
			return True
		except FileNotFoundError:
			return False
		except EnvironmentError:
			return False

	@staticmethod
	def check_lines(path: str) -> bool:
		"""
		Check if the number of line in name.txt is equal to the number of files in the folder
		:rtype: bool
		:param path: absolute path of the file
		:return: true if are the same
		"""
		lines = Rename.__get_lines(path)

		files = glob.glob(f"{path}/*.*")
		return True if len(files) - 1 == len(lines) else False

	@staticmethod
	def check_char(path: str) -> list[str]:
		"""
		Check if every char in name.txt are legal
		:param path: absolute path of the file
		:return: a list of illegal lines
		"""
		lines = Rename.__get_lines(path)

		error = list()

		for line in lines:
			if not Rename.__legal_line(line):
				error.append(line)

		return error

	@staticmethod
	def rename(path: str) -> None:
		"""
		Rename the files in the folder
		it takes the name from name.txt
		:param path: absolute path of the folder
		"""
		lines = Rename.__get_lines(path)
		redo = False

		files = glob.glob(f"{path}/*.*")
		files.remove(f"{path}\\name.txt")

		for i, file in enumerate(files):
			new_name = f"{str(i + 1).zfill(len(str(len(files))))} - {lines[i].strip()}"
			print(f"{file} -> {path}\\{new_name}{pathlib.Path(file).suffix}")

			if os.path.isfile(file):
				try:
					os.rename(file, f"{path}\\{new_name}{pathlib.Path(file).suffix}")
				except FileExistsError:
					os.rename(file, f"{path}\\{new_name}(ReNaMe){pathlib.Path(file).suffix}")
					redo = True

			else:
				print("Wtf error is occurred")
				break

		if redo:
			print("Redo")
			Rename.rename(path)

	@staticmethod
	def check_file_name_is_not_number_in_list(path: str, start_number: int) -> list[str]:
		"""
		Check if the file name is number,
		if it is, check if the number is in the list,
		if it is, add the number to the list
		:param start_number: the number to start rename
		:param path: absolute path of the file
		:return: a list of illegal lines
		"""
		files = glob.glob(f"{path}/*.*")
		final_number = start_number + len(files)

		error = list()

		for file in files:
			try:
				if int(file.split('\\')[-1].split('.')[0]) in range(start_number, final_number):
					error.append(file.split('\\')[-1])
			except ValueError:
				pass

		return error

	@staticmethod
	def rename_from_number(path: str, from_: int) -> None:
		"""
		Rename the files in the folder
		names start from from_
		:param path: absolute path of the folder
		:param from_: the number of the first file to rename
		"""
		files = glob.glob(f"{path}/*.*")

		for i, file in enumerate(files):
			new_name = f"{str(i + from_).zfill(len(str(len(files))))}"
			print(f"{file} -> {path}\\{new_name}{pathlib.Path(file).suffix}")

			if os.path.isfile(file):
				os.rename(file, f"{path}\\{new_name}{pathlib.Path(file).suffix}")

			else:
				print("Wtf error is occurred")
				break
