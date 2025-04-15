# FiddleTools

FiddleTools is a collection of tools designed to streamline the analysis of `__fiddle__.json` files for Fields of Mistria.
The tools also work on other game files that are JSONs and similarly formatted, though this project is mostly targeted at the fiddle files.

Light Mode | Dark Mode
:----------|-------------:
![](https://github.com/FoMTinkering/FiddleTools/blob/main/docs/lightparser.png) | ![](https://github.com/FoMTinkering/FiddleTools/blob/main/docs/darkparser.png)

All you need to run these tools is Python, with no need for any added packages.

To use the tools, go through the `settings.json` file included and set things up according to your game installation and personal preferences, or write your own scripts by importing the tools into Python directly.

## FiddleParser

FiddleParser is a very generic JSON-to-HTML kind of converter. The main QoL change is that it ignores all keys in the JSON which have "/" characters in them, since these are mostly duplicate keys in the file and take up a lot of space. 
Of course, a big benefit is that the output looks clean enough to read and click through, as it's a collection of collapsible bullet lists.


To convert your fiddle to HTML, set up the `settings.json` file and then run the `fiddle_to_html.py` script, or write your own script as shown in the subsection below if you want more control over the data.

### Scripting with FiddleParser

You can import `FiddleParser`:
```py
from fiddletools import FiddleParser

fiddle = FiddleParser()
```
and treat this variable as you would a dictionary, so all of these are valid :
```py
print(fiddle)
print(len(fiddle))
print(fiddle["ui"])
for k, v in fiddle.items(): print(k, v)
```

You can specify a custom path:
```py
fiddle = FiddleParser(path="fiddle_backups")
```
or parse a file that isn't the fiddle:
```py
fiddle = FiddleParser(filename="__mist__")
```

You can of course export the file to HTML, and optionally specify the output folder:
```py
fiddle.to_html()
# this is also valid:
# fiddle.to_html(output_folder="dump")
```

## FiddleComparator

FiddleComparator creates a dictionary that contains all the differences between two versions of the fiddle.
This also includes an HTML export (and a JSON dump feature) which is the main benefit of this comparator.


To export this comparison HTML, set up the `settings.json` file and then run the `compare_fiddles.py` script, or write your own script as shown in the subsection below if you want more control over the data.

### Scripting with FiddleComparator

You can import `FiddleComparator`:
```py
from fiddletools import FiddleComparator

comparator = FiddleComparator()
```
and, just like `FiddleParser`, you can treat it like any other dictionary, so these are valid:
```py
print(comparator)
print(len(comparator))
for k, v in comparator.items(): print(k, v)
print(comparator.get("stores")) 
# we aren't guarantee that "stores" is a key here (values could be the same in both versions)
```
You can specify custom paths and a custom output folder:
```py
comparator = FiddleComparator(
    path1="jsons_backup/0.13.1/__fiddle__.json",
    v1="v0.13.1",
    path2="jsons_backup/0.13.3/__fiddle__.json",
    v2="0.13.3",
    output_folder="comparisons"
)
```
and finally dump using the following methods:
```py
comparator.to_html()
comparator.to_json()
```
