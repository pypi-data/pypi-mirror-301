from pypdf import PdfReader
import json


# Read files
def read_file(file_path):
    try:
        if file_path.endswith(".pdf"):
            reader = PdfReader(file_path)
            output_text = ""
            for page in reader.pages:
                output_text += page.extract_text()
            return output_text
        elif file_path.endswith(".json"):
            with open(file_path, "r") as file:
                return json.load(file)
        else:
            with open(file_path, "r") as file:
                return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"pdf file '{file_path}' not found.")

