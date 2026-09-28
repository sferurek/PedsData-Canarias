#!/usr/bin/env python3
"""Check official public URLs registered in the PedsData source catalog."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import json
import urllib.error
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/'data/semantic/sources_catalog.json'
UA='PedsData-Canarias-link-audit/0.9 (+https://github.com/sferurek/PedsData-Canarias)'

def check(source):
    url=source['official_url']
    request=urllib.request.Request(url,headers={'User-Agent':UA,'Range':'bytes=0-1023'})
    try:
        with urllib.request.urlopen(request,timeout=25) as response:
            return source['source_id'],url,response.status,response.geturl(),''
    except urllib.error.HTTPError as error:
        return source['source_id'],url,error.code,error.geturl(),str(error.reason)
    except Exception as error:
        return source['source_id'],url,None,url,type(error).__name__+': '+str(error)

def main():
    sources=json.loads(CATALOG.read_text())['sources']
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures=[pool.submit(check,source) for source in sources]
        rows=[future.result() for future in as_completed(futures)]
    rows.sort()
    print('source_id\tstatus\tfinal_url\tnote')
    for source_id,url,status,final,note in rows:
        redirect='' if final==url else 'redirect from '+url
        print(f'{source_id}\t{status or "TIMEOUT"}\t{final}\t{note or redirect}')
    failures=[row for row in rows if row[2] is None or row[2]>=400]
    raise SystemExit(1 if failures else 0)
if __name__=='__main__':main()
