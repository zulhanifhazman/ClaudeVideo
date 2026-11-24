# Synthesises a cheerful 30s background track (royalty-free, generated) -> out/music.wav
import numpy as np, wave
SR=44100; BPM=112; beat=60/BPM; DUR=30
t_all=np.zeros(int(SR*DUR))
def add(sig,start):
    i=int(start*SR); j=min(len(t_all),i+len(sig)); t_all[i:j]+=sig[:j-i]
def note(f,d,amp=.2,kind='pluck'):
    t=np.arange(int(SR*d))/SR
    if kind=='pluck':
        s=(np.sin(2*np.pi*f*t)+.4*np.sin(4*np.pi*f*t)+.15*np.sin(6*np.pi*f*t))*np.exp(-t*6)
    elif kind=='pad':
        s=(np.sin(2*np.pi*f*t)+.5*np.sin(2*np.pi*f*1.003*t))*np.minimum(1,t*4)*np.exp(-t*.8)
    elif kind=='bass':
        s=np.sin(2*np.pi*f*t)*np.exp(-t*3)
    return amp*s
def kick():
    t=np.arange(int(SR*.3))/SR; return .7*np.sin(2*np.pi*(50+90*np.exp(-t*30))*t)*np.exp(-t*12)
def hat():
    t=np.arange(int(SR*.06))/SR; return .08*np.random.randn(len(t))*np.exp(-t*60)
def clap():
    t=np.arange(int(SR*.15))/SR; return .18*np.random.randn(len(t))*np.exp(-t*25)
mf=lambda m:440*2**((m-69)/12)
prog=[(60,[60,64,67]),(67,[59,62,67]),(69,[60,64,69]),(65,[60,65,69])]  # C G Am F
mel=[76,79,81,79,76,74,72,74, 74,76,79,76,74,72,71,72, 72,76,81,84,81,79,76,79, 77,76,74,72,74,76,74,72]
nb=int(DUR/beat)
for b in range(nb):
    tb=b*beat; bar=(b//4)%4; root,ch=prog[bar]
    if b%4==0:
        for n in ch: add(note(mf(n),beat*4,.06,'pad'),tb)
    add(note(mf(root-24),beat*.9,.35,'bass'),tb)
    if b>=4: add(kick(),tb)
    add(hat(),tb+beat/2)
    if b%2==1 and b>=8: add(clap(),tb)
    if b>=8:
        for k in range(2):
            m=mel[(b*2+k)%len(mel)]
            add(note(mf(m),beat*.6,.12),tb+k*beat/2)
# gentle reverb-ish echo
d=int(SR*beat*.75); echo=np.zeros_like(t_all); echo[d:]=t_all[:-d]*.25; t_all+=echo
fade=np.ones_like(t_all); n=int(SR*2.5); fade[-n:]=np.linspace(1,0,n); fade[:int(SR*.3)]=np.linspace(0,1,int(SR*.3))
t_all*=fade; t_all/=np.abs(t_all).max()*1.15
pcm=(t_all*32767).astype(np.int16); st=np.stack([pcm,pcm],1)
with wave.open('out/music.wav','wb') as w: w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(st.tobytes())
