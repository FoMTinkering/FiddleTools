from fiddletools import FiddleComparator, SETTINGS

comparator = FiddleComparator()
if SETTINGS["comparator_settings"]["dump_json"]:
    comparator.to_json()
if SETTINGS["comparator_settings"]["dump_html"]:
    comparator.to_html()