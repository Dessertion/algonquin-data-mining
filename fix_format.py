import os
import re

pattern1 = re.compile(r"\d+")
pattern2 = re.compile(r"[^0-9\n@]")

def searchNum(string):
    return pattern1.search(string)

def replaceNonNum(string):
    return pattern2.sub("$",string)

def main(folder,foldername):
    os.makedirs(folder,mode=0o777,exist_ok=True)

    for root, dirs, files in os.walk(foldername,topdown=False):
        for name in files:
            namep = os.path.join(root,name)
            if ".dat" in name and "-" in name:
                #breakpoint()
                f = open(namep,"r")
                s = f.read()
                lines = [s[i:i+99] for i in range(0,len(s),99)]
                
                f = open("./" + folder + "/" + name, "w+")
                ions = []
                counter = 0

                ap = int(name.split("-")[0])
                out = ""

                if ap <= 12:
                    rep = "0"
                else:
                    rep = "@"
                for linen, string in enumerate(lines):
                    if string.strip() == "" and linen not in range (1,19):
                        continue
                    if linen in range(1,11):
                        if "." in string[26:]:
                            ions.append(string[26:].strip())
                        else:
                            ions.append("N/A")
                    if linen in range(0,11):
                        if ap <= 12 and linen==10:
                            string = string[:29].replace(" ",rep).replace("*","0")
                        else:
                            string = string[:26].replace(" ",rep).replace("*","0")
                    else:
                        string = string[:29].replace(" ",rep).replace("*","0")

                    if linen == 10 and ap <= 12: #lol pesky randomass extra integer
                        string = string[:8] + string[9:]

                    out += (string + "\n")
                    counter+=1

                out = replaceNonNum(out) #check for faulty numbers
                out +=("~~~~\n")
                for string in ions:
                    out += (string + "\n")
                    #counter+=1
                
                
                f.write(out)

                # if counter < 20: # and name.split("-")[0]=="20":
                #     print(name + " " + str(counter))

if __name__=="__main__":
    foldername = input("Enter name of the folder containing the .dat files: ")
    main("new",foldername)
    print("Done Fixing Data")
    