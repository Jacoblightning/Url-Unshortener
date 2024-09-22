import requests
import argparse

def unshorten_url(url):
    response = requests.get(url)
    if response.status_code == 301:
        # Attempt to unshorten the redirected to URL
        return unshorten_url(response.redirect_destination)
    elif response.status_code == 200:
        if response.body.contains_meta_redirect:
            # Attempt to unshorten the redirected to URL
            return unshorten_url(response.body.meta_redirect_destintation)
        else:
            # No more redirects found so return the final URL
            return url
    else:
        pass

def main():
    pass