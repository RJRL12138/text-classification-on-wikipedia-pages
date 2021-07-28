from ContentUtil import ContentUtil
import os

class DownloadPages:
    def __init__(self,dataset):
        """ Initiate with instance of ContentUtil class and check the dataset folder path
            If not exists, create a folder

        Parameters
        ------------
            dataset : str
                The path string of dataset folder
        """
        
        self.ct = ContentUtil()
        self.AI_pre = dataset + "/AI/"
        self.Not_AI_pre = dataset + "/NOT/"
        if not os.path.exists(self.AI_pre):
            os.makedirs(self.AI_pre)
        if not os.path.exists(self.Not_AI_pre):
            os.makedirs(self.Not_AI_pre)
        self.filenames = []
        self.dataset_folder = dataset
        self.dataset = dict()
        for file in os.listdir(dataset):
            if '.txt' in file:
                self.filenames.append(file)

    def readfile(self,writeToFile):
        """ Read page urls from file and get the text data

        Parameters
        -----------
            writeToFile : bool
                A flag determining whether to write file or not
        """
        for file in self.filenames:
            all_page = []
            if "AI" in file:
                prefix = self.AI_pre
                target = "AI"
            else:
                prefix = self.Not_AI_pre
                target = "Not"
            category = file.split(',')[0].split('_')[0]
            print("="*20+"{} Start".format(category)+"="*20)
            postfix = "_"+category+".txt"
            index = 1
            dfile = self.dataset_folder+"/"+file
            with open(dfile,'r',encoding='utf-8') as f:
                for url in f.readlines():
                    url = url.strip('\n')
                    page = self.ct.get_content(url,index,postfix,prefix,writeToFile=writeToFile)
                    all_page.append(page)
                    if index%100 == 0:
                        print("{} finished {} files".format(category, index))
                    index +=1
            self.dataset.update({target:all_page})

