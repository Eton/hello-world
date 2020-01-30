import pandas as pd
import matplotlib.pyplot as plt
import glob
from matplotlib.font_manager import FontProperties
import numpy as np

if __name__ == "__main__":

    path = 'C:/Users/eton/Desktop/tainan/data/'

    csv_lst = glob.glob(path + "*.csv")

    df = None

    try:

        for filename in csv_lst:

            if df is None:

                df = pd.read_csv(filename)
                df = df.iloc[1:]

            else:

                df_tmp = pd.read_csv(filename)
                df_tmp = df_tmp.iloc[1:]
                df = pd.concat([df, df_tmp])

    except Exception as e:

        print(e)

    # 過濾房地 & 區域 & 

    df = df[(df['交易標的'] == '房地(土地+建物)') & \
    (df['鄉鎮市區'] == '安南區') & \
    (df['土地區段位置建物區段門牌'].str.contains('安和路一段')) & \
    (df['都市土地使用分區'].str.contains('住')) & \
    (df['建物型態'].str.contains('透天厝'))]

    df = df[['鄉鎮市區', '交易年月日', '總價元', '單價元平方公尺', '建築完成年月']]

    df['交易年月日'] = df['交易年月日'].str[:3].astype(int)

    df['屋齡'] = df['交易年月日'] - df['建築完成年月'].str[:3].replace('0','').astype(int)

    df = df[(df['屋齡'] >= 30) & (df['交易年月日'] >= 107)]

    df['單價元平方公尺'] = df['單價元平方公尺'].astype(int) / 0.3025

    df['yymm'] = df['交易年月日'].apply(lambda x: (str(x)[:5]).replace('.', '0'))

    groups = df.groupby('yymm')

    key = {}

    x = {}

    for name, group in groups:

        if name[:2] != '10':
            continue

        key[name] = format(int(group['單價每平方公尺'].sum() / len(group) * 3.3058), ',')
        x[name] = len(group)

    date = [k for k in sorted(key.keys())]
    value = [key[k] for k in sorted(key.keys())]

    x_date = [k for k in sorted(x.keys())]
    x_value = [x[k] for k in sorted(x.keys())]

    value_tuples = [tuple([k, key[k]]) for k in sorted(key.keys())]

    x_value_tuples = [tuple([k, x[k]]) for k in sorted(x.keys())]

    # plt.plot(date, value, marker='o')

    # plt.hist(x_value_tuples)

    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
    # plt.title('台南市每坪價格 單位(元)', fontproperties=font)

    fig = plt.figure()

    ax1 = fig.add_subplot(111)
    ax1.plot(date, value, marker='o')
    ax1.set_ylabel('每坪價格(元)', fontproperties=font)
    # ax1.set_ylim((100000, 210000))
    # new_ticks = np.linspace(100000, 210000, 10)
    # ax1.set_title('台南市每坪價格 單位(元)', fontproperties=font)

    # ax2 = ax1.twinx()  # this is the important function
    # ax2.set_xlim(['100','108'])
    # ax2.plot(date, x_value, 'r')
    # ax2.hist(x_value)
    # ax2.set_xlim(['100','108'])
    # ax2.plot(x_value_tuples, 'r')
    # ax2.set_xlim([0, np.e])
    # ax2.set_ylabel('交易量(次)', fontproperties=font)
    # ax2.set_xlabel('Same X for both exp(-x) and ln(x)')


    for t in value_tuples:

        ax1.annotate(
            "%s" % t[1], xy=t, xytext=(-20, 10), textcoords='offset points')

    plt.xticks(rotation=45)
    plt.show()

    # fig1 = plt.figure(figsize=(25, 5))
    # plt.xticks(range(len(key)), tuple(date), rotation=45)
    # plt.title('122')
    # plt.plot(value, 'o-')

    # plt.annotate(
    #         "1231213",
    #         xy=(113422, 113422),
    #         xytext=(-20, 10),
    #         textcoords='offset points')

    # # for v in value:
    # #     plt.annotate(
    # #         "1231213",
    # #         xy=(int(v), int(v)),
    # #         xytext=(-20, 10),
    # #         textcoords='offset points')

    # plt.show()

    # x = np.arange(0., np.e, 0.01)
    # y1 = np.exp(-x)
    # y2 = np.log(x)
    # fig = plt.figure()
    # ax1 = fig.add_subplot(111)
    # ax1.plot(x, y1)
    # ax1.set_ylabel('Y values for exp(-x)')
    # ax1.set_title("Double Y axis")
    # ax2 = ax1.twinx()  # this is the important function
    # ax2.plot(x, y2, 'r')
    # ax2.set_xlim([0, np.e])
    # ax2.set_ylabel('Y values for ln(x)')
    # ax2.set_xlabel('Same X for both exp(-x) and ln(x)')
    # plt.show()
