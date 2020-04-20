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


umap_csv = 'filtered_map_data3.csv'


df_original = pd.read_csv(umap_csv)



def filter(row):
    url_str= row['modified_url_list']
    refined_result_str = ''
    other_result_str = ''
    url_str = url_str.strip('[')
    url_str = url_str.strip(']')
    if url_str == '\s' or url_str ==' ' or url_str == '':
        print('empty string found, exit')
        return refined_result_str, other_result_str
    url_list = url_str.split(',')
    pattern = r'(pdf|aspx|asp|map+)/?$|map+|campus+|location+'
    pattern_pdf = r'pdf$'
    pattern_except = r'(corona|degree|hotel|park)+'
    rule_pdf = re.compile(pattern_pdf)
    rule_other = re.compile(pattern)
    rule_except = re.compile(pattern_except)
    for u in url_list:
        u = u.strip(' \'')
        u = u.rstrip('\'')
        u = u.lstrip('\'')
        #print(u)
        m_except = list(re.finditer(rule_except, u))
        #print(m)
        if len(m_except) != 0:
            print(m_except)
            print('invalid result: ' + u)
            continue
        else:
            m_pdf = list(re.finditer(rule_pdf, u))
            if len(m_pdf) != 0:
                #print('pdf found: ' + u)
                refined_result_str += u
                refined_result_str += ', '
            else:
                m_other = list(re.finditer(rule_other, u))
                if len(m_other) != 0:
                    #print('a possible link: ' + u)
                    other_result_str += u
                    other_result_str += ', '
    return refined_result_str, other_result_str




df_original.loc[:,'refined_result'],df_original.loc[:,'other_possible_result'] = zip(*df_original.apply(filter, axis=1))
df_original.to_csv('filtered_data6.csv')