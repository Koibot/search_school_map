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


umap_csv = 'filtered_map_data2.csv'


df_original = pd.read_csv(umap_csv)

df_t2 = df_original.head().copy()


def search_map_r3(row):
    grammar = r"""
                NP: 
                {<NNP><CC|IN>?<NNP>+}
                {}
                {<DT|PP\$>?<JJ>*<NN>}
                """
    cp = nltk.RegexpParser(grammar)
    campus_name = ''
    filtered_word = ''
    campus_kw = r'Campus|campus'
    college_name = row['new correct link']
    college_name = college_name.strip('www.')
    college_name = college_name.strip('.edu')
    print('college name: '+college_name)
    words = nltk.word_tokenize(row['STORE_NAME'])
    result_url_list = []
    # print(words)
    tagged = nltk.pos_tag(words)
    # print(tagged)
    t = cp.parse(tagged)
    # print(t)
    for st in t.subtrees():
        if st.label() == 'NP':
            print(st.leaves())
            print(st)
            np = ' '.join([w for w, t in st.leaves()])
            # print(np)
            campusname_position = [m.start() for m in re.finditer(campus_kw, np)]
            if campusname_position != -1 and len(campusname_position) != 0:
                print(np)
                print('exist campus')
                campus_name = np
                break
    return campus_name+' '+ college_name


def search_map_r2(row):
    search_keywords = ''
    availability = row['Verified']
    lk = row['LINK']
    try:
        response = requests.get(lk)
    except requests.ConnectionError as e:
        print('invalid link')
        print('try to get search keyword')


def search_map_r4(row):
    result_url_list = []
    search_kw = row['STORE_NAME']
    search_kw = search_kw + ' map'
    for u in search(search_kw, tld='com', num=5, stop=5, pause=2):
        print(u)
        striped_u = u.strip('https://')
        decomposed_link = striped_u.split('/')
        pt = r'^www|edu$|pdf$'
        rule = re.compile(pt)
        counter = 0
        cc = 0
        for e in decomposed_link:
            counter = counter + 1
            m = list(re.finditer(rule, e))
            if len(m) != 0:
                print('find one possible link: '+u)
                result_url_list.append(u)
    print(result_url_list)
    return result_url_list


df_original.loc[:, 'modified_url_list'] = df_original.apply(search_map_r4, axis=1)
df_original.to_csv('filtered_map_data3.csv')