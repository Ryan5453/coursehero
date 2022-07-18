import base64

from celery import current_task

from common.api import get_document_previews
from common.processing import overlay_unblurred
from common.scraper import get_pages
from common.pdf import generate_pdf
from worker.server import app


@app.task()
def get_pdf(document: dict):
    current_task.update_state(state="STARTED", meta={"current_task": "Grabbing metadata"})
    previews = get_document_previews(document["db_filename"])
    preview_json = previews.json()
    preview_id = preview_json.get("split_images")[0].split("/")[5]

    current_task.update_state(state="STARTED", meta={"current_task": "Grabbing images"})

    pages = get_pages(document, preview_id)

    current_task.update_state(state="STARTED", meta={"current_task": "Generating PDF"})

    pillow_pages = overlay_unblurred(document, pages)

    current_task.update_state(state="STARTED", meta={"current_task": "Running OCR"})

    pdf = generate_pdf(document, pillow_pages)

    return base64.b64encode(pdf).decode("utf-8"), document["title"]
