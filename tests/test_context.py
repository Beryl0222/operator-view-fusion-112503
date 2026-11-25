"""核对合成输入的业务引用及文件一致性。"""
import numpy as np
from support.inspect_data import load_bundle

def test_context():
    _, arrays, r, scenarios = load_bundle()
    from PIL import Image
    from pathlib import Path
    root=Path(__file__).resolve().parents[1]
    for image in r['images']:
        source=np.asarray(Image.open(root/image['source_file']))
        h,w=image['valid_height'],image['valid_width']
        assert source.shape == (h,w)
        assert np.array_equal(source,arrays['images'][image['row'],:h,:w])
    assert all(np.all(arrays[c['tensor']]>0) for c in r['quantization_configs'])
