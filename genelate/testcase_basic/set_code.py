import os
import re


def main():
   num = next_num_gen()
   #print(num)
   p_name = "P-" + format(num, '03') 
   print(p_name)
   build(p_name)

def build(name):
    if not os.path.exists(name):
        os.makedirs(name)
    f1 = open(name+ "/" + name + "_block", mode ='w')
    f2 = open(name+ "/" + name + "_code" , mode ='w')
    pf = 1;
    with open('./_CODE_.txt',encoding='utf-8')as f:
       lines= f.readlines()
       for line in lines:
           if line.startswith("/------"):
             pf  += 1    
           else:
             if pf == 1:
              f1.write(line)
             elif pf == 2:
              f2.write(line)

    f1.close()
    f2.close()
      
def next_num_gen():
   dir_list = []
   dirs = os.listdir(".")
   for name in dirs:
       if name.startswith('P-') and os.path.isdir(name):
           dir_list.append(name)
   
   #for name in dir_list:
   #    print(name)
   
   dir_list.sort(reverse = True)
   
   #for name in dir_list:
   #    print(name)
   
   if len(dir_list) == 0:
      return 1
   last = dir_list[0]
   #print(last)
   num_str_array = re.findall('[0-9]+', last)
   num = int(num_str_array[0])
   return num + 1

if __name__ == "__main__":
    main()
