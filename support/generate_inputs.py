"""生成声明尺寸的合成张量，用于资源边界和数值输入核查。"""
import argparse
import json
from pathlib import Path
import numpy as np

def generate(profile,output):
    """只准备输入，拒绝覆盖已有输出目录。"""
    output=Path(output)
    output.mkdir(parents=True,exist_ok=False)
    rng=np.random.default_rng(20261125)
    result={}
    for name, spec in profile['arrays'].items():
        shape=tuple(spec['shape']);count=int(np.prod(shape));pattern=spec['pattern']
        if pattern=='constant':value=np.full(shape,spec['value'])
        elif pattern=='arange':value=(np.arange(count)*spec.get('step',1)).reshape(shape)
        elif pattern=='modulo':value=(np.arange(count)%spec['modulus']).reshape(shape)
        elif pattern=='integers':value=rng.integers(spec['low'],spec['high'],size=shape)
        elif pattern=='probability_rows':
            value=rng.uniform(.001,1,size=shape);value/=value.sum(axis=-1,keepdims=True)
        elif pattern=='unit_rows':
            value=rng.normal(size=shape);value/=np.linalg.norm(value,axis=-1,keepdims=True)
        elif pattern=='boxes':
            value=rng.uniform(0,1000,size=shape);value[:,2:]=value[:,:2]+rng.uniform(2,30,size=(shape[0],2))
        elif pattern=='uniform':value=rng.uniform(spec.get('low',-1),spec.get('high',1),size=shape)
        else:raise ValueError('未知输入分布')
        value=np.asarray(value,dtype=spec['dtype'])
        if value.shape!=shape or not np.isfinite(value).all():raise ValueError('生成张量无效')
        dest=output/(name+'.npy');np.save(dest,value,allow_pickle=False)
        result[name]={'path':dest.name,'shape':list(shape),'dtype':str(value.dtype),'bytes':int(value.nbytes)}
    (output/'index.json').write_text(json.dumps({'id':profile['id'],'parameters':profile['parameters'],'arrays':result},ensure_ascii=False,indent=2))
    return result

def main():
    p=argparse.ArgumentParser(description='生成较大尺寸的本地合成输入')
    p.add_argument('--profile',type=Path,default=Path(__file__).resolve().parents[1]/'data/large_profile.json')
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();profile=json.loads(a.profile.read_text())
    result=generate(profile,a.output)
    print(json.dumps({'资料组':profile['id'],'数组数':len(result),'输入总字节':sum(v['bytes'] for v in result.values()),'输出目录':str(a.output)},ensure_ascii=False))

if __name__=='__main__':main()
