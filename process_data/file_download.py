import pandas as pd
import requests
from pathlib import Path
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
BASE_DIR = Path(__file__).resolve().parent.parent
BASE_FILE_DIR = BASE_DIR / 'file'

def download(r_id, row_dict):
    link_url = row_dict['字段4_复制']


    file_path = Path(link_url)
    file_extension = file_path.suffix
    file_name = f"../file/{r_id:0>4}_{row_dict['文本1']}{file_extension}"

    url = link_url

    response = requests.get(url, headers=headers)


    with open(file_name, 'wb') as f:
        f.write(response.content)


#
# my_row = {
#   "column": "【新闻资讯\n\t\t\t\t\t\t\t\t】",
#   "标题_链接": "https://sthjj.chuzhou.gov.cn/hbzx/tzgg/1104284826.html",
#   "标题": "滁州市重点排污单位视频监控联网平台运维项目招标公告",
#   "标题1": "招标公告",
#   "作者": "来源：滁州市生态环境局",
#   "时间": "发布日期：2023-03-08",
#   "信息": "项目概况 滁州市重点排污单位视频监控联网平台运维项目招标项目的潜在投标人应在 滁州市生态环境局（http://sthjj.chuzhou.gov.cn/）获取招标文件，并于2023年3月15日15点00分（北京...",
#   "searchcolumn": "所在栏目：环保资讯>通知公告",
#   "文本1": "滁州市重点排污单位视频监控联网平台运维项目招标公告",
#   "字段4": "【招标文件】滁州市重点排污单位视频监控联网平台运维项目(1).doc",
#   "字段4_复制": "https://sthjj.chuzhou.gov.cn/group4/M00/0C/82/CpYIZmQIBTaALMjZAATOhQ01gm4531.doc"
# }
#

excel_path = r"\\Tlserver\标书文件\work\word标书\滁州市\搜索-滁州市人民政府.xlsx"
link_key = '字段4_复制'


df = pd.read_excel(excel_path)
df.fillna("", inplace=True)

for row_id, row in df.iterrows():
    if row[link_key]:
        download(row_id, row)
        time.sleep(2)



print('Done')
