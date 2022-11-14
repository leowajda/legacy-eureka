import subprocess
import pandas as pd
import sys
import re


def fetch_id(path):
    return int(re.search(r"\d+", path)[0])


def fetch_leetcode_url(path):
    name = fetch_problem_name(path)
    url_name = re.sub(r"[^a-zA-Z0-9 ]", "", name).replace(" ", "-").lower()
    return f"[{name}](https://leetcode.com/problems/{url_name}/)"


def fetch_github_url(repository_name, path):
    label = 'arrows_counterclockwise' if 'recursive' in path else 'arrow_up_down'
    return f' [:{label}:]({repository_name}/blob/master/{path}) '


def fetch_problem_name(path):
    command = f'git log --pretty=format:"%B" --follow -- {path} | tail -n 1'
    result = subprocess.run([command], text=True, check=True, shell=True, stdout=subprocess.PIPE)
    return re.search(r"\'([^']*)\'", result.stdout)[1]


prev_frames = pd.read_csv('./docs/data.csv')
id_col, name_col, lang_col = prev_frames.columns
n, repo_name = len(sys.argv), sys.argv[1]

prev_frames = prev_frames.assign(lang_col=prev_frames[lang_col].str.split(' ')).explode(lang_col)
new_frames = [pd.DataFrame(
    [[fetch_id(sys.argv[i]), fetch_leetcode_url(sys.argv[i]), fetch_github_url(repo_name, sys.argv[i])]],
    columns=[id_col, name_col, lang_col]) for i in range(2, n)]

frames = pd.concat(new_frames + [prev_frames], ignore_index=True)
frames = frames.groupby(by=[id_col, name_col], as_index=False)[lang_col].agg(lambda x: set(x))
frames[lang_col] = frames[lang_col].apply(' '.join)

if not frames.equals(prev_frames):
    frames = frames.set_index(keys=[id_col]).sort_index()
    with open('./docs/data.csv', 'w') as f:
        f.write(frames.to_csv())

    with open('./README.md', 'w') as f:
        with open('./docs/content.md', 'r') as s:
            content = s.read()
        f.write(content)
        f.write(frames.to_markdown(colalign=("center", "center", "center")))
