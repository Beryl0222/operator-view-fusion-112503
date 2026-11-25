"""验证业务输入之间的引用关系及形状，不计算目标输出。"""
import numpy as np
from support.inspect_data import load_bundle

def test_linked_materials():
    _, arrays, r, scenarios = load_bundle()
    size=arrays['storage'].size
    for view in r['views']:
        assert len(view['shape']) == len(view['strides'])
        for index in np.ndindex(*view['shape']):
            address=view['offset']+sum(i*s for i,s in zip(index,view['strides']))
            assert 0<=address<size
    nodes={n['id'] for n in r['expression']['nodes']}
    assert set(r['expression']['outputs'])<=nodes
