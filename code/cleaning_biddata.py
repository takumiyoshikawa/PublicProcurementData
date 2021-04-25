import pandas as pd
import numpy as np
import glob
import codecs
import xlrd
import openpyxl
import datetime

# functions
## add JV dummy
def JVDummy(row):
    if len(row) == 35: #If the length of the name of the bidder reaches 35, we decide he if the TokuteiJV
        return pd.Series([1,0,0])
    else:
        if any([name in row for name in TokuteiJV]):
            return pd.Series([1,0,0])
        else:
            if any([name in row for name in KeijouJV]):
                return pd.Series([0,1,0])
            else:
                if any([name in row for name in ChiikiJV]):
                    return pd.Series([0,0,1])
                else:
                    return pd.Series([0,0,0])

# winning rate
def convert_w(row):
    if row == '決定':
        return 1
    else:
        if row == '特重無効':
            return 0
        elif type(row) == str:
            return int(row)
        else:
            return int(row)

# scores
strings = [' ', '-', '－',"辞退", '入札不参加', "不参加", "無効", "予定価格超過"]
def convert_s(row):
    if row in strings:
        return float(np.nan)
    else:
        return float(row)

# dates
def Date(row):
    date = pd.to_datetime(row)
    date_series = pd.Series([date.year, date.month, date.day])
    return date_series

# paramter
## col_names
English_col_chubu_chugoku_hokkaidou_kanto_kyushu = ["OderingParty", "ConstructionName", "BidDate", "ContractDate", "ConstructionType", "BidType","ScoringDummy","BidderName", "YoteiKakaku", "KijunKakaku", "ScoredPoints", "BidFirst", "SPRationFirst", "BidSecond", "SPRationSecond", "BidThird","SPRatioThird", "EstimatedPrice","WinningIndicator"]

English_col_kinki = ["OderingParty", "ConstructionName", "BidDate", "ContractDate", "ConstructionType", "BidType","ScoringDummy","BidderName", "Address","YoteiKakaku", "KijunKakaku", "ScoredPoints", "BidFirst", "SPRationFirst", "BidSecond", "SPRationSecond", "BidThird","SPRatioThird", "EstimatedPrice","WinningIndicator"]

English_col_tohoku = ["OderingParty", "ConstructionName", "location","BidDate", "ContractDate", "ConstructionType", "BidType","ScoringDummy","BidderName", "Address","YoteiKakaku", "KijunKakaku", "ScoredPoints", "BidFirst", "SPRationFirst", "BidSecond", "SPRationSecond", "BidThird","SPRatioThird", "EstimatedPrice", "WinningRatio" ,"WinningIndicator"]

TokuteiJV = ["特定ＪＶ", "特定JV","共同企業体", "特定建設", "（共企）"]
KeijouJV = ["経常ＪＶ", "経常JV","（共）"]
ChiikiJV = ["地域維持型"]

# constrcution type
construction_type = {"一般土木" : "civilengineering", "一般土木工事" : "civilengineering","アスファルト":"asphalt","アスファルト工事":"asphalt","アスファルト舗装":"asphalt", "アスファルト舗装工事":"asphalt","鋼橋上部" : "bridge","鋼橋上部工事" : "bridge" ,"造園":"landscaping", "造園工事":"landscaping","建築":"building", "建築工事":"building","木造建築":"woodenbuilding","木造建築工事":"woodenbuilding","電気設備":"electricity","電気設備工事":"electricity" ,"暖冷房衛生設備":"airconditioning", "暖冷房衛生設備工事":"airconditioning","セメント":"cement","セメント・コンクリート工事":"cement","セメント・コンクリート舗装工事":"cement","プレストレスメント":"prestressed", "プレストレスト・コンクリ-ト":"prestressed","プレストレスト・コンクリート工事":"prestressed","法面処理":"slope","法面処理工事":"slope","塗装":"painting","塗装工事":"painting","維持修繕":"maintenance","維持修繕工事":"maintenance","しゅんせつ":"dredging", "しゅんせつ工事":"dredging","河川しゅんせつ工事":"dredging","グラウト":"grout","グラウト工事":"grout","杭打":"stakeout","さく井":"well","プレハブ建築":"prefab","プレハブ建築工事":"prefab","機械設備":"machinery","機械設備工事":"machinery","通信設備":"communication","通信設備工事":"communication","受変電設備":"substation", "受変電設備工事":"substation"}

