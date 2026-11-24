# Playful "teasing" (na-na-na-na-na / sol-mi-la-sol-mi) background track, synthesised -> out/music.wav
import numpy as np, wave
SR=44100; BPM=126; B=60/BPM; DUR=30
out=np.zeros(int(SR*DUR)); rng=np.random.default_rng(1)
def add(s,t0,g=1.0):
    i=int(t0*SR); j=min(len(out),i+len(s))
    if i<len(out): out[i:j]+=g*s[:j-i]
def T(d): return np.arange(int(SR*d))/SR
mf=lambda m:440*2**((m-69)/12)
def kazoo(f,d,a=.22):
    t=T(d); vib=1+.012*np.sin(2*np.pi*6*t)
    ph=2*np.pi*np.cumsum(f*vib)/SR
    s=np.sign(np.sin(ph))*.5+np.sin(ph)+.3*np.sin(2*ph)+.15*np.sin(3*ph)
    s+= .15*rng.standard_normal(len(t))*np.abs(np.sin(ph))  # buzzy
    env=np.minimum(1,t*60)*np.minimum(1,(d-t)*25)
    return a*s*env
def xylo(f,d,a=.18):
    t=T(d); return a*(np.sin(2*np.pi*f*t)+.3*np.sin(2*np.pi*4*f*t)*np.exp(-t*30))*np.exp(-t*9)
def tuba(f,d,a=.35):
    t=T(d); ph=2*np.pi*f*t; return a*(np.sin(ph)+.4*np.sin(2*ph)+.2*np.sin(3*ph))*np.minimum(1,t*40)*np.exp(-t*4)
def kick(): t=T(.25); return .6*np.sin(2*np.pi*(45+80*np.exp(-t*35))*t)*np.exp(-t*14)
def snare(): t=T(.18); return (.2*rng.standard_normal(len(t))+.15*np.sin(2*np.pi*190*t))*np.exp(-t*22)
def hat(): t=T(.05); return .06*rng.standard_normal(len(t))*np.exp(-t*70)
def boing(t0):
    t=T(.45); f=180+120*np.sin(2*np.pi*9*t)*np.exp(-t*5)+t*200
    add(.35*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*5),t0)
def slide(t0,up=True,d=.5):
    t=T(d); f=np.linspace(500,1600,len(t)) if up else np.linspace(1600,500,len(t))
    add(.18*np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.pi*t/d),t0)
# taunt motif (G4 G4 E4 A4 G4 E4) in 2 bars, answered by a cheeky variant
G,E,A,C,D,F=67,64,69,72,62,65
taunt=[(G,0,.75),(G,1,.5),(E,1.5,1),(A,2.5,.5),(G,3,1),(E,4,1.5)]
taunt2=[(G,0,.5),(G,.5,.5),(E,1,.5),(A,1.5,.5),(G,2,.5),(E,2.5,.5),(C,3,.5),(D,3.5,.5),(E,4,1),(C,5,1.5)]
chords=[[48,55],[48,55],[53,60],[55,62]]  # C C F G oom-pah
nbars=int(DUR/(4*B))+1
for bar in range(nbars):
    t0=bar*4*B; root=chords[bar%4]
    for k in range(4):
        tb=t0+k*B
        add(tuba(mf(root[0] if k%2==0 else root[1]-12),B*.8),tb)      # oom
        if k%2==1: add(xylo(mf(root[1]+12),B*.4,.08),tb); add(xylo(mf(root[1]+16),B*.4,.06),tb)  # pah
        if bar>=1:
            if k in(0,2): add(kick(),tb)
            else: add(snare(),tb)
        add(hat(),tb+B/2)
# melody: kazoo taunts in 2-bar phrases, xylo echoes
for ph in range(0,nbars,2):
    t0=ph*4*B; mel=taunt if (ph//2)%2==0 else taunt2
    for m,b,d in mel:
        add(kazoo(mf(m),d*B*.9),t0+b*B)
        add(xylo(mf(m+12),.3,.07),t0+b*B+B*4*2*0)  # sparkle double
# sfx on scene changes / pops
for t in [0.2,3.8,8.7,9.1,10.1,13.8,14.8,18.1,23.1,24.0]: boing(t)
for t in [3.4,8.3,13.3,17.7,22.6]: slide(t,up=True,d=.45)
slide(28.5,up=False,d=.8)
d=int(SR*B*.5); e=np.zeros_like(out); e[d:]=out[:-d]*.18; out+=e
fade=np.ones_like(out); n=int(SR*2); fade[-n:]=np.linspace(1,0,n); out*=fade
out=np.tanh(out/np.abs(out).max()*1.4)*.85
pcm=(out*32767).astype(np.int16)
with wave.open('out/music.wav','wb') as w: w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(np.stack([pcm,pcm],1).tobytes())
