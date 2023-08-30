from os.path import isfile

from logging import getLogger, _nameToLevel
from flask import Flask, abort, jsonify

from deta import Deta
from functools import lru_cache

getLogger("werkzeug").setLevel(_nameToLevel["ERROR"])

def fread(
        path: str, *, root: str="web/", tokenizer: callable=lambda s: f"[[{s}]]", **replace
    ) -> str:
    """
    Checks if a file exists and if does returns its contents or else an empty string if not.
    """

    fpath = root + path
    
    if not isfile(fpath): return ""
    
    data = ""
    with open(fpath, "r") as file:
        data = file.read()
        file.close()
    
    if not replace: return data

    for rkey in replace:
        data = data.replace(tokenizer(rkey), str(replace[rkey]))
    
    return data

@lru_cache(None)
def edit_distance(s1: str, s2: str) -> int:
    """
    Calculates the distance between two strings
    """

    if len(s1) == 0: return len(s2)
    if len(s2) == 0: return len(s1)

    if s1[0] == s2[0]:
        return edit_distance(s1[1:], s2[1:])
    
    return 1 + min(
        edit_distance(s1[1:], s2[1:]),
        edit_distance(s1[1:], s2),
        edit_distance(s1, s2[1:])
    )

app = Flask("SSTDict", static_folder="res", static_url_path="/res")

_deta = Deta()

dict_db = _deta.Base("Dictionary")

@lru_cache(None)
def fetch_all_words() -> list:
    """
    Fetch all the words in dictionary
    """

    res = dict_db.fetch()
    all_items = [data["key"] for data in res.items]

    while res.last:
        res = dict_db.fetch(last=res.last)
        all_items += [data["key"] for data in res.items]
    
    return all_items

@app.route("/")
def home():
    return fread("index.html")

@app.route("/search/<query>")
@app.route("/search/<query>/<page>")
@app.route("/search/<query>/<page>/<perPage>")
def search(query: str, page: int = 1, perPage: int = 20):
    try:
        (int(page), int(perPage))
    except:
        return jsonify([])
    
    words_list = fetch_all_words()
    words_list = sorted(words_list, key=lambda word: edit_distance(query, word))
    words_list = words_list[(int(page) - 1) * int(perPage):]
    words_list = words_list[:int(perPage)]
    
    return jsonify([[index, word] for index, word in enumerate(words_list)])

@app.route("/meaning/<item>/get/")
def get_meaning(item: str):
    item_data = dict_db.get(item.lower())
    if not item_data:
        return jsonify({
            "key": item,
            "OK": False,
            "msg": "Item not found"
        })
    
    item_data["OK"] = True

    return jsonify(item_data)

@app.route("/meaning/<item>")
def meaning_page(item: str):
    item_data = dict_db.get(item.lower())
    if not item_data: return abort(404)

    return fread("meaning.html", **item_data)

if __name__ == "__main__":
    app.run(host="10.104.123.60", port=8000)
    # app.run(host="0.0.0.0", port=8000)

