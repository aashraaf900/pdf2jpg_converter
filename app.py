import gradio as gr
import fitz  # PyMuPDF
import zipfile, io

def pdf_to_images(pdf_file):
    if pdf_file is None:
        return None

    pdf_bytes = pdf_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for page_num in range(len(doc)):
            page = doc[page_num]
            pix = page.get_pixmap(dpi=300)

            img_bytes = pix.tobytes("jpeg")
            zipf.writestr(f"page_{page_num+1}.jpg", img_bytes)

    zip_buffer.seek(0)
    return zip_buffer

app = gr.Interface(
    fn=pdf_to_images,
    inputs=gr.File(label="Upload PDF", file_types=[".pdf"]),
    outputs=gr.File(label="Download ZIP of Images"),
    title="PDF → JPG Converter",
    description="Upload a PDF and download all pages as high-resolution JPG images in a ZIP file."
)

app.launch()
