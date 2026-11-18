"""카타카나 이름 -> 로마자 (pvf 시스템 폰트가 한글을 못 그려서 사용)"""
import re
DI={'キャ':'kya','キュ':'kyu','キョ':'kyo','シャ':'sha','シュ':'shu','ショ':'sho','シェ':'she','チャ':'cha','チュ':'chu','チョ':'cho','チェ':'che',
'ニャ':'nya','ニュ':'nyu','ニョ':'nyo','ヒャ':'hya','ヒュ':'hyu','ヒョ':'hyo','ミャ':'mya','ミュ':'myu','ミョ':'myo','リャ':'rya','リュ':'ryu','リョ':'ryo',
'ギャ':'gya','ギュ':'gyu','ギョ':'gyo','ジャ':'ja','ジュ':'ju','ジョ':'jo','ジェ':'je','ビャ':'bya','ビュ':'byu','ビョ':'byo','ピャ':'pya','ピュ':'pyu','ピョ':'pyo',
'ティ':'ti','ディ':'di','トゥ':'tu','ドゥ':'du','デュ':'dyu','テュ':'tyu','ファ':'fa','フィ':'fi','フェ':'fe','フォ':'fo','フュ':'fyu',
'ウィ':'wi','ウェ':'we','ウォ':'wo','ヴァ':'va','ヴィ':'vi','ヴェ':'ve','ヴォ':'vo','ツァ':'tsa','ツェ':'tse','ツォ':'tso','クォ':'quo','クヴィ':'kvi','イェ':'ye','スィ':'si','ズィ':'zi','グァ':'gua','クァ':'qua'}
MO=dict(zip('アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポヴァィゥェォ',
['a','i','u','e','o','ka','ki','ku','ke','ko','sa','shi','su','se','so','ta','chi','tsu','te','to','na','ni','nu','ne','no','ha','hi','fu','he','ho','ma','mi','mu','me','mo','ya','yu','yo','ra','ri','ru','re','ro','wa','wo','n','ga','gi','gu','ge','go','za','ji','zu','ze','zo','da','ji','zu','de','do','ba','bi','bu','be','bo','pa','pi','pu','pe','po','vu','a','i','u','e','o']))
def romaji(s,cap=True):
    o='';i=0
    while i<len(s):
        if s[i:i+3] in DI: o+=DI[s[i:i+3]];i+=3;continue
        if s[i:i+2] in DI: o+=DI[s[i:i+2]];i+=2;continue
        c=s[i]
        if c=='ッ':
            n=romaji(s[i+1:i+3],False) if i+1<len(s) else ''
            o+=n[:1] if n and n[0] not in 'aiueo' else ''
        elif c=='ー':
            pass
        elif c in MO: o+=MO[c]
        else: o+=c
        i+=1
    return o[:1].upper()+o[1:] if cap else o
