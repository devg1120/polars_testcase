import os
import bs4
import csv # モジュール"CSV"の呼び出し
import sys
import html
import re
import json

import polars as pl
from termcolor import colored

#import warnings
import math 

"""

Polarsでデータサイエンス100本ノックを解く（前編）
https://qiita.com/_jinta/items/28442d25bba067c13bb7

Polarsでデータサイエンス100本ノックを解く（後編）
https://qiita.com/_jinta/items/394b1682893e5991d592

データサイエンス100本ノック（構造化データ加工編）
https://github.com/The-Japan-DataScientist-Society/100knocks-preprocess
"""


ignore_list = [
               'P-058',  #module 'polars' has no attribute 'get_dummies'
               #'P-076',  #apply  => map_elements
               'P-086',  #begin
               'P-090',  #model_selection
               'P-091',  #apply
               'P-095',  #pyarrow
        ]

stmts_list = [
               'P-039',
               'P-043',
               'P-044',

               'P-059',
               'P-060',

               'P-076',

               'P-081',
               'P-082',
               'P-083',
               'P-084',
               'P-085',
               'P-087',
               'P-088',
               'P-089',
               'P-090',
               'P-091',
               'P-092',
               'P-094',
               'P-095',
               'P-096',
               'P-099',
        ]

ignore_list = []
stmts_list = []


input_filename = "01_50.html"
#input_filename = "51_100.html"

#PRINT = False
PRINT = True
NAME_PRINT = False
SOURCE_PRINT = False
SINGLE_TEST = False
TESTNO = 0
RANGE_TEST = False
TESTNO_FROM = 0
TESTNO_TO   = 0
DUMP = False
SAVEPATH = None

def help():
  print("""
  python <script_name> <path>                 //all test
  python <script_name> <path> -I              //ignore reset all test
  python <script_name> <path> -n              //name print
  python <script_name> <path> -s              //block/code  print
  python <script_name> <path> -d <outpath>    //md build
  python <script_name> <path> -t <num>        //one test
  python <script_name> <path> -r <num>-<num>  //range test
  python <script_name> <path> -It <num>       //reset ignore one test
  python <script_name> <path> -Ir <num>-<num> //reset ignore range test
  python <script_name> -i                     //ignore list
  """)
  sys.exit()

