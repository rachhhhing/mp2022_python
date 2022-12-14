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
    # 获取歌单标题
    title = soup.find('h2', "f-ff2 f-brk").text
    # 获取封面图片
    img = soup.find('img', "j-img").get('data-src')
    res = requests.get(img)
    image = Image.open(BytesIO(res.content))
    try:
        image.save('week14/cover/'+ title + '.jpg')
    except:
        pass
    # 获取创建者id
    idd = soup.find('a', "s-fc7")['href'].split('=')[-1]
    # 获取创建者昵称
    nickname = soup.find('a', "s-fc7").text
    # 获取歌单介绍
    text = soup.find('p', id="album-desc-more").text.replace('\n', '')  
    # 歌单内歌曲数
    songs = soup.find('span', id="playlist-track-count").text
    # 播放量
    plays = soup.find('strong', "s-fc6").text
    # 添加进播放列表次数
    adds = soup.find('a', 'u-btni u-btni-fav')['data-count']
    # 分享次数
    shares = soup.find('a', 'u-btni u-btni-share')['data-count']
    # 歌单评论数
    comments = soup.find('span', id="cnt_comment_count").text
    #print(title,idd,nickname,text,songs,plays,adds,shares,comments)
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
    for i in range(0, 35, 35):
        url = 'https://music.163.com/discover/playlist/?cat=华语&order=hot&limit=35&offset=' + str(i)
        p_jobs.append(p.spawn(producer, url))
    gevent.joinall(p_jobs)
    for id in id_list:
        c_jobs.append(p.spawn(consumer, id))
    gevent.joinall(c_jobs)

    print("总耗时：%.4f" %(time.time()-async_time_start))