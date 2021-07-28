import re
import urllib.request as req
from urllib.error import HTTPError
from bs4 import BeautifulSoup


class ParseWebPages:
    def __init__(self):
        self.pages = dict()

    def getSubCategory(self, Cat_URL, catg):
        """ Extract subcategory from category page

        Parameters
        ----------
            Cat_URL : str
                 A string of main category as part of url
            catg : str
                 Given a short string to indicate the category
        """

        pages = set()
        linkindex = 1
        requestbb = req.Request("http://en.wikipedia.org/wiki/Category:" + Cat_URL)
        try:
            req.urlopen(requestbb)
        except HTTPError as e:
            print(e.code)
            return
        html = req.urlopen(requestbb).read()
        bsObj = BeautifulSoup(html, "html5lib")
        try:
            bsObj.find('div', id="mw-subcategories").find_all('a', href=re.compile("^(/wiki/)((?!;)\S)*$"))
        except AttributeError:
            print("This page is missing something! No worries though!")

        if not bsObj.find('div', id="mw-subcategories"):
            return
        for link in bsObj.find('div', id="mw-subcategories").find_all('a', href=re.compile("^(/wiki/)((?!;)\S)*$")):
            if 'href' in link.attrs:
                if link.attrs['href'] not in pages:
                    newPage = link.attrs['href']
                    linkindex = linkindex + 1
                    pages.add(newPage)
        self.pages.update({catg: pages})

    def getPagesLink(self, cat):
        """Get page links from category and write to files

        Parameters
        ----------
            cat : str
                A short string indicate the category

        """

        val = self.pages.get(cat)
        detail = []
        content = set()
        for links in val:
            request = req.Request("http://en.wikipedia.org" + links)
            try:
                req.urlopen(request)
            except HTTPError as e:
                print(e.code)
                break
            html = req.urlopen(request).read()
            bobj = BeautifulSoup(html, "html5lib")
            if bobj.find('div', id="mw-pages") is None:
                print("nothing is found,next")
                continue
            detail = detail + bobj.find('div', id="mw-pages").find_all('a', href=re.compile("^(/wiki/)((?!;)\S)*$"))
            print(str(len(detail)) + "=" * 15)
        fileindex = 1
        for page in detail:
            href = page.attrs['href']
            if href not in content:
                content.add(href)
                fileindex = fileindex + 1
        filename = "datasets/" + cat + "_Category.txt"
        with open(filename, 'w') as w:
            for line in content:
                w.write(line + "\n")

    def reset_pages(self):
        """
            Reset the pages attribute
        """
        self.pages = dict()
