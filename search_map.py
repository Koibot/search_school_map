import urllib3
import requests
import pandas as pd
from googlesearch import search
import re
import nltk
from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from nltk import Tree

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

umap_excel = 'map_search.xlsx'
#umap_excel = 'filtered_map_data.xlsx'

df = pd.read_excel(umap_excel)

testdf = df.head()


# url = ['http://www.gwu.edu/sasasa/', 'http://www.smu.edu', '']#list of url of colleges

def search_college_url(college_name_raw):
    grammar = r"""
            NP: 
            {<NNP><CC|IN>?<NNP>+}
            {}
            {<DT|PP\$>?<JJ>*<NN>}
            """
    cp = nltk.RegexpParser(grammar)
    u_name = ''
    filtered_word = ''
    search_keyword = r'University|College|University+of'
    words = nltk.word_tokenize(college_name_raw)
    result_url_list = []
    # print(words)
    tagged = nltk.pos_tag(words)
    # print(tagged)
    t = cp.parse(tagged)
    # print(t)
    for st in t.subtrees():
        if st.label() == 'NP':
            # print(st.leaves())
            # print(st)
            np = ' '.join([w for w, t in st.leaves()])
            # print(np)
            tc = [m.start() for m in re.finditer(search_keyword, np)]
            if tc != -1 and len(tc) != 0:
                print(np)
                print('this is the relevant information')
                u_name = np
                break
    u_map_kw = u_name + ' ' + 'map' + 'location'
    for u in search(u_name, tld='com', num=10, stop=1, pause=2):
        result_url_list.append(u)
    print(result_url_list)
    return result_url_list


def not_a_search_college_url(college_name_raw):
    c_url = ''
    url_list = []
    kw = ''
    # grammar = r"""
    # NP: {<DT|PP\$>?<JJ>*<NN>}
    # {<NNP>+}
    # {<NNP><CC>?<NNP>}
    # """
    grammar = r"""
        NP: 
        {<NNP><CC>?<NNP>+}
        {}
        {<DT|PP\$>?<JJ>*<NN>}
        """
    cp = nltk.RegexpParser(grammar)
    words = nltk.word_tokenize(college_name_raw)
    tagged = nltk.pos_tag(words)
    #print(tagged)
    t = cp.parse(tagged)
    for st in t.subtrees():
        if st.label() == 'NP':
            #print(st.leaves())
            #print(st)
            np = ' '.join([w for w, t in st.leaves()])
            print(np)
            ptn = r'.[University]|.[College]'
            rule = re.compile(ptn)
            m = re.search(rule, np)
            print(m)
            if m is not None:
                print(np)
                for u in search('William Marshall College', tld='edu', num=10, stop=1, pause=2):
                    print(u)
                #url_list = list(str(u) for u in search(kw, tld='edu', stop=1))
    return '0'


def search_base_url(row):
    ret = ''
    availability = row['Verified']
    pt = r'^www|edu$'
    rule = re.compile(pt)
    lk = row['LINK']
    if isinstance(lk, float) or len(lk) == 0:
        ret = search_college_url(row['STORE_NAME'])
        return ret
    dec_l = row['LINK'].split('/')
    if availability == ('404' or '500') or 'OE':
        for e in dec_l:
            #print(e)
            m = list(re.finditer(rule, e))
            if len(m) != 0:
                ret = e
                break
    return ret


def is_available(row):
    u = str(row['LINK'])
    nv = ''
    ncl = ''
    if len(u) != 0 and u != 'nan':
        print(u + ' is not null')
        try:
            res = requests.get(u)
        except requests.ConnectionError as e:
            return 'OE'
        c = res.status_code
        if c == 404:
            #print('website ' + u + ' does not exist')
            nv = '404'
            return nv
        elif c == 500:
            #print('can not reach server of ' + u)
            nv = '500'
            return nv
        elif c == 200:
            #print('url ' + u + ' exists')
            nv = 'E'
            return nv
    else:
        print('url does not exist')
        uname_raw = row['STORE_NAME']
        #print(ncl)
        nv = 'NE'
        return nv
    return nv


df.loc[:, 'Verified'] = df.apply(is_available, axis=1)
df.loc[:, 'new correct link'] = df.apply(search_base_url, axis=1)
df.to_csv('filtered_map_data2.csv')