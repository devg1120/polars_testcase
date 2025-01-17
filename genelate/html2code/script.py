import os
import bs4
import csv # モジュール"CSV"の呼び出し
import sys
import html

import polars as pl
from termcolor import colored

"""

Polarsでデータサイエンス100本ノックを解く（前編）
https://qiita.com/_jinta/items/28442d25bba067c13bb7

Polarsでデータサイエンス100本ノックを解く（後編）
https://qiita.com/_jinta/items/394b1682893e5991d592

データサイエンス100本ノック（構造化データ加工編）
https://github.com/The-Japan-DataScientist-Society/100knocks-preprocess
"""

#soup = bs4.BeautifulSoup(open('01_50.html'), 'html.parser')
#soup = bs4.BeautifulSoup(open('51_100.html'), 'html.parser')
#soup = bs4.BeautifulSoup(open(input_filename), 'html.parser')

input_filename = "01_50.html"
#input_filename = "51_100.html"

#PRINT = False
PRINT = True
SOURCE_PRINT = False
SINGLE_TEST = False
TESTNO = 0
DUMP = False
SAVEPATH = None

def help():
  print("""
  python <script_name> 50/100         all print
  python <script_name> 50/100 -n      name print
  python <script_name> 50/100 -s      souce print
  python <script_name> 50/100 -d <savepath>     dump
  python <script_name> 50/100 -t <number>       one test
  """)
  sys.exit()

def yes_no_input():
    while True:
        choice = input("Please respond with 'yes' or 'no' [y/N]: ").lower()
        if choice in ['y', 'ye', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False

args = sys.argv
if len(args) >= 2:
    if args[1] == '50':
        input_filename = "01_50.html"
    elif args[1] == '100':
        input_filename = "51_100.html"
    else:
        help()
else:
    help()

if len(args) >= 3:
    if args[2] == '-n':
        PRINT = False
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

ignore_list = [
               'P-057:',
               'P-058:',
               'P-068:',
               'P-069:',
               'P-072:',
               'P-073:',
               'P-075:',
               'P-076:',
               'P-085:',
               'P-086:',
               'P-088:',
               'P-089:',
               'P-090:',
               'P-091:',
               'P-094:',
               'P-095:',
               'P-096:',
               'P-097:',
               'P-098:',
               'P-099:',
               'P-100:',
        ]

stmts_list = [
               'P-039:',
               'P-043:',
               'P-044:',

               'P-059:',
               'P-060:',
               'P-081:',
               'P-082:',
               'P-083:',
               'P-084:',
               'P-085:',
               'P-087:',
               'P-088:',
               'P-089:',
               'P-090:',
               'P-091:',
               'P-092:',
        ]

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
      'pl':pl
     }

def _save(path_w, data):
    with open(path_w, mode='w') as f:
         f.write(data)

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
    #    print(colored("**** error statement ****","red"))
    #    print(colored("**** multi statement ****","green"))
    if ignore(name):
        print(colored("**** ignore statement ****","red"))
        return True

    elif is_stmts(name) :
        print(colored("**** multi statement ****","green"))
        t = exec_stmt(code)
        p(t)
        return True

    #if name == "P-039:" :
    #    print(colored("**** multi statement ****","green"))
    #    t = exec_stmt(code)
    #    p(t)
    #    return True

    #elif name == "P-043:" :
    #    print(colored("**** multi statement ****","green"))
    #    t = exec_stmt(code)
    #    p(t)
    #    return True

    #elif name == "P-044:" :
    #    print(colored("**** multi statement ****","green"))
    #    t = exec_stmt(code)
    #    p(t)
    #    return True

    else:
        print(".... good statement ....")
        return False



#soup = bs4.BeautifulSoup(open('01_50.html'), 'html.parser')
#soup = bs4.BeautifulSoup(open('51_100.html'), 'html.parser')
soup = bs4.BeautifulSoup(open(input_filename), 'html.parser')

links = soup.find_all('h4') # 全てのaタグ要素を取得

csvlist = [] # 配列を作成

# SINGLE_TEST
# TESTNO

for link in links: # aタグのテキストデータを配列に格納
    name = link.text.lstrip()
    block = None
    code = None
    if not name.startswith('P-'):
        continue

    if SINGLE_TEST:
        test_name = "P-" + format(TESTNO, '03') + ":" 
        if test_name  != name :
            continue
    print("=======================")
    #print(name+ " ", end="")
    print(name+ " ")
    #print("------------- name end")
    sample_txt = name
    csvlist.append(sample_txt)
    block = soup.select(f'h4:-soup-contains("{name}") ~ blockquote')
    html = block[0]
    b_code = bs4.BeautifulSoup(html.get_text(), 'html.parser')
    p("------------- block")
    p(b_code)
    p("------------- block end")
    if DUMP:
        block = b_code.text
    div_code = soup.select(f'h4:-soup-contains("{name}") ~ div')
    if len(div_code)>0:
        divhtml = div_code[0]

        soup_code = bs4.BeautifulSoup(divhtml.get_text(), 'html.parser')
        if soup_code:
           sp("------------- code")
           sp(soup_code.text)
           sp("------------- code end")
           if DUMP:
               code = soup_code.text
           try:
              if not check_statement(name, soup_code.text):
                  r = eval(soup_code.text)
                  p(r)
                  p("END: "+ name)
           except Exception as e:
              print("Exception:")
              print(name)
              print(e)
              sys.exit()

        #sys.exit()
    if DUMP:
        dump(name, block, code)



