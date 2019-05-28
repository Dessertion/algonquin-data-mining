from itertools import chain

class Obj:
    
    def getInfo(self):
        raise NotImplementedError

    def getMeta(self):
        raise NotImplementedError

    @staticmethod
    def getThing(string,meta):
        for s in Obj.__subclasses__():
            if s.getMeta() == meta:
                return s(string)
        return None

    def __init__(self,string):
        self.info = dict(zip(self.getInfo().keys(),""*len(self.getInfo().keys())))
        counter = 0
        for key,val in self.getInfo():
            self.info[key] = string[counter:counter+val]
            counter+=val

class Mammal(Obj):
    def getInfo(self):
        return {"MML_ID":2,
        "MML_ACT":1,
        "MML_LOC":1,
        "MML_EVD":1}
    
    def getMeta(self):
        return 0
    
    def __init__(self,string):
        Obj.__init__(self,string)    

class Bird(Obj):

    def getInfo(self):
        return {
        "BIRD_ID":2,
        "BIRD_ACT":1,
        "BIRD_LOC":1,
        "BIRD_DIS":1}

    def getMeta(self):
        return 1

    def __init__(self,string):
        Obj.__init__(self,string)
             
class Tree(Obj):
    def getInfo(self):
        return {
        "TREE_ID":2,
        "TREE_PCT":1,
        "TREE_DIA":2,
        "TREE_HT":2,
        "TREE_DEN":2
    }

    def getMeta(self):
        return 2

    def __init__(self,string):
        Obj.__init__(self,string)

class Rock(Obj):
    def getInfo(self):
        return {"SIM":1,
        "AVG_SIZE":2,
        "FW":1,
        "FF":1,
        "CVR":1,
        "ERSN":1,
        "SHP":1}
    
    def getMeta(self):
        return 3

    def __init__(self,string):
        Obj.__init__(self,string)
             

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
        "ROCK":(3,8),
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

    ORDER+=["AP","GTS","PG"] + list(chain(["ROCK","TREE",
    "BIRD","MAMMAL"]*9)) 


    def __init__(self, filepath):
        self.filepath = filepath
        self.parsed_data = dict(zip(SSRF.INFO.keys(),[[]]*len(SSRF.INFO.keys())))


    def read(self):
        MAPPED_INFO = list(map(lambda x : self.INFO[x], self.ORDER))
        with open(self.filepath,"r") as f:
            self.data = f.read().splitlines()
            itm = 0
            for i in range(0,len(self.data)):
                number = ""
                count = 0
                if self.data[i][0] == '~':
                    break
                for j in range (0,len(self.data[i])):
                    number+=self.data[i][j]
                    count+=1

                    if self.ORDER[itm] == "NULL":
                        number = ""
                        count = 0
                        continue
                    if self.ORDER[itm] == "NEXT":
                        break
                    if self.data[j] == "@":
                        number =""
                        count = 0
                        continue
                    if type(MAPPED_INFO[itm]) == tuple:
                        if count >= MAPPED_INFO[itm][1]:
                            self.parsed_data[self.ORDER[itm]].append(Obj.getThing(number,MAPPED_INFO[itm][0]))
                            count = 0
                            itm+=1
                            number=""
                    elif count >= MAPPED_INFO[itm]:
                        print(self.ORDER[itm])
                        s = self.ORDER[itm]
                        self.parsed_data[s].append(number)
                        count = 0
                        itm+=1
                        number=""
                    

    def lol(self):
        return self.parsed_data

a = SSRF(r"new\20-436.dat")
a.read()
print(a.lol())