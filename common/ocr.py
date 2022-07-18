import base64
import io
from multiprocessing.dummy import Pool

from PIL.Image import Image

from common.constants import HTTP_CLIENT, GOOGLE_VISION_KEY


def mass_ocr(documents: list[Image]):
    pool = Pool(9)  # Each page gets it's own thread - the max pages is 9
    responses = pool.map(gv_ocr, documents)
    pool.close()
    pool.join()

    return [r.json() if r.status_code == 200 else None for r in responses]


def gv_ocr(image: Image):
    img_file = io.BytesIO()
    image.save(img_file, format="JPEG")
    params = {
        "prettyPrint": False,
        "key": GOOGLE_VISION_KEY,
    }
    data = {
        "requests": [
            {
                "image": {
                    "content": base64.b64encode(img_file.getvalue()).decode("utf-8")
                },
                "features": [
                    {
                        "type": "DOCUMENT_TEXT_DETECTION",
                    }
                ],
            }
        ]
    }
    return HTTP_CLIENT.post(
        "https://vision.googleapis.com/v1/images:annotate",
        params=params,
        json=data,
    )