construction_type_hokkaido = {"一般土木" : "civilengineering","一般土木工事" : "civilengineering","舗装":"asphalt","アスファルト舗装":"asphalt","アスファルト舗装工事":"asphalt" ,"鋼橋上部" : "bridge","鋼橋上部工事" : "bridge","造園":"landscaping", "造園工事":"landscaping","建築":"building","建築工事":"building","木造建築":"woodenbuilding","木造建築工事":"woodenbuilding","電気":"electricity","暖冷房衛生設備":"airconditioning", "暖冷房衛生設備工事":"airconditioning","セメント":"cement","セメント・コンクリート工事":"cement", "セメント・コンクリート舗装工事":"cement", "PSコンクリート":"prestressed","プレストレスト・コンクリ-ト":"prestressed","ＰＳコンクリート":"prestressed" ,"法面処理":"slope","法面処理工事":"slope","塗装":"painting","塗装工事":"painting","維持":"maintenance","しゅんせつ":"dredging","河川しゅんせつ工事":"dredging","しゅんせつ工事":"dredging","グラウト":"grout","グラウト工事":"grout","杭打":"stakeout","さく井":"well","プレハブ建築":"prefab","プレハブ建築工事":"prefab","機械装置":"machinery","機械設備工事":"machinery","通信設備":"communication","通信設備工事":"communication","受変電設備":"substation", "受変電設備工事":"substation","管":"pipe","防水加工":"waterproof", "その他":"others"}

regions = ["chubu", "chugoku", "hokkaido", "kanto", "kinki", "kyushu", "tohoku"]
skips = [5, 6, 6, 6, 4, 2, 5]
col_names = [English_col_chubu_chugoku_hokkaidou_kanto_kyushu, English_col_chubu_chugoku_hokkaidou_kanto_kyushu, English_col_chubu_chugoku_hokkaidou_kanto_kyushu, English_col_chubu_chugoku_hokkaidou_kanto_kyushu, English_col_kinki, English_col_chubu_chugoku_hokkaidou_kanto_kyushu, English_col_tohoku]

# main
for t,region in enumerate(regions):
    all_files=glob.glob(f"data/{region}/bid/*/{region}_construction_*")
    for file in all_files:
        df = pd.read_excel(file, skiprows = skips[t])
        df.columns = col_names[t]
        df = df[English_col_chubu_chugoku_hokkaidou_kanto_kyushu]
        df["region"] = region
        # drop nan name
        df = df[~df["OderingParty"].isnull()]
        df = df[~df["ConstructionName"].isnull()]
        # construction_type
        if region == "hokkaido":
            df["ConstructionType"] = df["ConstructionType"].replace(construction_type_hokkaido)
        else:
            df["ConstructionType"] = df["ConstructionType"].replace(construction_type)
        # JV
        df[["TokuteiJV", "KeijouJV", "ChiikiJV"]] = df["BidderName"].apply(JVDummy)
        df["JV"] = df["TokuteiJV"] + df["KeijouJV"] + df["ChiikiJV"]
        # winning
        df["WinningIndicator"]=df["WinningIndicator"].replace("落札", 1)
        df["WinningIndicator"]=df["WinningIndicator"].fillna(0)
        df["WinningIndicator"] = df["WinningIndicator"].apply(convert_w)
        # ScoredPoints
        df["ScoredPoints"] = df["ScoredPoints"].apply(convert_s)
        df["SPRationFirst"] = df["SPRationFirst"].apply(convert_s)
        df["BidFirst"] = df["BidFirst"].apply(convert_s)
        df["SPRationSecond"] = df["SPRationSecond"].apply(convert_s)
        df["BidSecond"] = df["BidSecond"].apply(convert_s)
        df["SPRatioThird"] = df["SPRatioThird"].apply(convert_s)
        df["BidThird"] = df["BidThird"].apply(convert_s)
        # date
        df[["BidYear", "BidMonth", "BidDay"]] = df["BidDate"].apply(Date)
        # drop
        df.drop("EstimatedPrice", axis=1)
        if t == 0:
            df_old = df
        else:
            df_old = pd.concat([df_old, df])

df = df_old
df.to_csv("data/all_data.csv", encoding ="cp932")