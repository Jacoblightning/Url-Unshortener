# import argparse
from urllib.parse import urlparse

import regex as re
import requests

DEBUG = False


def unshorten_url(url):
    if DEBUG:
        print(f"Starting with {url=}")
    try:
        response = requests.get(url)
    except requests.exceptions.TooManyRedirects:
        print(f"WARNING: Url Probably redirects to itself")
        return url
    pattern = re.compile(r"\<meta.*?\>", re.DOTALL | re.UNICODE | re.VERSION1)
    innerpattern1 = re.compile(r"\<meta.*?http-equiv=(\"|')refresh\1.*?\>")

    # Don't try this regex in other engines. It's nonstandard and will cause errors.
    # Not supported by "re" this is why we need "regex"
    innerpattern2 = re.compile(
        r"\<meta.*?content=(\"|').*?url=(.*?)(?<!\\(?:\\\\)*)\1.*?\>"
    )  # Magic regex
    for match in pattern.finditer(response.text):
        isin = innerpattern1.search(match.group(0))
        if isin:
            content = innerpattern2.search(match.group(0))
            if content:
                newurl = content.group(2)
                parsednew = urlparse(newurl)
                if newurl.startswith("/"):

                    if DEBUG:
                        print("DEBUG: Trying to calculate url using method 1.")

                    oldurl = urlparse(response.url)
                    newurl = oldurl._replace(path=newurl).geturl()

                    if DEBUG:
                        print(f"DEBUG: Recursing to {newurl}")

                    if newurl != response.url and newurl != url:
                        return unshorten_url(newurl)
                    print("WARNING: Url redirects to self.")
                    return response.url
                elif parsednew.scheme:

                    if DEBUG:
                        print("DEBUG: Url is already a full url.")
                        print(f"DEBUG: Recursing to {newurl}")

                    if newurl != response.url and newurl != url:
                        return unshorten_url(newurl)
                    print("WARNING: Url redirects to self.")
                    return response.url
                else:

                    if DEBUG:
                        print("DEBUG: Trying to calculate url using method 2.")

                    oldurl = urlparse(response.url)
                    oldpath = oldurl.path
                    start_path = oldpath[: oldpath.rfind("/") + 1]
                    start_path += newurl
                    if "." in oldpath[oldpath.rfind("/") + 1 :]:
                        start_path += "." + start_path.split(".")[-1]

                    if DEBUG:
                        print(f"DEBUG: Recursing to {start_path}")

                    newurl = start_path

                    if newurl != response.url and newurl != url:
                        return unshorten_url(newurl)
                    print("WARNING: Url redirects to self.")
                    return response.url
    # TODO: Javascript check

    # Well we didn't return from inside the loop so there is no meta redirect tag.
    return response.url


def main():
    print("CLI Coming soon.")
    print(
        f"You can call unshorten_url from this shell.\nYou can set debug mode with dbg(<True or False>)"
    )

    def dbg(debug):
        global DEBUG
        DEBUG = debug
        if DEBUG:
            print("DEBUG: Debug mode is on.")
        else:
            print("DEBUG: Debug mode is off.")

    while True:
        comm = input("> ")
        if not comm.strip():
            continue
        try:
            comp = compile(comm, "<string>", "eval")
            res = eval(comp, globals(), {"dbg": dbg})
            if res:
                print(res)
        except Exception as e:
            print(f"Error executing {comm}:\n{e}")


if __name__ == "__main__":
    main()
