import time
import gevent
from bs4 import BeautifulSoup 
from gevent import monkey, pool
monkey.patch_all()
import requests
import psycopg2

id_list = []
dsn = "dbname=zrq user=postgres password=20020909ZRQ"
headers = {  
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'  
    }

def producer(url):
    response = requests.get(url=url, headers=headers)
    html = response.text 
    soup = BeautifulSoup(html, 'html.parser')   
    ids = soup.select('.dec a')                             # 获取包含歌单详情页网址的标签
    id_list.extend(ids)

def consumer(id, cur):
    url = 'https://music.163.com/' + id['href']             # 获取歌单详情页地址
    response = requests.get(url=url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    # 获取ID
    ID = id['href'].split('=')[-1]
    # 获取歌单标题
    title = soup.find('h2', "f-ff2 f-brk").text
    # 获取歌单介绍
    try:
        text = soup.find('p', id="album-desc-more").text.replace('\n', '')
    except: 
        text = '无'
    # 获取创建者昵称
    author = soup.find('a', "s-fc7").text
    # 获取创建日期
    date = soup.find('span', 'time s-fc4').text[:10]
    #print(ID,title,text,author,date)

    # 将详情页信息写入数据库中
    cur.execute("INSERT INTO music VALUES (%s, %s, %s, %s, %s)", (ID,title,text,author,date))
    
if __name__=='__main__':
    async_time_start = time.time()
    
    p_jobs = []
    p = pool.Pool(20)
    for i in range(0, 1300, 35):
        url = 'https://music.163.com/discover/playlist/?cat=流行&order=hot&limit=35&offset=' + str(i)
        p_jobs.append(p.spawn(producer, url))
    gevent.joinall(p_jobs)

    # 话说我把游标当参数传进去, 就不需要异步连接了啊
    with psycopg2.connect(dsn) as conn:
        with conn.cursor() as cur:
            c_jobs=[p.spawn(consumer, id, cur) for id in id_list]
            gevent.joinall(c_jobs)
    conn.commit()

    print("总耗时：%.4f" %(time.time()-async_time_start))