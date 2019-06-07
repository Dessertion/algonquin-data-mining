# algonquin-data-mining

These are a couple of Python scripts to aid TOPS students in mining the ~~extremely poorly formatted~~ Algonquin field trip sample station data. This will hopefully help alleviate much of the pain of the data-mining process and allow students to _actually_ find interesting results (or the lack thereof given the quality of past data).

## Updating information

To update the available json information:

1. Extract all the `.dat` files from the given AP data zip file into a folder in these scripts' directory (i.e. extracting them all into a folder called `AP20_Data` which is in the same directory as the provided 3 scripts)
    > Note: it will be far easier to extract the data if one uses a tool such as 7zip, which can extract just files using regex (regular expressions). This means that you can simply extract all the `*.dat` files from the zipped data file provided.

2. Run the script `fix_format.py`, and follow the instructions
3. Then run the script `json_dumper.py`

The data will all be stored in the `jsons/` folder, with names formatted like `AP-GTS.json`, where `AP` is the AP number (and GTS is hopefully self-explanatory by this point).

## Reading the data

* All the information is in strings; parse it yourself
* Names are formatted like the SSRFs (i.e. most things will have the same name), with some exceptions:
    * If there are non-alphabet characters in the name, replace it with the easiest English equivalent
        * This means `Δ` -> `DELTA` and `#` -> `NUMBER`
    * Spaces are replaced with underscores (e.g. `LAND HAB` -> `LAND_HAB`)
    * Names with numbers have the numbers removed, and all entries sharing the same prefix will be stored in one array using the numberless-prefix (e.g. `SWT1` and `SWT2` are simply both found under the array entry for `SWT`)
    * Images have been all clumped together under the name `IMG`
        * The image order is the same as on the SSRF, top-to-bottom, left-to-right
        > Note: Unless you're doing Panoramas, this should have no real consequence, and if you are doing Panoramas/are thinking of doing Panoramas, change your mind or feel the regret.
* Bird, Tree, Mammal, and Rock data are formatted slightly differently:
    * There are 4 arrays of objects, one for each `BIRDS`, `TREES`, `MAMMALS`, and `ROCKS`
    * Each entry (an object) in any of the array of objects, contain the relevant data for that given object
        * The entries in each array are in the same order as they appear in on the SSRF
        * Example: `MAMMALS[0]` may be the following object: `{
      "ID": "08",
      "ACT": "0",
      "LOC": "3",
      "EVD": "0"
    }`
* Imaging experiments are also present in the JSON file. Possible experiments are:
    * DO (Dissolved Oxygen, parts per million)
    * PH (Water pH)
    * N3 (Nitrate, mmol per litre )
    * N2 (Nitrite, mmol per litre )
    * NH (Ammonium, parts per million)
    * PO (Phosphate, parts per thousand)
    * CH (Chlorine, parts per thousand)
    * HD (Hardness, parts per thousand)
    * AK (Alkalinity, parts per thousand)
    * SP (Soil pH)
* Entries with broken data/no data should have the value `"N/A"` (a string), or is empty (in the case of an array)
