import os
from tools import *

def convert_tutorial_to_notebook(url: str, notebook_name: str) -> str:
    outputs_dir = os.path.join(os.path.dirname(__file__), "outputs")
    os.makedirs(outputs_dir, exist_ok=True)
    
    pdf_path = os.path.join(outputs_dir, "temp_tutorial.pdf")
    notebook_path = os.path.join(outputs_dir, f"{notebook_name}.ipynb")
    
    print(f"\nFiles will be saved at:")
    print(f"PDF: {pdf_path}")
    print(f"Notebook: {notebook_path}\n")

    tutorial_getter = TutorialGetterTool()
    notebook_converter = NotebookConverterTool()

    print("Downloading tutorial PDF...")
    download_result = tutorial_getter.run({
        "url": url,
        "output_pdf_path": pdf_path
    })

    print("\nConverting PDF to notebook...")
    system_prompt = """You are a helpful assistant that converts the PDF content to a Python notebook format with all the code blocks, text formatting and explanations exactly the same as the given notebook. 
    Ensure the content remains the EXACT same in order and format. Make the output only a `.ipynb` file, NOTHING ELSE, DON'T EVEN INCLUDE THE ```json```. Start writing the `.ipynb` file here:"""
    
    convert_result = notebook_converter.run({
        "input_notebook_path": pdf_path,
        "output_notebook_path": notebook_path,
        "system_config_prompt": system_prompt
    })

    os.remove(pdf_path)

    return notebook_path

if __name__ == "__main__":
    url = input("Enter the URL of the tutorial to convert: ")
    notebook_name = input("Enter the name for the converted notebook (without extension): ")
    
    notebook_path = convert_tutorial_to_notebook(url, notebook_name)
    print(f"\nConversion complete! Notebook saved at: {notebook_path}")


