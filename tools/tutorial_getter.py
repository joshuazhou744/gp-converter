from playwright.sync_api import sync_playwright
from pydantic import BaseModel
from typing import Type
import time

class DownloadTutorialPDFInput(BaseModel):
    url: str
    output_pdf_path: str

class TutorialGetterTool():
    name: str = "download_tutorial_pdf"
    description: str = "Download a tutorial PDF from a given URL."

    def run(self, argument: dict) -> str:
        try:
            url = argument.get("url")
            output_pdf_path = argument.get("output_pdf_path")

            if not all([url, output_pdf_path]):
                return "Error: Missing required arguments (url, output_pdf_path)"

            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(url, wait_until="load", timeout=60000)
                time.sleep(0.5)
                page.pdf(path=output_pdf_path, format="A4")
                browser.close()
            return f"PDF downloaded successfully to {output_pdf_path}"
        except Exception as e:
            return f"Error downloading PDF: {str(e)}"