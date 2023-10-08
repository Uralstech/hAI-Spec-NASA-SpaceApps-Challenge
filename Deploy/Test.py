from requests import post
from os.path import join, abspath, dirname

PDF_PATH: str = join(dirname(dirname(abspath(__file__))), "Utility/.DocsCache/nasa-std-5009a.pdf")
IP: str = "IP ADDRESS"
PORT: int = 8080

with open(PDF_PATH, "rb") as file:
    request = post(f"http://{IP}:{PORT}/api/instruct", files={"file" : file}, timeout=600)
    print(request.content)