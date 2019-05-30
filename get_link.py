import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import string
import pickle
import os 
home = os.getcwd()
ua = UserAgent()
header = {'user-agent':ua.chrome}

start_url = "http://big5.chengyudaquan.org"




start_get = requests.get(start_url,header) 
start_soup = BeautifulSoup(start_get.content,'lxml')

#取得所有分類的url----------------------------------------------------
#重疊成語  非四字成語
  
count = 0 
overlapping_link = []
not_four_word_link = []
for c1_1_ul in start_soup.find_all('div',attrs={"class":"c1 l"}):
    for c1_1_ul_a in c1_1_ul.find_all('ul'):
        count += 1
        if count == 2: #取得重疊成語
                for c1_1_ul_a_href in c1_1_ul_a.find_all("li"): #取得所有的連結
                        
                        #print(c1_1_ul_a_href)
                        overlapping_link.append(start_url+c1_1_ul_a_href.a["href"])

        
        if count == 3: #取得非四字成語
                for c1_1_ul_a_href in c1_1_ul_a.find_all("li"): #取得所有的連結
                        
                        #print(c1_1_ul_a_href)
                        not_four_word_link.append(start_url+c1_1_ul_a_href.a["href"])

         
#print(overlapping_link)
other_link = []
print("---------------------------------------------------------------------")
for c2_1 in start_soup.find_all('div',attrs={"class":"c2 l"}):
    for c2_a in c2_1.find_all('a'):
            #print(c2_a['href'])
            other_link.append(start_url+c2_a['href'])
            break



#取得重疊成語的上排連結
above_link = []

for link in overlapping_link:
        overlapping_get = requests.get(link,header) 
        overlapping_soup = BeautifulSoup(overlapping_get.content,'lxml')
        
        for overlapping_soup_english in overlapping_soup.find('ul',attrs={'class':'list2'}):
                if overlapping_soup_english.string != " " and overlapping_soup_english!='\n':
                        above_link.append(start_url+overlapping_soup_english.a["href"])
                        #print(overlapping_soup_english)
       
# #         break

# #取得頁數連結
print(overlapping_link)
for link in overlapping_link:
        overlapping_get = requests.get(link,header) 
        overlapping_soup = BeautifulSoup(overlapping_get.content,'lxml')
         
        for overlapping_soup_page in overlapping_soup.find('select',attrs={'id':'page_select'}):

                #print(overlapping_soup_page)
                if overlapping_soup_page.string != " " and overlapping_soup_page!='\n':
                        above_link.append(start_url+overlapping_soup_page["value"])
                        #print(overlapping_soup_page["value"])
        break


#print(not_four_word_link)
#非四字成語
# for link in not_four_word_link:
#         not_four_word_get = requests.get(link,header)
#         not_four_word_soup = BeautifulSoup(not_four_word_get.content,'lxml')
#         not_four_word_soup_datalist = not_four_word_soup.find('table',attrs={'class':'datalist'})
        
#         for not_four_word_soup_tr in not_four_word_soup_datalist.find_all('tr',):
#                 #print(not_four_word_soup_tr.td)
#                 if not_four_word_soup_tr.td != None:
#                         #print(not_four_word_soup_tr.td.a["href"])
#                         above_link.append(start_url+not_four_word_soup_tr.td.a["href"])
                        

#         break


#取得其他成語的上排連結
for link in other_link:
        other_get = requests.get(link,header) 
        other_soup = BeautifulSoup(other_get.content,'lxml')
        for other_soup_english in other_soup.find('ul',attrs={'class':'list2'}):
                if other_soup_english.string != " " and other_soup_english!='\n':
                        above_link.append(start_url+other_soup_english.a["href"])
                        #print(other_soup_english)
        


#處理重疊成語和其他成語
all_word = []
for word_link in above_link:
    
    
    print(word_link)
    source = requests.get(word_link,headers=header)
    soup = BeautifulSoup(source.content,'lxml')   

    body = soup.body
    
    for ul_list in body.find('ul',attrs={"class":"list"}):
        #print(ul_list)
        if ul_list.string != '\n' and ul_list.string != " ":
            word = ul_list.a["href"]
            word = start_url+word
            word_source = requests.get(word,headers=header,timeout=10)
            word_soup = BeautifulSoup(word_source.content,'lxml')
            word_box = word_soup.find_all('div',attrs={'class':'content'})
            words  = []
            for word_box_word in word_box[0].children:
                if word_box_word.string != '\n' and word_box_word.string != None:
                    words.append(word_box_word.string)
                    #print(word_box_word.string)
            all_word.append(words)
            print(words)
            #break

    #break




print(len(all_word))

path = os.path.join(home,'save.pickle')
with open(path,'rb') as fp:
        pickle.dump(all_word,fp)
