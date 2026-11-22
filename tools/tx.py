import sys,glob,json,os,wave,numpy as np
def load(f):
    w=wave.open(f); a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768; return a
from faster_whisper import WhisperModel
d=sys.argv[1]; out=sys.argv[2]
m=WhisperModel(sys.argv[3],device="cpu",compute_type="int8",cpu_threads=4)
res={}
for f in sorted(glob.glob(d+'/*.wav')):
    segs,_=m.transcribe(load(f),language="ms",word_timestamps=True,vad_filter=False,initial_prompt="Qivea, sabun Qivea, kulit, sabun mandi.")
    L=[]
    for s in segs:
        L.append({"s":s.start,"e":s.end,"t":s.text.strip(),"w":[(w.start,w.end,w.word) for w in s.words]})
    k=os.path.basename(f)[:-4]; res[k]=L
    print(k," | ".join(f"[{x['s']:.1f}-{x['e']:.1f}] {x['t']}" for x in L),flush=True)
json.dump(res,open(out,'w'),ensure_ascii=False,indent=1)
