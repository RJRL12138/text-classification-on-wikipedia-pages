# encode=utf8
import datetime
import os
import random
import re
import urllib.request as req
from urllib.error import HTTPError
from nltk.corpus import stopwords
import nltk
from bs4 import BeautifulSoup

random.seed(datetime.datetime.now())


class ContentUtil:
    def __init__(self):
        """initiate with loading stopwords list

        Parameters
        ----------
        Default load stopwords from file stopword.txt
        If file not exists, use stopword from NLTK package

        """
        self.stopwordset = set()
        if os.path.exists("stopword.txt"):
            with open("stopword.txt", 'r') as f:
                for line in f.readlines():
                    line = line.rstrip('\n')
                    self.stopwordset.add(line)
        else:
            nltk.download('stopwords')
            self.stopwordset = set(stopwords.words('english'))

    def getStopWords(self):
        """ Return the stopword set

        Returns
        -------
            A set of stopwords
        """

        return self.stopwordset

    def loadData(self, AI_path, Not_AI_path):
        """Load data from files without labels

        Parameters
        ----------
        AI_path : str
            The file location of the AI dataset
        Not_AI_path : str
            The file location of the Not AI dataset

        Returns
        -------
        list,list
            list of AI data and Not AI data
        """

        AI_pages = []
        Not_AI_pages = []
        if not (os.path.exists(AI_path) and os.path.exists(Not_AI_path)):
            print("Invalid folder. Try it again!")
            return
        operator = re.compile('(\W)+')
        AI_filename = [f for f in os.listdir(AI_path) if ".txt" in f]
        Not_filename = [f for f in os.listdir(Not_AI_path) if ".txt" in f]
        for file in AI_filename:
            raw = open(AI_path + file, 'r').read()
            raw = operator.sub(' ', raw)
            raw = operator.sub(' ', raw)
            AI_pages.append(raw)
        for file in Not_filename:
            raw = open(Not_AI_path + file, 'r').read()
            raw = operator.sub(' ', raw)
            raw = operator.sub(' ', raw)
            Not_AI_pages.append(raw)
        return AI_pages, Not_AI_pages

    def load_with_label(self,AI_path,Not_AI_path):
        """Load data from files with labels

        Parameters
        ----------
        AI_path : str
            The file location of the AI dataset
        Not_AI_path : str
            The file location of the Not AI dataset

        Returns
        -------
        list,list
            list of AI data and Not AI data with labels
            list[list[data,label]]
        """


        AI_pages = []
        Not_AI_pages = []
        if not (os.path.exists(AI_path) and os.path.exists(Not_AI_path)):
            print("Invalid folder. Try it again!")
            return
        operator = re.compile('(\W)+')
        label = re.compile("_(.*?)\.")
        AI_filename = [f for f in os.listdir(AI_path) if ".txt" in f]
        Not_filename = [f for f in os.listdir(Not_AI_path) if ".txt" in f]
        for file in AI_filename:
            ltxt = label.search(file).group(1)
            raw = open(AI_path + file, 'r').read()
            raw = operator.sub(' ', raw)
            raw = operator.sub(' ', raw)
            AI_pages.append([raw,ltxt])
        for file in Not_filename:
            ltxt = label.search(file).group(1)
            raw = open(Not_AI_path + file, 'r').read()
            raw = operator.sub(' ', raw)
            raw = operator.sub(' ', raw)
            Not_AI_pages.append([raw,ltxt])
        return AI_pages, Not_AI_pages

    def get_txt(self, linkurl):
        """Get text from a url

        Parameters
        ----------
        linkurl : str
            The url used to get text

        Returns
        --------
            BeautifulSoup object

        """


        thtml = req.Request("https://en.wikipedia.org" + linkurl)
        try:
            req.urlopen(thtml)
        except HTTPError as e:
            print(e)
            return
        tht = req.urlopen(thtml).read()
        txtObj = BeautifulSoup(tht, 'html5lib')
        return txtObj.find('div', id="mw-content-text")

    def get_content(self, urls, index, postfix, prefix, writeToFile=True):
        """Get text from HTML pages

        Parameters
        ----------
            urls : str 
                The target url used to extract text
            index : int
                The index number of file used to name files
            postfix : str
                A string used as output files' postfix
            prefix : str
                A string used as output files' prefix
            writeToFile : bool
                A flag to determine whether to write output files or not
                Default as True

        Returns
        --------
            str 
            Return text from HTML pages
        """

        
        ttobj = self.get_txt(urls)
        if ttobj is None:
            return
        ttobj.noscript.decompose()
        if ttobj.find('span', class_="mwe-math-element"):
            mathTag = ttobj.find_all('span', class_="mwe-math-element")
            for mTag in mathTag:
                mTag.decompose()
        if ttobj.find('div', id="toc"):
            ttobj.find('div', id="toc").decompose()
        if ttobj.find('div', role="note"):
            for note in ttobj.find_all('div', role="note"):
                note.decompose()
        if ttobj.find('table', class_="infobox"):
            for table in ttobj.find_all('table', class_="infobox"):
                table.decompose()
        if ttobj.find('table', class_="vertical-navbox"):
            for table in ttobj.find_all('table', class_="vertical-navbox"):
                table.decompose()
        pure = ttobj.get_text()
        pp = self.clearstopwords(pure)
        if writeToFile:
            filename = prefix + str(index) + postfix
            ff = open(filename, 'w')
            ff.write(pp)
            ff.close()
            return pp
        else:
            return pp

    def clearstopwords(self, text):
        """Remove punctuations and other non alphabetic characters

        Parameters
        ----------
            text : The target to be cleaned

        Returns
        -------
            str
            Return the strings after removing characters
        """


        reference = re.compile("((See\salso\[)|(References\[)){1}(\s|\S)+")
        nota = re.compile("\[(\w){0,4}\]")
        blank = re.compile("^((\s*)\n)|(\n){2,}")
        bracket = re.compile('\\(|\\)|\\[|\\]|\\{|\\}')
        operator = re.compile('(\*|\+|\&|\-|\$|\=|\%|\^|\/)+')
        number = re.compile("(\d)+")
        comma = re.compile('\\"')

        pp = reference.sub('', text)
        pp = comma.sub(' ', pp)
        pp = number.sub(' ', pp)
        pp = operator.sub(' ', pp)
        pp = blank.sub('', pp)
        pp = bracket.sub('', pp)
        pp = nota.sub('', pp)
        return pp
