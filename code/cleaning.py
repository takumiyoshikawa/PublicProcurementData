import pandas as pd
import bs4
import pathlib
import re
import jaconv

colname = [['firm_name','ceo_name', 'firm_address', 'firm_id'], 
           ['civilengineering_qualification', 'civilengineering_rank', 'civilengineering_exception', 'civilengineering_financial_score', 'civilengineering_technical_score', 'civilengineering_total_score'],
           ['asphalt_qualification', 'asphalt_rank', 'asphalt_exception', 'asphalt_financial_score', 'asphalt_technical_score', 'asphalt_total_score'],
           ['bridge_qualification', 'bridge_rank', 'bridge_exception', 'bridge_financial_score', 'bridge_technical_score', 'bridge_total_score'],
           ['landscaping_qualification', 'landscaping_rank', 'landscaping_exception', 'landscaping_financial_score', 'landscaping_technical_score', 'landscaping_total_score'],
           ['builiding_qualification', 'builiding_rank', 'builiding_exception', 'builiding_financial_score', 'builiding_technical_score', 'builiding_total_score'],
           ['woodenbuiliding_qualification', 'woodenbuiliding_rank', 'woodenbuiliding_exception', 'woodenbuiliding_financial_score', 'woodenbuiliding_technical_score', 'woodenbuiliding_total_score'],
           ['electricity_qualification', 'electricity_rank', 'electricity_exception', 'electricity_financial_score', 'electricity_technical_score', 'electricity_total_score'],
           ['airconditioning_qualification', 'airconditioning_rank', 'airconditioning_exception', 'airconditioning_financial_score', 'airconditioning_technical_score', 'airconditioning_total_score'],
           ['cement_qualification', 'cement_rank', 'cement_exception', 'cement_financial_score', 'cement_technical_score', 'cement_total_score'],
           ['prestressed_qualification', 'prestressed_rank', 'prestressed_exception', 'prestressed_financial_score', 'prestressed_technical_score', 'prestressed_total_score'],
           ['slope_qualification', 'slope_rank', 'slope_exception', 'slope_financial_score', 'slope_technical_score', 'slope_total_score'],
           ['painting_qualification', 'painting_rank', 'painting_exception', 'painting_financial_score', 'painting_technical_score', 'painting_total_score'],
           ['maintenance_qualification', 'maintenance_rank', 'maintenance_exception', 'maintenance_financial_score', 'maintenance_technical_score', 'maintenance_total_score'],
           ['dredging_qualification', 'dredging_rank', 'dredging_exception', 'dredging_financial_score', 'dredging_technical_score', 'dredging_total_score'],
           ['grout_qualification', 'grout_rank', 'grout_exception', 'grout_financial_score', 'grout_technical_score', 'grout_total_score'],
           ['stakeout_qualification', 'stakeout_rank', 'stakeout_exception', 'stakeout_financial_score', 'stakeout_technical_score', 'stakeout_total_score'],
           ['well_qualification', 'well_rank', 'well_exception', 'well_financial_score', 'well_technical_score', 'well_total_score'],
           ['prefab_qualification', 'prefab_rank', 'prefab_exception', 'prefab_financial_score', 'prefab_technical_score', 'prefab_total_score'],
           ['machinery_qualification', 'machinery_rank', 'machinery_exception', 'machinery_financial_score', 'machinery_technical_score', 'machinery_total_score'],
           ['communication_qualification', 'communication_rank', 'communication_exception', 'communication_financial_score', 'communication_technical_score', 'communication_total_score'],
           ['substation_qualification', 'substation_rank', 'substation_exception', 'substation_financial_score', 'substation_technical_score', 'substation_total_score'],
           ['date']]

# For Hokkaido

# colname = [['firm_name','ceo_name', 'firm_address', 'firm_id'], 
#            ['civilengineering_qualification', 'civilengineering_rank', 'civilengineering_exception', 'civilengineering_financial_score', 'civilengineering_technical_score', 'civilengineering_total_score'],
#            ['builiding_qualification', 'builiding_rank', 'builiding_exception', 'builiding_financial_score', 'builiding_technical_score', 'builiding_total_score'],
#            ['asphalt_qualification', 'asphalt_rank', 'asphalt_exception', 'asphalt_financial_score', 'asphalt_technical_score', 'asphalt_total_score'],
#            ['bridge_qualification', 'bridge_rank', 'bridge_exception', 'bridge_financial_score', 'bridge_technical_score', 'bridge_total_score'],
#            ['prestressed_qualification', 'prestressed_rank', 'prestressed_exception', 'prestressed_financial_score', 'prestressed_technical_score', 'prestressed_total_score'],
#            ['dredging_qualification', 'dredging_rank', 'dredging_exception', 'dredging_financial_score', 'dredging_technical_score', 'dredging_total_score'],
#            ['machinery_qualification', 'machinery_rank', 'machinery_exception', 'machinery_financial_score', 'machinery_technical_score', 'machinery_total_score'],
#            ['pipe_qualification', 'pipe_rank', 'pipe_exception', 'pipe_financial_score', 'pipe_technical_score', 'pipe_total_score'],
#            ['electricity_qualification', 'electricity_rank', 'electricity_exception', 'electricity_financial_score', 'electricity_technical_score', 'electricity_total_score'],
#            ['painting_qualification', 'painting_rank', 'painting_exception', 'painting_financial_score', 'painting_technical_score', 'painting_total_score'],
#            ['landscaping_qualification', 'landscaping_rank', 'landscaping_exception', 'landscaping_financial_score', 'landscaping_technical_score', 'landscaping_total_score'],
#            ['waterproof_qualification', 'waterproof_rank', 'waterproof_exception', 'waterproof_financial_score', 'waterproof_technical_score', 'waterproof_total_score'],
#            ['grout_qualification', 'grout_rank', 'grout_exception', 'grout_financial_score', 'grout_technical_score', 'grout_total_score'],
#            ['well_qualification', 'well_rank', 'well_exception', 'well_financial_score', 'well_technical_score', 'well_total_score'],
#            ['maintenance_qualification', 'maintenance_rank', 'maintenance_exception', 'maintenance_financial_score', 'maintenance_technical_score', 'maintenance_total_score'],
#            ['others_qualification', 'others_rank', 'others_exception', 'others_financial_score', 'others_technical_score', 'others_total_score'],
#            ['date']]