def yes_no_input():
    while True:
        choice = input("Please respond with 'yes' or 'no' [y/N]: ").lower()
        if choice in ['y', 'ye', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False

def print_ignore_list():
     print(ignore_list)

input_path = ""
args = sys.argv
if len(args) >= 2:
    if args[1] == '-i':
        print_ignore_list()
        sys.exit()
    input_path = args[1]

else:
    help()

#ignore_list = [
if len(args) >= 3:
    if args[2] == '-I':
        ignore_list = []
    elif args[2] == '-n':
        PRINT = False
        NAME_PRINT = True
    elif args[2] == '-s':
        PRINT = False
        SOURCE_PRINT = True
    elif args[2] == '-t':
        PRINT = True
        SINGLE_TEST = True
        if len(args) == 4:
           TESTNO = int(args[3])
        else:
           help()
    elif args[2] == '-It':
        ignore_list = []
        PRINT = True
        SINGLE_TEST = True
        if len(args) == 4:
           TESTNO = int(args[3])
        else:
           help()
    elif args[2] == '-r':
        PRINT = True
        RANGE_TEST = True
        if len(args) == 4:
           RANGE = args[3].split('-')
           if len(RANGE) != 2:
               help()
           TESTNO_FROM = int(RANGE[0])
           TESTNO_TO   = int(RANGE[1])
        else:
           help()
    elif args[2] == '-Ir':
        ignore_list = []
        PRINT = True
        RANGE_TEST = True
        if len(args) == 4:
           RANGE = args[3].split('-')
           if len(RANGE) != 2:
               help()
           TESTNO_FROM = int(RANGE[0])
           TESTNO_TO   = int(RANGE[1])
        else:
           help()
    elif args[2] == '-d':
        DUMP = True
        PRINT = False
        if len(args) == 4:
           SAVEPATH = args[3]
           if not os.path.isdir(SAVEPATH):
              print("not exist: ", SAVEPATH);
              sys.exit()
        else:
           help()
    else:
      help()

if DUMP:
  print("Are you sure you want to run it? dump...")
  if not yes_no_input():
      sys.exit()


dtypes = {
    'customer_id': str,
    'gender_cd': str,
    'postal_cd': str,
    'application_store_cd': str,
    'status_cd': str,
    'category_major_cd': str,
    'category_medium_cd': str,
    'category_small_cd': str,
    'product_cd': str,
    'store_cd': str,
    'prefecture_cd': str,
    'tel_no': str,
    'postal_cd': str,
    'street': str,
    'application_date': str,
    'birth_day': pl.Date
}

df_customer = pl.read_csv("../data/customer.csv", dtypes=dtypes)
df_category = pl.read_csv("../data/category.csv", dtypes=dtypes)
df_product  = pl.read_csv("../data/product.csv",  dtypes=dtypes)
df_receipt  = pl.read_csv("../data/receipt.csv",  dtypes=dtypes)
df_store    = pl.read_csv("../data/store.csv",    dtypes=dtypes)
df_geocode  = pl.read_csv("../data/geocode.csv",  dtypes=dtypes)

#df_customer = pl.read_csv("../data/customer.csv")
#df_category = pl.read_csv("../data/category.csv")
#df_product  = pl.read_csv("../data/product.csv")
#df_receipt  = pl.read_csv("../data/receipt.csv")
#df_store    = pl.read_csv("../data/store.csv")
#df_geocode  = pl.read_csv("../data/geocode.csv")

def p(str):
    if PRINT:
       print(str)

def sp(str):
    if PRINT:
       print(str)
    else:
       if SOURCE_PRINT:
          print(str)

gv = {
      'df_receipt':  df_receipt ,
      'df_customer': df_customer,
      'df_product':  df_product,
      'df_geocode':  df_geocode,
      'df_category': df_category,
      'df_store':    df_store,
      
      'pl':pl
     }

def _save(path_w, data):
    with open(path_w, mode='w') as f:
         f.write(data)

def _read(path_r):
    with open(path_r) as f:
        s = f.read()
    return s

def dump(name, block, code):
    subdir_name = name.rstrip(':')
    _path = SAVEPATH +'/' + subdir_name
    print("dump: " , _path)
    if not os.path.isdir(_path):
         print("not subdir: " , _path)
         os.mkdir(_path)

    #print(block)
    #print(code)
    block_path = _path + "/"  + subdir_name + "_block"
    code_path  = _path + "/"  + subdir_name + "_code"
    #print(block_path)
    #print(code_path)
    #print(type(block))
    #print(type(code))
    _save(block_path, block)
    _save(code_path,  code)

def exec_stmt(stmt):
    lv = {'ans' : "not anser"}
    exec(stmt,gv,lv)
    return lv["ans"]


def ignore(name):
    return name in ignore_list


def is_stmts(name):
    return name in stmts_list

def check_statement(name, code):
    print("                    ", end="")
    if ignore(name):
        print(colored("*** ignore statement","red"))
        return (True, None)

    elif is_stmts(name) :
        print(colored("*** multi statement","green"))
        t = exec_stmt(code)
        #p(t)
        return (True, t)

    else:
        print("... good statement")
        return (False, None)


def stmt_type(name ):
    if ignore(name):
        print(colored("*** ignore stmt","red"), end="")

    elif is_stmts(name) :
        print(colored("*** multip stmt","green"), end="")

    else:
        print("... normul stmt", end="")


#soup = bs4.BeautifulSoup(open('01_50.html'), 'html.parser')
#soup = bs4.BeautifulSoup(open('51_100.html'), 'html.parser')
#soup = bs4.BeautifulSoup(open(input_filename), 'html.parser')

#links = soup.find_all('h4') # 全てのaタグ要素を取得
#_path = "../testcase"

setpath = input_path + "/" + 'set.json'

if  os.path.exists(setpath):
   json_open = open(setpath, 'r')
   json_load = json.load(json_open)
   
   ignore_list = json_load['ignore_list']
   stmts_list = json_load['stmts_list']


dirs = os.listdir(input_path)
#links = os.listdir(_path)


csvlist = [] # 配列を作成

# SINGLE_TEST
# TESTNO

dirs.sort()
for name in dirs:
    #name = link.text.lstrip()
    block = None
    code = None
    if not name.startswith('P-'):
        continue

    if NAME_PRINT:
        print(name, end=" ")
        stmt_type(name)
        print("")
        continue

    if SINGLE_TEST:
        #test_name = "P-" + format(TESTNO, '03') + ":" 
        test_name = "P-" + format(TESTNO, '03') 
        if test_name  != name :
            continue

    if RANGE_TEST:
        #print("RANGE_TEST")
        num_str_array = re.findall('[0-9]+', name)
        #print(num_str_array );
        if len(num_str_array) == 0:
            continue
        #print(num_str_array );
        num = int(num_str_array[0])
        #print(num,TESTNO_FROM, TESTNO_TO)
        if TESTNO_FROM > num or TESTNO_TO < num :
            continue
    block_path = input_path + "/" + name + "/" + name + "_block"
    code_path  = input_path + "/" + name + "/" + name + "_code"

    block = _read(block_path)
    code = _read(code_path)

    print("=======================")
    #print(name+ " ", end="")
    print(name+ " ")
    print("------------- bkock")
    print(block)
    print("------------- code")
    print(code)
    #continue 
    try:
       c = check_statement(name, code)
       if c[0]:
           p("------------- result")
           p(c[1])
           p("END: "+ name)
       else:
           r = eval(code)
           p("------------- result")
           p(r)
           p("END: "+ name)
    except Exception as e:
       print("Exception:")
       print(name)
       print(e)
       sys.exit()

    #sys.exit()



