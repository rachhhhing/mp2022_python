import datetime
import psycopg2
import psycopg2.extras

dsn = "dbname=zrq user=postgres password=20020909ZRQ"

def select(keyword, mode, sheet='music'):
    if mode == 'title':
        command = f"select * from {sheet} where {mode} like '%{keyword}%'"
    else:
        command = f"Select * from {sheet} where {mode} = '{keyword}'"
    with psycopg2.connect(dsn) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as dict_cur:
            dict_cur.execute(command)
            res = dict_cur.fetchall()
            music = [r['title'] for r in res]
    return music

print('-----按ID-----')
for music in select('4891546330', '"ID"'): print(music)
print('-----按title-----')
for music in select('夏天', 'title'): print(music)
print('-----按author-----')
for music in select('网易云音乐', 'author'): print(music)
print('-----按date-----')
for music in select(datetime.date(2020,5,20), 'date'): print(music)