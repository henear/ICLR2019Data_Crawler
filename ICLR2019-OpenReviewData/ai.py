import numpy as np
import h5py
import string
import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options        
import time

# Meta data of papers
class PaperMeta(object):
    def __init__(self, title, abstract, keyword, rating, url, withdrawn, Review):
        self.title = title  # str
        self.abstract = abstract  # str
        self.keyword = keyword  # list[str]
        self.rating = rating  # list[int]
        self.url = url
        self.withdrawn = withdrawn
        self.review = Review
        
        if len(self.rating) > 0:
            self.average_rating = np.mean(rating)
        else:
            self.average_rating = -1

            
class Keyword(object):
    def __init__(self, keyword, frequency, rating):
        self.keyword = keyword  # list[str]
        self.frequency = frequency
        self.rating = rating  # list[int]        
    
    def average_rating(self):
        if len(self.rating) > 0:
            return np.mean(self.rating)
        else:
            return -1
    
    def update_frequency(self, frequency):
        self.frequency += frequency
        
    def update_rating(self, rating):
        self.rating = np.concatenate((self.rating, rating))
            
            
def write_meta(meta_list, filename):
    f = h5py.File(filename, 'w')
    for i, m in enumerate(meta_list):
        grp = f.create_group(str(i))
        grp['title'] = m.title
        grp['abstract'] = m.abstract
        grp['keyword'] = '#'.join(m.keyword)
        grp['rating'] = m.rating
        grp['url'] = m.url
        grp['withdrawn'] = m.withdrawn        
    f.close()
    
    
def read_meta(filename):
    f = h5py.File(filename, 'r')
    meta_list = []
    for k in list(f.keys()):

        meta_list.append(PaperMeta(
            f[k]['title'].value, 
            f[k]['abstract'].value, 
            f[k]['keyword'].value.split('#'),
            f[k]['rating'].value,
            f[k]['url'].value,
            f[k]['withdrawn'].value,
            f[k]['Review'].value 

        ))
    return meta_list


def crawl_meta(allURLs,meta_hdf5=None, write_meta_name='data.hdf5'):
    result = []
    
    if meta_hdf5 is None:
        # Crawl the meta data from OpenReview
        # Set up a browser to crawl from dynamic web pages
        
        
        executable_path = '/usr/local/bin/chromedriver'
        options = Options()
        options.add_argument("--headless")
        browser = webdriver.Chrome(options=options, executable_path=executable_path)            
    
        # Load all URLs for all ICLR submissions
        urls = []
        with open(allURLs) as f:
            urls = f.readlines()
        urls = [url.strip() for url in urls]
        
        meta_list = [] 
        wait_time = 0.5
        max_try = 2000
        for i, url in enumerate(urls):
            curLine = [""] * 12 
            try:
                browser.get(url)



                time.sleep(wait_time)
                key = browser.find_elements_by_class_name("note_content_field")
                key = [k.text for k in key]
                
                withdrawn = 'Withdrawal confirmation:' in key
                value = browser.find_elements_by_class_name("note_content_value")
                # print(value)
                value = [v.text for v in value]


                # title
                title = "\"" + string.capwords(browser.find_element_by_class_name("note_content_title").text) + "\""
                curLine[0] = title
                # submission_date = browser.find_element_by_class_name("date_item")
                # print(submission_date)
                # print("hhhhhhhhh" + str(submission_date))
                # abstract

                valid = False
                tries = 0
                while not valid:
                    if 'Abstract:' in key:
                        valid = True
                    else:
                        time.sleep(wait_time)
                        tries += 1
                        if tries >= max_try:
                            print('Reached max try: {} ({})'.format(title, url))
                            break
                abstract = ' '.join(value[key.index('Abstract:')].split('\n'))
                abstract.replace("\"", "*")
                abstract.replace("\n", "  ")
                abstract.replace("\\", "\\\\")
                curLine[-4] = "\"" + abstract + "\""
                # keyword
                if 'Keywords:' in key:
                    keyword = value[key.index('Keywords:')].split(',')
                    keyword = [k.strip(' ') for k in keyword]
                    keyword = [''.join(string.capwords(k).split(' ')) for k in keyword if not k == '']
                    for j in range(len(keyword)):
                        if '-' in keyword[j]:
                            keyword[j] = ''.join([string.capwords(kk) for kk in keyword[j].split('-')]) 

                else:
                    keyword = []
                

                # rating
                rating_idx = [i for i, x in enumerate(key) if x == "Rating:"]
                rating = []
                raCount = 0
                if len(rating_idx) > 0:
                    for idx in rating_idx:

                        rating.append(int(value[idx].split(":")[0]))
                        curLine[raCount*2+2] = rating[-1]
                        raCount += 1

                        if raCount >= 3:
                            break



               
                curLine[1] = "\"" + str(keyword) + "\""

                # Review
                review_idx = [i for i, x in enumerate(key) if x == "Review:"]
                review = []
                reCount = 0
                if len(review_idx) > 0:
                    for idx in review_idx:
                        
                        # print(value[idx])
                        value[idx] = value[idx].replace("\"", "*")
                        value[idx] = value[idx].replace("\n", "  ")
                        value[idx] = value[idx].replace("\\", "\\\\")
                        curLine[reCount*2+3] = "\"" + value[idx].replace("\"", "*") + "\""
                        reCount += 1
                        if reCount >= 3:
                            break

                        
                        
                
                print('习近平总书记[{}] [Abs: {} chars, keywords: {}, ratings: {}] {}'.format(
                    i+1, len(abstract), len(keyword), rating, title))
                meta_list.append(PaperMeta(title, abstract, keyword, rating, url, withdrawn))
            except:
                pass
            result.append(curLine)
            
        # Save the crawled data
        write_meta(meta_list, write_meta_name)
    else:
        # Load the meta data from local
        meta_list = read_meta(meta_hdf5)
    # print(curLine)
    return result

# Get the meta data
# Uncomment this if you want to load the previously stored data file
# meta_list = crawl_meta('data.hdf5')
# Uncomment this if you want to cral data from scratch
# meta_list = crawl_meta(allURLs="url2.txt")

# num_withdrawn = len([m for m in meta_list if m.withdrawn])
# print('Number of submissions: {} (withdrwan submissions: {})'.format(
#     len(meta_list), num_withdrawn))
