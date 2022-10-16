import os
import pandas as pd

class Data_analyze:
    '''
    数据分析类
    '''
    def __init__(self, dir_path):
        """
        数据的读取
        """
        self._df = []                                           # 每个csv文件按df格式储存进列表

        #存一些基本的数据信息，便于后续报错
        self._area = ["Aotizhongxin","Changping","Dingling","Dongsi","Guanyuan","Gucheng","Huairou","Nongzhanguan","Shunyi","Tiantan","Wanliu","Wanshouxigong"]
        self._time = ["2013.03.01", "2017.02.28"]
        self._pollutant = ["PM2.5","PM10","SO2","NO2","CO","O3"]
        self._climate = ["TEMP","PRES","DEWP","RAIN","wd","WSPM"]

        print("-----数据读取中，请稍后-----")
        files = os.listdir(dir_path)                            # 获取目录下所有的文件
        for path in files:
            with open(dir_path + "/" + path) as f:
                df = pd.read_csv(f)
                self._df.append(df)
        print("-----数据读取完成-----")

    def time_analyze(self, area, pol):
        """
        时间分析：某区域某类型污染物随时间的变化
        PS:以天为最小精度统计数据
        """
        df = self._df[self._area.index(area)]
        year = ndf['year']

        return self.time_data_list


    def space_analyze(self,year,co2_type):
        """
        空间分析：某时间点或时间段北京空气质量的空间分布态势
        """
        df_space = self.df_list[self.time_list.index(year)]['Sum']
        #print(df_space)
        self.space_data_list = []
        province_list = list(df_space[df_space.columns[0]])
        for i in range(len(province_list)):
            data = df_space.loc[i, co2_type]
            self.space_data_list.append(data)

        print(f'年份：{year}  碳排放量类型：{co2_type}')
        for i in range(0,len(province_list)-2):
            print(f'省份：{province_list[i]}  排放量：{self.space_data_list[i]}')
        print(f'总计：{province_list[len(province_list)-1]}  排放量：{self.space_data_list[len(province_list)-1]}')

        return self.space_data_list[0:-2]

class Data_view(Data_analyze):
    '''
    数据可视化类
    '''
    def __init__(self, dir_path):
        super().__init__(self, dir_path)

    def time_view(self):
        time_list = self.time_list
        for i in self.province_list:
            time_data_list = self.time_analyze(i,'Total')
            #print(time_data_list)
            plt.figure(figsize=(20,6.5))
            plt.bar(range(len(time_list)),time_data_list,tick_label = time_list,color = 'violet')
            plt.xlabel('年份')
            plt.ylabel(i+' Co2 排放量')
            plt.savefig('figure/'+i+'_total.png')

    def space_view(self):
        province_list = self.province_list
        space_data_list = np.array(self.space_analyze('1997','Total'))
        plt.pie(space_data_list,
                labels=province_list,
                autopct='%.2f%%'
                )
        plt.title("Beijing Co2 排放量 总体占比情况")
        plt.show()

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
    data = Data_analyze('week7/PRSA_Data_20130301-20170228')
    

if __name__ == '__main__': main()