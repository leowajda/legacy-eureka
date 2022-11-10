import pandas as pd
from pathlib import Path
from functools import reduce

p = Path('.')
subdirs = [x for x in p.iterdir() if x.is_dir() and 'eureka-' in x.name]

for dir in subdirs:
    for file in dir.iterdir():
        print(file)

frames = [pd.read_csv(f'/home/runner/work/eureka-scraper/eureka-scraper/{dir}/docs/data.csv') for dir in subdirs]

join = reduce(lambda left, right: pd.merge(left, right, how='outer', on=['ID', 'Name']), frames)
join = join.set_index('ID').fillna('').sort_index()

with open('./README.md', 'w') as f:
    with open('./docs/content.md', 'r') as s:
        content = s.read()
    f.write(content)
    f.write(join.to_markdown(colalign=("center", "center", "center")))
