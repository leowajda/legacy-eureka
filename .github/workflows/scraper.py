import subprocess
import pandas as pd
import sys
import re


def fetch_leetcode_url(path):
    name = fetch_problem_name(path)
    url_name = re.sub(r"[^a-zA-Z0-9 ]", "", name).replace(" ", "-").lower()
    return f"[{name}](https://leetcode.com/problems/{url_name}/)"


def fetch_github_url(repository_name, path):
    label = 'arrows_counterclockwise' if 'recursive' in path else 'arrow_up_down'
    return f' [:{label}:](https://github.com/{repository_name}/blob/master/{path}) '


def fetch_problem_name(path):
    command = f'git log --pretty=format:"%B" --follow -- {path} | tail -n 1'
    result = subprocess.run([command], text=True, check=True, shell=True, stdout=subprocess.PIPE)
    return re.search(r"\'([^']*)\'", result.stdout)[1]


def fetch_id(path):
    return int(re.search(r"\d+", path)[0])


def update_files(data):
    with open('./docs/data.csv', 'w') as f:
        f.write(data.to_csv())

    with open('./README.md', 'w') as f:
        with open('./docs/content.md', 'r') as s:
            content = s.read()
        f.write(content)
        f.write(data.to_markdown(colalign=("center", "center", "center"), tablefmt="github"))


def populate_data(data):
    accumulator = [data]
    repository_name = sys.argv[1]

    n = len(sys.argv)
    for i in range(2, n):

        file_path = sys.argv[i]
        id = fetch_id(file_path)
        github_url = fetch_github_url(repository_name, file_path)

        if id in data.index:
            prev_record = data.loc[id, data.columns[-1]]
            if file_path not in prev_record:
                data.loc[id, data.columns[-1]] = prev_record + github_url
        else:
            leetcode_url = fetch_leetcode_url(file_path)
            accumulator.append(pd.DataFrame([[id, leetcode_url, github_url]], columns=[id_col, name_col, lang_col]))
            accumulator.append([[id, leetcode_url, github_url]])

    return accumulator


# prev_data = pd.read_csv('./docs/data.csv')
# id_col, name_col, lang_col = prev_data.columns[0], prev_data.columns[1], prev_data.columns[2]

# temp_data = populate_data(prev_data)
# n = len(temp_data)

# new_data = pd.concat([temp_data[i] for i in range(n)], ignore_index=True).sort_values(by=[id_col])
# new_data.set_index(id_col, inplace=True)

# update_files(new_data)

