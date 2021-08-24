# Command line tools to upload data from TTL files into StarDog.

## Usage

```{bash}
pip install -r requirements.txt
python utils/ttl2graph/run.py --help  
python utils/ttl2graph/run.py --db_name='gauss_old_model' --path='/home/jovyan/shared/expo/UVIndex/UVSearch/Gauss_index/ttl/'
```
  
By default, using next parameters:  
`--db_name='gauss_old_model'`  
`--path='/home/jovyan/shared/expo/UVIndex/UVSearch/Gauss_index/ttl/'`  
`--count=100`  
`--workers=10`  
`--endpoint='http://ai.ihsmdev.biz:5820`  





