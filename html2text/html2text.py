import sys
import unicodedata

from urllib.request import urlopen
from bs4 import BeautifulSoup


strings_to_exclude = [
    "ISO Geodetic Registry (ISOGR) (read-only)",
    "Toggle navigation",
    "Geodetic Registry (read-only)",
    "Documentation",
    "User Guide",
    "Feedback",
    "Back",
    "Welcome",
    "ISO Geodetic Register",
    "Coordinate Reference",
    "Systems",
    "Compound CRS",
    "Engineering CRS",
    "Geodetic CRS",
    "Projected CRS",
    "Vertical CRS",
    "Coordinate Systems",
    "Cartesian Coordinate System",
    "Ellipsoidal Coordinate System",
    "Spherical Coordinate System",
    "Vertical Coordinate System",
    "Datums",
    "Engineering Datum",
    "Geodetic Datum",
    "Vertical Datum",
    "Coordinate",
    "Operations",
    "Concatenated Operation",
    "Conversion",
    "Transformation",
    "Other",
    "Coordinate System Axis",
    "Ellipsoid",
    "Coordinate Operation Method",
    "Coordinate Operation Parameter",
    "Prime Meridian",
    "Unit of Measurement",
    "Download PDF",
    "Item details",
    "Management information",
    "Show WKT",
    "Show GML",
    "Powered by",
    "Ok"
]


def extract_text_from_html(argv):

    if len(argv) == 1:
        raise Exception("A URL needs to be provided")
    url = argv[1]

    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    # remove script and style elements from the tree
    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()

    # break into lines removing leading and trailing spaces
    lines = (line.strip() for line in text.splitlines())
    # remove blank lines and unwanted strings
    chunks = [unicodedata.normalize("NFKD", chunk) for chunk in lines if chunk and (chunk not in strings_to_exclude)]
    
    print(chunks)


if __name__ == "__main__":
    extract_text_from_html(sys.argv)
