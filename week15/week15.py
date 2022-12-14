import os
import csv
import time
import gevent
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup 
from gevent import monkey, pool
monkey.patch_all()
import requests

id_list = []
headers = {  
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'  
    }

def producer(url):
    response = requests.get(url=url, headers=headers)  
    html = response.text 
    soup = BeautifulSoup(html, 'html.parser')   
    ids = soup.select('.dec a')                             # 获取包含歌单详情页网址的标签
    id_list.extend(ids)

def consumer(id):
    url = 'https://music.163.com/' + id['href']             # 获取歌单详情页地址
    response = requests.get(url=url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    # 获取ID
    ID = id['href'].split('=')[-1]
    # 获取歌单标题
    title = soup.find('h2', "f-ff2 f-brk").text
    # 获取歌单介绍
    text = soup.find('p', id="album-desc-more").text.replace('\n', '')
    # 获取创建者昵称
    author = soup.find('a', "s-fc7").text
    # 获取创建日期
    date = soup.find('span', id='time s-fc4')
    mp3_path = 
    related_articles = 
    #print(ID,title,text,author,date,mp3_path,related_articles)
    # 将详情页信息写入CSV文件中
    with open('week14/music_message.csv', 'a+', encoding='utf-8') as f:
        f.write(title + ',' + idd + ',' + nickname + ',' + text + ',' + songs + ',' + plays + ',' + adds + ',' + shares + ',' + comments + '\n')

if __name__=='__main__':
    async_time_start = time.time()
    head = ['歌单标题','id','昵称','介绍','歌曲数量','播放量','添加到播放列表次数','分享次数','评论数']
    with open('week14/music_message.csv', 'w', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(head)
    
    p_jobs = []
    c_jobs = []
    p = pool.Pool(20)   # 控制数目
    for i in range(0, 1300, 35):
        url = 'https://music.163.com/discover/playlist/?cat=华语&order=hot&limit=35&offset=' + str(i)
        p_jobs.append(p.spawn(producer, url))
    gevent.joinall(p_jobs)
    for id in id_list:
        c_jobs.append(p.spawn(consumer, id))
    gevent.joinall(c_jobs)

    print("总耗时：%.4f" %(time.time()-async_time_start))