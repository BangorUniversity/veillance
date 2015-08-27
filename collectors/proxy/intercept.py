from bs4 import BeautifulSoup
import cStringIO
from PIL import Image
from libmproxy.script import concurrent
from libmproxy.protocol.http import decoded

@concurrent
def response(context, flow):
    if flow.response.headers.get_first("content-type", "").startswith("image"):
        with decoded(flow.response):  # automatically decode gzipped responses.
            try:
                s = cStringIO.StringIO(flow.response.content)
                img = Image.open(s).rotate(180)
                s2 = cStringIO.StringIO()
                img.save(s2, "png")
                flow.response.content = s2.getvalue()
                flow.response.headers["content-type"] = ["image/png"]
            except:  # Unknown image types etc.
                pass

    if flow.response.headers.get_first("content-type", "") == "text/html":
        with decoded(flow.response):  # automatically decode gzipped responses.
            print "HELLO"
            soup = BeautifulSoup(flow.response.content)
            print soup.get_text()

