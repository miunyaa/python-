import csv
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定使用宋体

url = 'https://movie.douban.com/j/chart/top_list'
start = 0
limit = 100
param = {
    'type': '24',
    'interval_id': '100:90',
    'action': '',
    'start': start,
    'limit': limit
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62'
}
response = requests.get(url=url, params=param, headers=headers)
list_data = response.json()

f = open('./豆瓣.csv', 'w', encoding='utf-8-sig', newline='')
csv_write = csv.DictWriter(f, fieldnames=[
    '电影名',
    '主演人数',
    '主演',
    '评分',
    '上映时间',
    '类型',
    '评论数',
    '拍摄国家'
])
csv_write.writeheader()

for i in list_data:
    dic = {
        '电影名': i['title'],
        '主演人数': i['actor_count'],
        '主演': i['actors'],
        '评分': i['score'],
        '上映时间': i['release_date'],
        '类型': i['types'],
        '评论数': i['vote_count'],
        '拍摄国家': i['regions']
    }
    csv_write.writerow(dic)

# 读取 csv 文件
df = pd.read_csv('./豆瓣.csv')

# 统计电影类型数量
type_count = df['类型'].value_counts()

# 分析各个国家发布的电影数量占比
# 统计电影拍摄国家数量
regions_count = df['拍摄国家'].value_counts()
# 计算各个国家的电影数量占比
regions_prop = regions_count / regions_count.sum()
# 绘制电影拍摄国家数量占比饼图
plt.figure(figsize=(8, 8))
plt.pie(regions_prop.values, labels=regions_prop.index, autopct='%1.1f%%', startangle=90)
plt.title('豆瓣电影Top100电影拍摄国家数量占比图')
plt.axis('equal')



# 计算各个类型的电影数量占比
type_prop = type_count / type_count.sum()

# 绘制电影类型数量占比饼图
plt.figure(figsize=(8, 8))
plt.pie(type_prop.values, labels=type_prop.index, autopct='%1.1f%%', startangle=90)
plt.title('豆瓣电影Top100电影类型数量占比图')
plt.axis('equal')

# 统计电影评分分布
plt.figure(figsize=(10, 5))
sns.histplot(df['评分'], bins=20)
plt.title('豆瓣电影Top100电影评分分布图')
plt.xlabel('电影评分')
plt.ylabel('电影数量')

# 统计电影拍摄国家数量
regions_count = df['拍摄国家'].value_counts()

# 绘制电影拍摄国家数量柱状图
plt.figure(figsize=(10, 5))
plt.bar(regions_count.index, regions_count.values)
plt.title('豆瓣电影Top100电影拍摄国家数量分布图')
plt.xlabel('电影拍摄国家')
plt.ylabel('电影数量')
plt.xticks(rotation=45)

# 统计主演人数最多的前十个影片
top_10_actors = df.nlargest(10, '主演人数')
plt.figure(figsize=(10, 5))
plt.bar(top_10_actors['电影名'], top_10_actors['主演人数'])
plt.title('豆瓣电影Top100主演人数最多的前十个影片')
plt.xlabel('电影名')
plt.ylabel('主演人数')
plt.xticks(rotation=45)

# 计算各个国家的电影平均评分
avg_score_by_region = df.groupby('拍摄国家')['评分'].mean().sort_values(ascending=False)

# 统计平均评分最高的前十个国家
top_10_regions = avg_score_by_region.nlargest(10)

plt.figure(figsize=(10, 5))
plt.bar(top_10_regions.index, top_10_regions.values)
plt.title('豆瓣电影Top100平均评分最高的前十个国家')
plt.xlabel('国家')
plt.ylabel('平均评分')
plt.xticks(rotation=45)

# 显示所有图表
plt.show()




