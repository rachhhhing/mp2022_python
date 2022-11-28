import os
import csv
import time
import requests
from io import BytesIO
from PIL import Image
from queue import Queue
from threading import Thread
from bs4 import BeautifulSoup

# 生产者-消费者模式实现对网易云歌单信息的爬取及整理
def producer(q, url):
    """
    生产者：获取一个分类下的所有歌单的id
    """
    headers = {  
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'  
    }
    response = requests.get(url=url, headers=headers)  
    html = response.text 
    soup = BeautifulSoup(html, 'html.parser')   
    ids = soup.select('.dec a')                             # 获取包含歌单详情页网址的标签
    q.put(ids)

def consumer(q):
    """
    消费者：对每个id获取歌单的详细信息
    """
    headers = {  
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'  
    }
    while True:
        ids = q.get()
        if ids is None:
            break
        else:
            for i in ids:
                url = 'https://music.163.com/' + i['href']      # 获取歌单详情页地址
                response = requests.get(url=url, headers=headers)  
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                # 获取歌单标题  
                title = soup.select('h2')[0].get_text().replace(',', '，')
                # 获取封面图片
                img = soup.select('img')[0]['data-src']
                res = requests.get(img)
                image = Image.open(BytesIO(res.content))
                try:
                    image.save('week12/cover/'+ title + '.jpg')
                except:
                    image.save('week12/cover/'+ title + '.png')
                # 获取创建者id
                idd = soup.select('.s-fc7')[0]['href'].split('=')[-1]
                # 获取创建者昵称
                nickname = soup.select('.s-fc7')[0].get_text()
                # 获取歌单介绍  
                if soup.select('#album-desc-more'):
                    text = soup.select('#album-desc-more')[0].get_text().replace('\n', '').replace(',', '，')  
                else:
                    text = '无'   
                # 歌单内歌曲数  
                songs = soup.select('#playlist-track-count')[0].get_text()
                # 播放量  
                plays = soup.select('.s-fc6')[0].get_text()
                # 添加进播放列表次数
                adds = soup.find('a','u-btni u-btni-fav')['data-count']
                # 分享次数
                shares = soup.find('a','u-btni u-btni-share')['data-count']
                # 歌单评论数
                comments = soup.select('#cnt_comment_count')[0].get_text().replace('评论', '0')
                #print(title,idd,nickname,text,songs,plays,adds,shares,comments)
                # 将详情页信息写入CSV文件中
                with open('week12/music_message.csv', 'a+', encoding='utf-8') as f:
                    f.write(title + ',' + idd + ',' + nickname + ',' + text + ',' + songs + ',' + plays + ',' + adds + ',' + shares + ',' + comments + '\n')

def status():
    start = time.time()
    while True:
        time.sleep(0.5)
        now_time = time.time()-start
        with open('week12/music_message.csv', 'rb') as f:
            length = len(f.readlines()) - 1
        size = os.path.getsize('week12/music_message.csv')
        end_time = now_time / (length+1) * 1300
        end_size = size / (length+1) * 1300

        print(f'\r运行时间：{now_time: .4f} / {end_time: .4f} \
                爬取页数：{length} / 1300 \
                文件内存：{size} / {end_size: .0f}', end='')

if __name__=='__main__':
    head = ['歌单标题','id','昵称','介绍','歌曲数量','播放量','添加到播放列表次数','分享次数','评论数']
    with open('week12/music_message.csv', 'w', encoding='utf-8') as f:
        csv_writer = csv.writer(f)                          # csv格式写入文件file
        csv_writer.writerow(head)
    '''
    s = Thread(target=status)
    s.daemon = True
    s.start()
    '''
    q = Queue()
    plist = []
    clist = []
    for i in range(0, 350, 35): 
        time.sleep(2)
        # 修改每页开始的数据位置即可换页
        url = 'https://music.163.com/discover/playlist/?cat=后摇&order=hot&limit=35&offset=' + str(i)
        p = Thread(target=producer, args=(q, url))
        plist.append(p)
    for p in plist:
        p.start()
    for t in plist:
        p.join()
    for i in range(30): 
        c = Thread(target=consumer, args=(q,))
        clist.append(c)
    for c in clist:
        c.start()
    for c in clist:
        q.put(None)