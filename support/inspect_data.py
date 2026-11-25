"""检查本地合成张量与事件资料，不执行模型运算。"""
import argparse
import json
import math
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]

def load_bundle(root=ROOT):
    """读取清单并检查形状、标识和事件引用资料。"""
    root = Path(root)
    catalog = json.loads((root / 'data/catalog.json').read_text())
    arrays = {}
    for name, relative in catalog['tensors'].items():
        path = (root / relative).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError('张量文件超出项目路径')
        value = json.loads(path.read_text())
        if any(not isinstance(x,int) or x<0 for x in value['shape']):
            raise ValueError('张量维度不是非负整数')
        if len(value['values']) != math.prod(value['shape']):
            raise ValueError('张量元素数与形状不一致')
        array = np.asarray(value['values'],dtype=value['dtype']).reshape(value['shape'])
        if not np.isfinite(array).all():
            raise ValueError('资料中的张量含非有限值')
        arrays[name] = array
    records = json.loads((root/'data/records.json').read_text())
    scenarios = json.loads((root/'data/events.json').read_text())
    ids = [item['id'] for item in scenarios]
    if len(ids) != len(set(ids)) or not all(item['events'] for item in scenarios):
        raise ValueError('事件组标识重复或为空')
    return catalog, arrays, records, scenarios

def main():
    parser = argparse.ArgumentParser(description='查看合成资料的张量、记录和事件组')
    parser.add_argument('--root',type=Path,default=ROOT)
    args=parser.parse_args()
    catalog, arrays, records, scenarios = load_bundle(args.root)
    print(json.dumps({'产品':catalog['product'],'资料性质':catalog['provenance'],'张量':{k:{'shape':list(v.shape),'dtype':str(v.dtype),'bytes':v.nbytes} for k,v in arrays.items()},'记录字段':list(records),'事件组':[s['id'] for s in scenarios]},ensure_ascii=False))

if __name__ == '__main__':
    main()
