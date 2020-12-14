def read_from_file(file_name:str) -> str:
    with open(file_name, 'r') as file:
        return file.read()