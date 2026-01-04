from scholarly import scholarly
import jsonpickle
import json
from datetime import datetime
import os

author: dict = scholarly.search_author_id("bj7eQ6sAAAAJ")

try:
    scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
except Exception as e:
    print(f"Warning: Could not fill all sections: {e}")
    # 尝试只获取基本信息
    try:
        scholarly.fill(author, sections=['basics', 'indices', 'counts'])
    except Exception as e2:
        print(f"Warning: Could not fill basic sections: {e2}")

name = author.get('name', 'Unknown')
author['updated'] = str(datetime.now())
author['publications'] = {v['author_pub_id']:v for v in author.get('publications', [])}
print(json.dumps(author, indent=2))
os.makedirs('../assets/results', exist_ok=True)
with open(f'../assets/results/gs_data.json', 'w') as outfile:
    json.dump(author, outfile, ensure_ascii=False)

shieldio_data = {
  "schemaVersion": 1,
  "label": "citations",
  "message": f"{author.get('citedby', 0)}",
}
with open(f'../assets/results/gs_data_shieldsio.json', 'w') as outfile:
    json.dump(shieldio_data, outfile, ensure_ascii=False)
