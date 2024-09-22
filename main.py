import requests
import argparse
import regex as re
from urllib.parse import urlparse

DEBUG = True

def unshorten_url(url):
    if DEBUG:
        print(f"Starting with {url=}")
    response = requests.get(url)
    pattern = re.compile(r"\<meta.*?\>", re.DOTALL|re.UNICODE|re.VERSION1)
    innerpattern1 = re.compile(r"\<meta.*?http-equiv=(\"|')refresh\1.*?\>")

    # Don't try this regex in other engines. It's nonstandard and will cause errors.
    # Not supported by "re" this is why we need "regex"
    innerpattern2 = re.compile(r"\<meta.*?content=(\"|').*?url=(.*?)(?<!\\(?:\\\\)*)\1.*?\>") # Magic regex
    for match in pattern.finditer(response.text):
        isin = innerpattern1.search(match.group(0))
        if isin:
            content = innerpattern2.search(match.group(0))
            if content:
                newurl = content.group(2)
                parsednew = urlparse(newurl)
                if newurl.startswith('/'):

                    if DEBUG:
                        print("DEBUG: Trying to calculate url using method 1.")

                    oldurl = urlparse(response.url)
                    newurl = oldurl._replace(path=newurl).geturl()

                    if DEBUG:
                        print(f"DEBUG: Recursing to {newurl}")

                    return unshorten_url(newurl)
                elif parsednew.scheme:

                    if DEBUG:
                        print("DEBUG: Url is already a full url.")
                        print(f"DEBUG: Recursing to {newurl}")

                    return unshorten_url(newurl)
                else:

                    if DEBUG:
                        print("DEBUG: Trying to calculate url using method 2.")

                    oldurl = urlparse(response.url)
                    oldpath = oldurl.path
                    start_path = oldpath[:oldpath.rfind('/')+1]
                    start_path += newurl
                    if "." in oldpath[oldpath.rfind('/')+1:]:
                        start_path += "."+start_path.split(".")[-1]

                    if DEBUG:
                        print(f"DEBUG: Recursing to {start_path}")

                    return unshorten_url(start_path)
    # TODO: Javascript check

    # Well we didn't return from inside the loop so there is no meta redirect tag.
    return response.url





def main():
    pass

if __name__ == '__main__':
    main()

# Temp
print(f"Shortened url is: \"{unshorten_url("http://127.0.0.1:5000/meta")}\"")