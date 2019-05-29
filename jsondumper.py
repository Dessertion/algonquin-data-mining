from scrape_data import SSRF
import os
import json

os.makedirs("jsons",exist_ok=True)

for root, dirs, files in os.walk(r"./new"):
    for f in files:
        if "*" in open(os.path.join(root,f)).read():
            print(os.path.join(root,f))
        x = SSRF(os.path.join(root,f))
        with open("./jsons/" + f.split(".")[0] + ".json","w+") as new:
            txt = x.toJSON()
            ap = json.loads(txt)["AP"]
            if len(ap) >= 2:
                if ap[0] != ap[1]:
                    #breakpoint()
                    print(f)
            new.write(x.toJSON())
