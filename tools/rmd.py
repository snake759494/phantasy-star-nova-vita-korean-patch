import struct
NBASIC=373; LBASE=401
def v7(c): return ((c>>8)<<7)|(c&0x7f)
def enc7(v): return bytes([0x80|(v&0x7f), v>>7])
def parse(b):
    hs,so,to,te,te2,cnt=struct.unpack('<6I',b[0x30:0x48])
    r=dict(hdr=hs,so=so,to=to,te=te,cnt=cnt,id=struct.unpack('<Q',b[0x90:0x98])[0] if so else None)
    s=b[so+16:to] if so else b''
    toks=[];i=0
    while i+1<len(s):
        c=s[i]|s[i+1]<<8; i+=2
        if c==0: break
        if c==0x8090:
            j=s.index(b'\0',i); toks.append(('C',c,s[i:j])); i=j+1
        elif c in (0x8081,0x8099): toks.append(('C',c,s[i:i+1])); i+=1
        elif c&0x8000: toks.append(('C',c,b''))
        else: toks.append(v7(c))   # value: basic = v-1, local = v-LBASE
    r['toks']=toks; r['nloc']=cnt-NBASIC if so else 0
    return r
