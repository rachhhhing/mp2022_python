import os
import calendar
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import date
import matplotlib.pyplot as plt
from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import ChartType
from pyecharts.globals import ThemeType

class Data_analyze:
    '''
    数据分析类
    '''
    def __init__(self, dir_path):
        """
        数据的读取

        :param dir_path:数据文件所在文件夹
        """
        self._df = []                                           # 每个csv文件按df格式储存进列表
        self._area = ["Aotizhongxin","Changping","Dingling","Dongsi","Guanyuan","Gucheng","Huairou","Nongzhanguan","Shunyi","Tiantan","Wanliu","Wanshouxigong"]
        self._pollutant = ["PM2.5","PM10","SO2","NO2","CO","O3"]
        self._climate = ["TEMP","PRES","DEWP","RAIN","wd","WSPM"]

        print("-----数据读取中，请稍后-----")
        files = os.listdir(dir_path)                            # 获取目录下所有的文件
        for path in files:
            with open(dir_path + "/" + path) as f:
                df = pd.read_csv(f)
                df = df.set_index("No")
                self._df.append(df)
        print("-----数据读取完成-----")

    def time_analyze(self, pol, area):
        """
        时间分析：某区域某类型污染物随时间的变化(PS:以均值代表每天的污染物含量)

        :param pol:污染物类型
        :param area:某区域
        :return pol_time:某污染物在该地区每一天的含量值
        """
        data_time = []
        df = self._df[self._area.index(area)]
        for n in range(1,len(df)+1,24):
            time = date(df.at[n,'year'], df.at[n,'month'], df.at[n,'day'])  # 获得该日期                                         
            pol_mean = df[pol][n-1:n+23].mean()                             # 获得该天下污染物的均值
            data_time.append([time, pol_mean])
        pol_time = pd.DataFrame(data_time, columns=['Date', pol])           # 将时间存为时间序列索引，方便后续画图
        pol_time = pd.DataFrame(pol_time).set_index('Date')
        pol_time.index = pd.to_datetime(pol_time.index)
        return pol_time

    def space_analyze(self, pol, *time):
        """
        空间分析：某时间点北京空气质量的空间分布态势(PS:以均值代表某时间点的污染物含量)

        :param pol:污染物类型
        :param *time:某时间点，不定长列表，可以表示年月日
        :return pol_space:某污染物在某时间点各区域的含量值
        """
        data_space = []
        if len(time) == 1:
            for df in self._df:
                area = df.iloc[0,-1]
                df_year = df[df['year'] == time[0]]
                pol_mean = df_year[pol].mean()
                data_space.append([area, pol_mean])
        elif len(time) == 2:
            for df in self._df:
                area = df.iloc[0,-1]
                df_month = df[(df['year'] == time[0]) & (df['month'] == time[1])]
                pol_mean = df_month[pol].mean()
                data_space.append([area, pol_mean])
        else:
            for df in self._df:
                area = df.iloc[0,-1]
                df_day = df[(df['year'] == time[0]) & (df['month'] == time[1]) & (df['day'] == time[2])]
                pol_mean = df_day[pol].mean()
                data_space.append([area, pol_mean])
        pol_space = pd.DataFrame(data_space, columns=['Area', pol])
        pol_space = pd.DataFrame(pol_space).set_index('Area')
        return pol_space

