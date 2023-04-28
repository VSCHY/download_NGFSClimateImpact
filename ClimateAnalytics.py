import pandas as pd
import requests
import numpy as np
import ast
import tqdm

def import_df(name):
    dire = "metadata/"
    dfile = dire +  name + ".xlsx"
    df = pd.read_excel(dfile)
    df = df.set_index("id")
    return df
    

class NGFSClimateImpact:
    def __init__(self, download = False):
        
        if download:
            self.download_metadata()
        self.countries = import_df("countries")
        self.iso_countries = self.countries.index.to_list()

        self.country_groups = import_df("country_groups")
        self.scenarios = import_df("scenarios")
        self.scenarios_list = self.scenarios.index.to_list()
        

        self.spatial_weightings = import_df("spatial_weightings")
        self.temporal_averagings = import_df("temporal_averagings")
        self.units = import_df("units")
        self.variable_groups = import_df("variable_groups")
        self.vars = import_df("vars")

        self.get_groups()
    
    def download_metadata(self):
        data = requests.get('https://cie-api.climateanalytics.org/api/meta/').json()
        for k in data.keys():
            df = pd.DataFrame.from_dict(data[k])
            if k == "countries":
                df["large"] = df["large"].astype(np.int8)
            elif k == "scenarios":
                df["basescenario"] = df["basescenario"].astype(np.int8)
                df["primary"] = df["primary"].astype(np.int8)
            df.to_excel("metadata/"+k+".xlsx", index = False)

    def download_variables(self, vars, season = "annual", agg = "other" ):
        #for i, iso in enumerate(self.iso_countries):
        for i, iso in tqdm.tqdm(enumerate(self.iso_countries), total=len(self.iso_countries)):
            for j, scenar in enumerate(self.scenarios_list):
                URL = self.get_url(iso = iso, scenar = scenar, reg = iso, vars = vars, season = season, agg = agg)
                data = requests.get(URL).json()
                df = pd.DataFrame.from_dict(data)
                df["Country"] = iso
                df["Scenario"] = scenar
                df["Variable"] = vars
                df["Variable name"] = self.vars.loc[vars]["name"]
                df["Unit"] = self.vars.loc[vars]["unit"]
                df["Variable Group"] = self.D_correspondance_var[vars]
                if iso != "GLOBAL":
                    df["Country Group"] = self.D_region_countries[iso]
                else:
                    df["Country Group"] = "GLOBAL"
                if (i+j) == 0:
                    d_out = df
                else:
                    d_out = pd.concat([df, d_out], axis = 0)
        return d_out

    def get_groups(self,):
        gg  = self.variable_groups["children"].to_dict()
        gg2 = {gk: ast.literal_eval(gg[gk]) for gk in gg.keys()}

        D = {}
        for vn in self.vars.index:
            for gk in gg2.keys():
                if vn in gg2[gk]:
                    D[vn] = gk
                    break
        self.D_correspondance_var = D

        gg  = self.country_groups["children"].to_dict()
        gg2 = {gk: ast.literal_eval(gg[gk]) for gk in gg.keys()}
        D = {}
        for vn in self.countries.index:
            for gk in gg2.keys():
                if vn in gg2[gk]:
                    D[vn] = gk
                    break
        self.D_region_countries = D
        

    def get_url(self, iso, scenar,vars,season, agg, format = "json",  reg = None):
        if reg is None:
            reg = iso
        URL = f'https://cie-api.climateanalytics.org/api/timeseries/?iso={iso}&region={reg}&scenario={scenar}&'
        URL += f'var={vars}&season={season}&aggregation_spatial={agg}&format={format}'
        return URL



