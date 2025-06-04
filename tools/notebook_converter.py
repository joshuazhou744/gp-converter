from pydantic import BaseModel
from typing import Type
import os

import pdfplumber
from openai import OpenAI
from dotenv import load_dotenv
import base64

load_dotenv()

class NotebookConverterInput(BaseModel):
    input_notebook_path: str
    output_notebook_path: str
    system_config_prompt: str

class NotebookConverterTool():
    name: str = "convert_notebook"
    description: str = "Convert a Jupyter notebook to a different format."

    def run(self, argument: dict) -> str:
        try:
            input_notebook_path = argument.get("input_notebook_path")
            output_notebook_path = argument.get("output_notebook_path")
            system_config_prompt = argument.get("system_config_prompt")

            if not all([input_notebook_path, output_notebook_path, system_config_prompt]):
                return "Error: Missing required arguments (input_notebook_path, output_notebook_path, system_config_prompt)"

            os.makedirs(os.path.dirname(output_notebook_path), exist_ok=True)

            pdf_text = ""
            with pdfplumber.open(input_notebook_path) as pdf:
                for page in pdf.pages:
                    pdf_text += page.extract_text()

            client = OpenAI()

            prompt = f"""
Now, please convert this PDF to a notebook following the same format and structure as the example:

PDF to convert:
{pdf_text}
"""

            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_config_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=4096,
                    temperature=0.0
                )

                notebook_content = response.choices[0].message.content

                with open(output_notebook_path, "w") as f:
                    f.write(notebook_content)

                return f"Notebook converted from {input_notebook_path} to {output_notebook_path}"
            except Exception as api_error:
                print(f"API Error: {str(api_error)}")
                return f"Error making API request: {str(api_error)}"

        except Exception as e:
            print(f"General Error: {str(e)}")
            return f"Error converting notebook: {str(e)}"