# -*- coding: utf-8 -*-

import urllib.request
import yaml
import pandas as pd


def TXTfromURL(src):
    response = urllib.request.urlopen(src)
    data = response.read()
    return data.decode('utf-8')

def ValuefromYAMLFile(src, index, key):
    with open(src, "r") as fr:
        dataMap = yaml.load(fr)
        print(dataMap[index][key])
        
def WriteYAML(src):
    with open("output.yaml", "w") as fw:
        #fw.write(yaml.dump(src, default_flow_style=False))
        print(yaml.dump(src, default_flow_style=False))

def DFfromYAML(src):
    dataMap = yaml.load(src)
    return pd.DataFrame(dataMap)


url = "https://raw.githubusercontent.com/gitllama/Python/master/Yaml/music.yaml"

data = TXTfromURL(url)
print(data)

df = DFfromYAML(data)

WriteYAML(df)

df = df[df["artist"] == "くるり"]
print(df[["artist","date"]])
