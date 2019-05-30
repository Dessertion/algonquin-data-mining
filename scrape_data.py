from itertools import chain
from itertools import repeat

import json
import re
import collections

class Thing:
    
    def getInfoLength(self):
        raise NotImplementedError

    @staticmethod
    def getMeta():
        raise NotImplementedError

    @staticmethod
    def getThing(string,meta):
        for s in Thing.__subclasses__():
            if s.getMeta() == meta:
                return s(string)
        return None

    def __init__(self,string):
        self.info = dict(zip(self.getInfoLength().keys(),("" for _ in self.getInfoLength().keys())))
        counter = 0
        for key,val in self.getInfoLength().items():
            x = string[counter:counter+val]
            if "@" not in x:
                self.info[key] = string[counter:counter+val]
            else:
                self.info[key] = ""
            counter+=val

    def __repr__(self):
        return str(self.info)

    def getInfo(self):
        return self.info


class Mammal(Thing):
    def getInfoLength(self):
        return {"MML_ID":2,
        "MML_ACT":1,
        "MML_LOC":1,
        "MML_EVD":1}
    
    @staticmethod
    def getMeta():
        return 0
    
    def __init__(self,string):
        Thing.__init__(self,string)    

class Bird(Thing):

    def getInfoLength(self):
        return {
        "BIRD_ID":2,
        "BIRD_ACT":1,
        "BIRD_LOC":1,
        "BIRD_DIS":1}

    @staticmethod
    def getMeta():
        return 1

    def __init__(self,string):
        Thing.__init__(self,string)
             
class Tree(Thing):
    def getInfoLength(self):
        return {
        "TREE_ID":2,
        "TREE_PCT":1,
        "TREE_DIA":2,
        "TREE_HT":2,
        "TREE_DEN":2
    }

    @staticmethod
    def getMeta():
        return 2

    def __init__(self,string):
        Thing.__init__(self,string)

class Rock(Thing):
    def getInfoLength(self):
        return {"SIM":1,
        "AVG_SIZE":2,
        "FW":1,
        "FF":1,
        "CVR":1,
        "ERSN":1,
        "SHP":1,
        "B_FIELD":2}
    
    @staticmethod
    def getMeta():
        return 3

    def __init__(self,string):
        Thing.__init__(self,string)
             

class SSRF:
    INFO = {
        "AP": 2,
        "GTS":3,
        "PG":1,
        "LST":4,
        "CC":1,
        "CT":1,
        "PRECIP":1,
        "WS":1,
        "WD":1,
        "LAND_HAB":2,
        "WATER_HAB":2,
        "SAT_HOG":2, # no clue wtf this stands for lol
        "SAT_SUN":3,
        "SAT_SHA":3,
        "SWT":3,
        "HYPRO":3,
        "STSL":3,
        "STSH":3,
        "SCDT":1,
        "CST":1,
        "STK":1,
        "RBN":1,
        "SHN":1,
        "TDS":3,
        "TUR":3,
        "ALB":2,
        "DELTA":2,
        "WCD":2,
        "WCV":2,
        "WIDTH":3,
        "IMG":4,
        "PAN_IMGS":2,
        "JOB":1,
        #now for page 2
        "ROCK":(3,10),
        "TREE":(2,9),
        "BIRD":(1,5),
        "MAMMAL":(0,5),
        "NULL":1,
        "NEXT":1
    }

    #super disgusting but idgaf
    ORDER = list(chain(["AP","GTS","PG","LST","CC","CT","PRECIP","WS","WD","NEXT","LAND_HAB","SAT_HOG","SAT_SUN","SAT_SHA"],
    ["SWT"]*2,["HYPRO"]*3,["SCDT"],["HYPRO"]*2,["STSL"]*6,["CST","STK"],["STSH"]*6,["NULL"]*6,["RBN","SHN"],["NULL"]*4,["WATER_HAB"],
    ["TDS"]*2,["TUR"]*2,["IMG"]*2,["ALB"]*10,["PAN_IMGS","IMG","DELTA"],["WCD"]*10,["WCV"]*10,["WIDTH"]*2,["IMG"]*5,["JOB"]*10,["IMG"]*6,["NEXT"]))

    IONS = ["DO","PH","N3","N2","NH","PO","CH","HD","AK","SP"]

    def __init__(self, filepath, debug=False):
        self.parsed_data = dict(zip(SSRF.INFO.keys(), ([] for _ in SSRF.INFO.keys())))
        del self.parsed_data["NULL"]; del self.parsed_data["NEXT"]
        self.debug = debug
        self.filepath = filepath

        ap = re.search(r"\d+",filepath)
        if not ap:
            print(filepath)
        else: ap = ap.group()
        if int(ap) <= 12:
            x = list(chain(["NULL"]*10,["TREE","BIRD","MAMMAL"]))*8
            self.order = self.ORDER+  ["ROCK","NEXT"] + x
        else:
            self.order = self.ORDER+ ["AP","GTS","PG","NEXT"] + list(chain(["ROCK","TREE",
    "BIRD","MAMMAL"]*9))  

        self.mapped_info = list(map(lambda x : self.INFO[x], self.order))
        #print(self.order)
        self.read()

    def read(self):
        with open(self.filepath,"r") as f:
            self.data = f.read().splitlines()
            itm = 0
            null = False
            linen = 0
            for line in self.data:
                number = ""
                count = 0
                linen+=1
                if line[0] == '~':
                    break
                for char in line:
                    number+=char
                    count+=1

                    if self.debug and self.order[itm] == "CST":
                        breakpoint()

                    if self.order[itm] == "NULL":
                        number = ""
                        count = 0
                        itm+=1
                        null = True
                        continue
                    else:
                        null = False

                    if self.order[itm] == "NEXT":
                        itm+=1
                        break
                    if char == "@":
                        if type(self.mapped_info[itm]) == tuple:
                            if count>=self.mapped_info[itm][1]:
                                itm+=1 
                                count = 0
                                number =""  
                        elif count>= self.mapped_info[itm]:
                            itm+=1
                            count =0
                            number = ""
                        continue
                    if type(self.mapped_info[itm]) == tuple:
                        if count >= self.mapped_info[itm][1]:
                            if self.debug:
                                print(self.order[itm])
                            if number.replace("0","").strip():
                                self.parsed_data[self.order[itm]].append(Thing.getThing(number,self.mapped_info[itm][0]))
                            count = 0
                            itm+=1
                            number=""
                    elif count >= self.mapped_info[itm]:
                        if self.debug:
                            print(self.order[itm])
                        s = self.order[itm]
                        self.parsed_data[s].append(number)
                        count = 0
                        itm+=1
                        number=""
        ions = {}
        linen0 = linen+1
        while linen < len(self.data)-1:
            linen+=1
            #print(str(linen) + " " + self.data[linen])
            ions[SSRF.IONS[linen-linen0]] = self.data[linen]
        
        self.parsed_data.update(ions)
                
    def lol(self):
        return self.parsed_data

    
    def toJSON(self):
        ret = self.parsed_data
        for key,value in ret.items():
            if type(value) == list and value:
                if issubclass(type(value[0]),Thing):
                    ret[key] = list(x.getInfo() for x in value)
        return json.dumps(ret)

a = SSRF("./new/10-121.dat")
print(a.toJSON())