import os
import re

pattern = re.compile("\d+")

def searchNum(string):
    return pattern.search(string)

def main():
    os.makedirs("new",mode=0o777,exist_ok=True)

    for root, dirs, files in os.walk(r".\AHP_AP20\AHPDATA",topdown=False):
        for name in files:
            namep = os.path.join(root,name)
            if ".dat" in namep and "FIT" in namep:
                #breakpoint()
                f = open(namep,"r")
                s = f.read()
                for idx in range(0,len(s)):
                    if idx%100 == 0:
                         s = s[:idx] + "\n" + s[idx:]
                
                f = open(".\\new\\" + name, "w+")
                do = []
                linen = 0
                counter = 0
                for string in s.splitlines():
                    if string.strip() == "":
                        continue
                    if linen in range(1,11):
                        if "." in string:
                            do.append(string[26:31])
                        else:
                            do.append("N/A")
                    linen+=1
                    string = string[:26].replace(" ","@")
                    f.write(string + "\n")
                    counter+=1
                
                f.write("~~~~\n")
                for string in do:
                    f.write(string.strip() + "\n")
                    counter+=1
                
                if counter < 25 and name.split("-")[0]=="20":
                    print(name + " " + str(counter))

if __name__=="__main__":
    main()