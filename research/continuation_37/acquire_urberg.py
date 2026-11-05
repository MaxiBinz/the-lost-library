"""One ordinary public repository download with limits, receipts and MD5 check."""
import hashlib
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
URL="https://knowledge.uchicago.edu/records/ejwkr-nxd77/files/Urberg_uchicago_0330D_13320.pdf?download=1"
EXPECTED_MD5="1f0193e4c997d3a94e060d804a38aeda"
LIMIT=500_000_000
TARGET=ROOT/"research/scholarship/urberg2016.pdf"


def main():
    if TARGET.exists():
        if hashlib.md5(TARGET.read_bytes()).hexdigest()==EXPECTED_MD5:
            print("Already retained; no network request.")
            return
        raise RuntimeError("Existing file is not the verified source; preserve it for audit.")
    audit=json.loads((ROOT/"data/resource_audit.json").read_text())
    assert audit["conservative_planning_total_bytes"]+LIMIT<3_000_000_000
    receipt={"url":URL,"record_url":"https://knowledge.uchicago.edu/records/ejwkr-nxd77",
             "expected_md5":EXPECTED_MD5,"private_reading_only":True,
             "rights":"Copyright 2016 Michelle Urberg; repository labels the dissertation Open. No redistribution permission inferred.",
             "checked_at_utc":datetime.now(timezone.utc).isoformat(),"bytes_received":0}
    partial=TARGET.with_suffix(".pdf.part")
    start=time.monotonic()
    try:
        with urllib.request.urlopen(URL,timeout=60) as response:
            receipt.update(status=response.status,final_url=response.url,
                           content_type=response.headers.get("Content-Type"),content_length=response.headers.get("Content-Length"))
            assert response.status==200 and receipt["content_type"].split(";",1)[0].lower() in {"application/pdf","application/octet-stream"}, "Unexpected response type; do not treat HTML as a PDF"
            if receipt["content_length"]: assert int(receipt["content_length"])<=LIMIT
            md5=hashlib.md5();sha=hashlib.sha256();milestone=32_000_000
            with partial.open("wb") as output:
                while True:
                    block=response.read(min(1024*1024,LIMIT-receipt["bytes_received"]+1))
                    if not block:break
                    if receipt["bytes_received"]==0:assert block.startswith(b"%PDF-"), "Response lacks PDF signature"
                    receipt["bytes_received"]+=len(block)
                    if receipt["bytes_received"]>LIMIT:raise ValueError("Transfer ceiling reached")
                    output.write(block);md5.update(block);sha.update(block)
                    if receipt["bytes_received"]>=milestone:
                        print(json.dumps({"bytes_received":receipt["bytes_received"],"elapsed_s":round(time.monotonic()-start,1)}),flush=True)
                        milestone+=32_000_000
            receipt.update(md5=md5.hexdigest(),sha256=sha.hexdigest())
            assert receipt["md5"]==EXPECTED_MD5,"Published MD5 mismatch"
            assert partial.open("rb").read(5)==b"%PDF-"
            partial.rename(TARGET)
            receipt.update(saved=True,path=str(TARGET.relative_to(ROOT)))
    except Exception as exc:
        receipt.update(saved=False,error=type(exc).__name__+": "+str(exc))
        raise
    finally:
        receipt["elapsed_s"]=round(time.monotonic()-start,2)
        path=HERE/"download_receipts.json"
        previous=json.loads(path.read_text()) if path.exists() else []
        path.write_text(json.dumps(previous+[receipt],indent=2)+"\n")
    print(json.dumps(receipt,indent=2))


if __name__=="__main__":main()
