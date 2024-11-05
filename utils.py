from pdf2image import convert_from_path
from PIL import Image
import os

def generate_pdf_thumbnail(pdf_path, thumbnail_path):
    """
    Generates a thumbnail image from the first page of a PDF file.
    
    Args:
        pdf_path (str): The path to the PDF file.
        thumbnail_path (str): The path to save the generated thumbnail image.

    Returns:
        str: The path to the generated thumbnail image.
    """
    try:
        # Convert the first page of the PDF to an image
        pages = convert_from_path(pdf_path, first_page=0, last_page=1)
        if pages:
            # Save the first page as an image thumbnail
            page = pages[0]
            page.thumbnail((300, 400))  # Adjust thumbnail size as needed
            page.save(thumbnail_path, 'JPEG')
            return thumbnail_path
        else:
            raise ValueError("No pages found in PDF")
    except Exception as e:
        print(f"Error generating thumbnail: {e}")
        return None
