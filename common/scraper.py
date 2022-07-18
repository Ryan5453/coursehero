from multiprocessing.dummy import Pool

from common.constants import ASSET_BASE, HTTP_CLIENT


def _metadata_injector(args: tuple):
    url, page, base = args
    return HTTP_CLIENT.get(url), page, base


def _reorganize_images(images: list[tuple]):
    images = [image for image in images if image[0].status_code == 200]
    pages = {}
    for image in images:
        img, page, base = image
        if page not in pages.keys():
            pages[page] = {"parts": []}
        if base:
            pages[page]["base"] = img
        else:
            pages[page]["parts"].append(img)

    for pageNum in pages:
        if "base" not in pages[pageNum]:
            pages[pageNum]["base"] = pages[pageNum]["parts"][0]

    return pages


def get_pages(document: dict, preview_id: str):
    _pagecount = document["document_pages"]["page_count"]
    pagecount = _pagecount if _pagecount <= 9 else 9
    hash = document["filehash"]

    args = []
    for pageNumber in range(pagecount):
        base_url = (
            f"{ASSET_BASE.format(hash=hash, split_id=preview_id)}/page-{pageNumber+1}.jpg"
        )
        args.append((base_url, pageNumber, True))
        for part in range(4):
            url = f"{ASSET_BASE.format(hash=hash, split_id=preview_id)}/split-{part}-page-{pageNumber+1}.jpg"
            args.append((url, pageNumber, False))

    pool = Pool(9)  # Each URL gets it's own thread - the max pages is 9
    responses = pool.map(_metadata_injector, args)
    pool.close()
    pool.join()

    return _reorganize_images(responses)
