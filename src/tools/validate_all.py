import glob,os,collections
# The map pack lives in the repo; EQ_MAPS overrides (same convention as the other tools).
OUT=os.environ.get('EQ_MAPS', os.path.join(os.path.dirname(__file__),'..','..','Emoda Legends Maps'))
issues=collections.defaultdict(list); stats={}
files=sorted(f for f in glob.glob(f'{OUT}/*.txt') if not f.endswith('_colored.txt'))
for p in files:
    b=os.path.basename(p); raw=open(p,'rb').read()
    # 1) CRLF: every newline must be \r\n. Count lone \n (not preceded by \r)
    lone=0
    for i,ch in enumerate(raw):
        if ch==0x0A and (i==0 or raw[i-1]!=0x0D): lone+=1
    # 2) trailing/format + color range
    txt=raw.decode('utf-8','replace'); nL=nP=colbad=fmtbad=0
    for ln in txt.split('\r\n'):
        if not ln: continue
        if ln[0]=='L':
            nL+=1; f=ln[1:].split(',')
            if len(f)<9: fmtbad+=1; continue
            try:
                c=[int(x) for x in f[6:9]]
                if any(v<0 or v>255 for v in c): colbad+=1
            except: fmtbad+=1
        elif ln[0]=='P':
            nP+=1; f=ln[1:].split(',')
            if len(f)<7: fmtbad+=1; continue
            try:
                c=[int(x) for x in f[3:6]]
                if any(v<0 or v>255 for v in c): colbad+=1
            except: fmtbad+=1
    stats[b]=(nL,nP)
    if lone: issues['lone_nl'].append((b,lone))
    if colbad: issues['color_out_of_range'].append((b,colbad))
    if fmtbad: issues['bad_format'].append((b,fmtbad))
    if nL==0 and nP==0: issues['empty'].append((b,0))
print(f"Validated {len(files)} files.")
for k in ['lone_nl','color_out_of_range','bad_format','empty']:
    v=issues.get(k,[])
    print(f"  {k}: {len(v)}"+ ("" if not v else "  -> "+", ".join(f'{n}({c})' for n,c in v[:12])))
# zone coverage: base zones missing _1 or _2
bases=sorted(set(b[:-4] for b in stats if not (b[:-4].endswith(('_1','_2','_3')))))
miss1=[z for z in bases if f'{z}_1.txt' not in stats]
miss2=[z for z in bases if f'{z}_2.txt' not in stats]
print(f"\nBase zones: {len(bases)}")
print(f"  missing _1 ({len(miss1)}): {', '.join(miss1)}")
print(f"  missing _2 ({len(miss2)}): {', '.join(miss2)}")
