import regex
from httpx import Client

API_BASE_URL = "https://coursehero.com/api"
API_CLIENT_ID = "4_5k0wmakgj1gk44k0gcgw8w0sw80c8gos08w88o004440wwssoc"
API_CLIENT_SECRET = "ufvtfcnwz2804wg848sk8scws440sss008wcck88ko8c0sc0w"
API_HEADERS = {
    "Host": "www.coursehero.com",
    "User-Agent": "Course Hero/1.9.128 (com.coursehero.Course-Hero; build:3; iOS 15.3.1) Alamofire/1.9.128",
    "Accept-Language": "en-US;q=1.0, es-MX;q=0.9",
    "Connection": "keep-alive",
}
API_BASE_PARAMS = {
    "client_id": API_CLIENT_ID,
    "client_secret": API_CLIENT_SECRET,
}
HTML_REGEX = regex.compile("<.*?>")
HTTP_CLIENT = Client(follow_redirects=True)
ASSET_BASE = "https://www.coursehero.com/doc-asset/bg/{hash}/splits/{split_id}"
GOOGLE_VISION_KEY = ""