def clean_html(filename):
    html = open(filename,  encoding="cp932").read()
    soup = bs4.BeautifulSoup(html, "html.parser")
    table = soup.find("div")
    firm_list = table.find_all("tr")

    df = pd.DataFrame(columns = sum(colname, []))
    for firm in firm_list:
        firm = firm.select("font")
        if len(firm) < 1:
        	continue

        # exception : append JV flag 
        if (not re.search( '（共）', list(firm[0].strings)[0]) == None) and len(list(firm[0].strings)) == 3:
            temp = list(firm[0].strings) + ["JV"]
            firm_data = pd.Series(temp, index = colname[0])
        # exception : not having firm_id
        elif len(list(firm[0].strings)) == 3:
            temp = list(firm[0].strings) + [""]
            firm_data = pd.Series(temp, index = colname[0])
        else:
            firm_data = pd.Series(firm[0].strings, index = colname[0])
        
        # make df
        for i in range(1, len(firm)):
            temp = [str(content) for content in firm[i].contents]
            
            if len(temp) <= 1:
                temp = ["", "", "", "", "", ""]
                firm_ind =  pd.Series(temp, index = colname[i])
            else:
                # zenkaku to hankaku
                temp = [jaconv.z2h(c, digit = True, ascii = True) for c in temp]
                firm_ind = pd.Series("".join(temp).split("<br/>"), index = colname[i])
            
            firm_data = pd.concat([firm_data, firm_ind])
            
        date = pd.Series(filename.split("/")[-2], index=colname[-1])
        firm_data = pd.concat([firm_data, date])
        df = df.append(firm_data, ignore_index=True)
    print(df)
    return df


def list_all_files(directory, extension=None, size=None, sort=False):
    if extension is not None and extension[0] != ".":
        extension = "." + extension
    
    directory = pathlib.Path(directory)

    path_list = []
    files = directory.glob("**/*")

    if size is None:
        for file in files:
            if file.is_file() and (extension is None or file.suffix == extension):
                path_list.append(str(file))
    else:
        for i, obj in enumerate(files):
            if len(path_list) >= size:
                break
            
            if file.is_file() and (extension is None or file.suffix == extension):
                path_list.append(str(file))

    if sort:
        path_list.sort()

    return path_list
    
def make_panel(file_list):
    if file_list == None:
        print("ValueError : file_list is None")

    else:
        panel_df = pd.DataFrame(columns= sum(colname, []))
        for file in file_list:
            df = clean_html(file)
            panel_df = panel_df.append(df, ignore_index=True)
            panel_df = panel_df[~panel_df[['firm_name', 'date']].duplicated()]
           
            
        return panel_df
    
def make_csv(file_list, directory):
    panel_df = make_panel(file_list)
    panel_df.to_csv(directory, encoding='utf_8_sig')

def get_input_directory(region, business_category, date):
    path = pathlib.Path(__file__).resolve()
    directory = str(path.parent.parent) + "/data/" + region + "/qualification/" + business_category + "/" + date

    return directory


def set_output_directory(region, business_category, date):
    path = pathlib.Path(__file__).resolve()
    # make output directory
    path_dir = pathlib.Path(str(path.parent.parent) + "/data/" + region)
    pathlib.Path.mkdir(path_dir, exist_ok = True, parents=True)
    # file name
    directory = str(path.parent.parent) + "/data/" + region + "/qualification/" + region + "_" + business_category + "_" + date + ".csv"
    
    return directory



if __name__ == "__main__":

    region = 'kanto'
    business_category = "construction"
    dates = ["20200501"]

    for date in dates:
      output_directory = set_output_directory(region, business_category, date)
      file_list = list_all_files(get_input_directory(region, business_category, date), extension= 'html', sort = True)
      make_csv(file_list, output_directory)




