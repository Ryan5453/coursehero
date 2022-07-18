from PIL.Image import Image
from common.ocr import mass_ocr
import io


def generate_pdf(document: dict, images: list[Image]):
    # json = mass_ocr(images)
    pdf = io.BytesIO()
    images[0].save(
        pdf,
        format="PDF",
        resolution=100.0,
        save_all=True,
        append_images=images[1:],
    )
    return pdf.getvalue()
