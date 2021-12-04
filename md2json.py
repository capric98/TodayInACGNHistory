#!/usr/bin/env python3
#coding=utf-8
import argparse
import os
import json

import git
import toml

from datetime import date

__markdown_path__ = "markdown"

def trans(mdf, jsf: os.PathLike, today, commit: str):
    print(mdf, "->", jsf)

    jobj   = {
        "events": [],
        "lastUpdated": {
            "date": today,
            "commit": commit
        }
    }

    datesuffix = os.path.basename(mdf).split(".")[0]
    datesuffix = "-{}-{}".format(datesuffix[:2], datesuffix[-2:])

    with open(mdf, encoding="utf-8") as f:
        event = None
        for line in f.readlines():
            # print(line, end="")
            if line.strip().startswith("# "):
                if event: jobj["events"].append(event)
                event  = {
                    "title": "",
                    "date": "",
                    "content": ""
                }
                event["title"] = line.split("-", maxsplit=1)[1].strip()
                event["date"]  = line.split("-")[0].split("# ", maxsplit=1)[1].strip() + datesuffix
            else:
                event["content"] = event["content"]+line

    if event: jobj["events"].append(event)

    for k in range(len(jobj["events"])):
        if jobj["events"][k]["content"].strip().endswith("```"):
            newcontent = jobj["events"][k]["content"].strip().removesuffix("```")
            addpos = newcontent.rindex("```toml")
            # print(newcontent[addpos:].removeprefix("```toml"))

            jobj["events"][k]["content"] = newcontent[:addpos]
            jobj["events"][k]["addition"] = toml.loads(newcontent[addpos:].removeprefix("```toml"))

        jobj["events"][k]["content"] = jobj["events"][k]["content"].rstrip()

    with open(jsf, mode="w", encoding="utf-8") as f:
        f.write(json.dumps(jobj))

def all_markdown(path: list[os.PathLike]) -> list[os.PathLike]:
    flist = []
    for root, _, files in os.walk(path):
        for f in files:
            flist.append(os.path.join(root, f))

    return flist


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Markdown to json.')
    parser.add_argument("--force", "-F", action=argparse.BooleanOptionalAction, help="force update")
    parser.add_argument("files", type=str, nargs="*", help="force files")

    args = parser.parse_args()

    today = date.isoformat(date.today())

    repo   = git.Repo()
    commit = repo.head.object.hexsha

    with open("api/.history", encoding="utf-8") as f:
        history = f.read()
    flist = [item.a_path for item in repo.index.diff(repo.commit(history))]

    if os.path.basename(__file__) in [os.path.basename(f) for f in flist]:
        print("Update all jsons due to the change of this script.")
        flist = all_markdown(__markdown_path__)
    elif args.force:
        flist = args.files

    # print("Update list: {}".format(flist))

    for file in flist:
        if not(file.endswith(".md") and file.startswith(__markdown_path__)): continue

        fdate  = os.path.basename(file).split(".")[0]
        lang   = os.path.basename(os.path.dirname(file))
        target = os.path.join("api/json", "{}.{}.json".format(fdate, lang))

        trans(file, target, today, commit)