class Data_view(Data_analyze):
    '''
    数据可视化类
    '''
    def __init__(self, dir_path):
        super().__init__(dir_path)

    def time_view(self, pol, area):
        """
        时间分析可视化：画折线图以及热力图
        """
        #画折线图
        df = super().time_analyze(pol, area)
        df_month = df.resample("M").mean()

        plt.subplot(2, 1, 1)
        df[pol].plot()
        plt.xlabel("")
        plt.ylabel(f'{pol} day average')
        plt.title(f'{pol} in {area}')

        plt.subplot(2, 1, 2)
        df_month[pol].plot()
        plt.xlabel("")
        plt.ylabel(f'{pol} month average')
        plt.show()
        
        #画热力图
        df["year"] = pd.DatetimeIndex(df.index).year
        df["month"] = pd.DatetimeIndex(df.index).month
        df_cal = df.pivot_table(index="month", columns="year", values=pol, aggfunc=np.mean)
        ax = sns.heatmap(df_cal, cmap='RdYlGn_r', robust=True, fmt='.2f', 
                 annot=True, linewidths=.5, annot_kws={'size':11}, 
                 cbar_kws={'shrink':.8, 'label':pol})
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=10)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontsize=10)
        plt.title(f'Average {pol} in {area}', fontdict={'fontsize':18}, pad=14)
        plt.show()
        
    def space_view(self, pol, *time):
        """
        空间分析可视化：画饼图以及热力图
        """
        #画饼图
        df = super().space_analyze(pol, *time)
        data_list = np.array(df[pol])
        cmap = plt.get_cmap("tab20c")
        color=cmap(range(12))
        plt.pie(data_list, colors = color, 
                labels=self._area,
                textprops = {'fontsize':7, 'color':'k'},
                autopct='%.2f%%')
        plt.title(f"Beijing {pol} distribution in {str(time)[1:][:-1]}")
        plt.show()

        #画热力图
        g = Geo(init_opts=opts.InitOpts(width='1000px', 
                                height='600px', 
                                theme=ThemeType.DARK),)
        g.add_schema(maptype='北京')
        area = ['奥体中心', '昌平', '定陵', '东四', '官园', '古城', '怀柔', '农展馆', '顺义', '天坛', '万柳', '万寿西宫']
        area_loc = [[39.985069,116.401665],
                    [40.22077,116.23128],
                    [40.286598,116.238896],
                    [39.924995,116.417679],
                    [39.932392,116.355858],
                    [39.911766,116.193359],
                    [40.316,116.63177],
                    [39.939819,116.46846],
                    [40.13012,116.65477],
                    [40.029076,116.311478],
                    [39.967056,116.296959],
                    [39.879616,116.36853]]
        for i in range(len(area)):
            # 定义坐标对应的名称，添加到坐标库中 add_coordinate(name, lng, lat)
            g.add_coordinate(area[i], area_loc[i][1], area_loc[i][0])
        # 将数据添加到地图上
        g.add(  series_name = pol,                              # 系列名称
                data_pair = list(zip(area, data_list)),         # 数据项 (坐标点名称，坐标点值)
                blur_size = 20,
                symbol_size = 15,
                type_ = ChartType.HEATMAP                       #类型选为热力图
                #type_ = ChartType.EFFECT_SCATTER
            )
        # 设置样式
        g.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        # 设置标题及分段
        g.set_global_opts(
                    visualmap_opts=opts.VisualMapOpts(max_= max(data_list), is_piecewise=True),
                    title_opts=opts.TitleOpts(title="北京空气质量分布"))
        # 渲染
        g.render(f"week7/Beijing {pol} distribution in {str(time)[1:][:-1]}.html")

class NotnumError(ValueError):
    def __init__(self,year,province,industry,type):
        self.year = year
        self.province = province
        self.industry = industry
        self.type = type
        self.message = f"the data of {province} in {year} has nan about {industry} and the type is {type}"

class NotnumberTest(Data_analyze):
    def __init__(self,path_list):
        Data_analyze.__init__(self,path_list)
        
    def read_data(self):
        doc_list = self.df_list
        year_list = self.time_list
        province_list = self.province_list
        for y in range(len(doc_list)):
            self._year = year_list[y]
            for sheet in doc_list[y]:
                if sheet != 'Sum':
                    self._province = sheet
                    df_temp = doc_list[y][sheet]
                    row_index = list(df_temp[df_temp.columns[0]])
                    col_index = list(df_temp.columns)
                    #print(col_index)
                    values = df_temp.values
                    for industry_index in range(2,len(row_index)):
                        if not pd.isnull(row_index[industry_index]):
                            self._industry = row_index[industry_index]
                            for type_index in range(1,len(col_index)-3):
                                if not pd.isnull(col_index[type_index]):
                                    self._type = col_index[type_index]
                                    if pd.isnull(values[industry_index][type_index]):
                                        raise NotnumError(self._year,self._province,self._industry,self._type)
                                    else:
                                        continue
                    #print(sheet)
        #print(len(doc_list))

def main():
    #pol_data = Data_analyze('week7/PRSA_Data_20130301-20170228')
    #pol_time = pol_data.time_analyze("PM2.5", "Aotizhongxin")
    #print(pol_time)
    #pol_area = pol_data.space_analyze("SO2", 2015)
    #pol_area = pol_data.space_analyze("SO2", 2015, 12)
    #print(pol_area)
    
    pol_data = Data_view('week7/PRSA_Data_20130301-20170228')
    #pol_data.time_view("PM2.5", "Aotizhongxin")
    pol_data.space_view("SO2", 2015, 12)

if __name__ == '__main__': main()