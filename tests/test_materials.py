"""验证资料足以读取和定位，不运行尚不存在的数值产品。"""
import json
from pathlib import Path
import numpy as np
from support.inspect_data import load_bundle

def test_tensor_inventory_and_shapes():
    catalog, arrays, _, _ = load_bundle()
    assert arrays and set(arrays) == set(catalog['tensors'])
    assert all(a.dtype.kind in 'fiu' for a in arrays.values())

def test_event_groups_have_distinct_identifiers():
    _, _, records, scenarios = load_bundle()
    assert records and scenarios
    assert all(isinstance(e.get('kind'),str) for s in scenarios for e in s['events'])

def test_declared_tensor_references_exist():
    _, arrays, records, _ = load_bundle()
    def visit(value):
        if isinstance(value,dict):
            for key,child in value.items():
                if key == 'tensor':
                    assert child in arrays
                visit(child)
        elif isinstance(value,list):
            for child in value:
                visit(child)
    visit(records)
