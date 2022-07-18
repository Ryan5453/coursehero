import io

import cv2
import numpy
from PIL import Image
from skimage.io._plugins.pil_plugin import ndarray_to_pil
from skimage.metrics import structural_similarity


def overlay_unblurred(document: dict, pages: dict):
    pillow_pages = []
    _pagecount = document["document_pages"]["page_count"]
    pagecount = _pagecount if _pagecount <= 9 else 9
    for pageNumber in range(pagecount):
        page = pages[pageNumber]
        base_arr = cv2.cvtColor(
            cv2.imdecode(
                numpy.asarray(bytearray(page["base"].content), dtype=numpy.uint8),
                -1,
            ),
            cv2.COLOR_BGR2GRAY,
        )
        base = Image.open(io.BytesIO(page["base"].content)).convert("RGB")
        for part_ in page["parts"]:
            part = cv2.cvtColor(
                cv2.imdecode(
                    numpy.asarray(bytearray(part_.content), dtype=numpy.uint8), -1
                ),
                cv2.COLOR_BGR2GRAY,
            )
            (_, diff) = structural_similarity(base_arr, part, full=True)
            diff = (diff * 255).astype("uint8")

            thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[
                1
            ]
            contours = cv2.findContours(
                thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            contours = contours[0] if len(contours) == 2 else contours[1]

            mask = numpy.zeros(base_arr.shape, dtype="uint8")
            for c in contours:
                if cv2.contourArea(c) > 40:
                    cv2.drawContours(mask, [c], 0, (255, 255, 255), -1)

            base.paste(
                Image.open(io.BytesIO(part_.content)).convert("RGBA"),
                mask=ndarray_to_pil(mask).convert("L"),
            )
        pillow_pages.append(base)
    return pillow_pages
