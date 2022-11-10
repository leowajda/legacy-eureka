import pandas as pd
from pathlib import Path
from functools import reduce

subdirs = [x for x in Path('.').iterdir() if x.is_dir() and 'eureka-' in x.name]
frames = [pd.read_csv(f'/home/runner/work/eureka-scraper/eureka-scraper/{dir}/docs/data.csv') for dir in subdirs]

join = reduce(lambda left, right: pd.merge(left, right, how='outer', on=['ID', 'Name']), frames)
join = join.set_index('ID').fillna('').sort_index()

with open('./README.md', 'w') as f:
    with open('./docs/content.md', 'r') as s:
        content = s.read()
    f.write(content)
    f.write(join.to_markdown(colalign=("center", "center", "center")))
