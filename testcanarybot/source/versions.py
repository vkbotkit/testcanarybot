def codenameToINT(int1: int, int2: int, int3: int) -> int:
    return int1 * 10000 + int2 * 1000 + int3

def correctCodeName(int1: int, int2: int, int3: int) -> str:
    return f"{'%02d' % int1}.{'%02d' % int2}.{'%03d' % int3}"


raw = {
    'sorted': {
        'stable': {},

        'unstable': {},

        'dev': {
            0: {9: [100 + i for i in range(1, 8)]} 
        }
    },
    'root': {
        #convertedINT: currentCodeName
    }
}
for i in raw['sorted'].keys():
    for j in raw['sorted'][i].keys():
        for k in raw['sorted'][i][j].keys():
            for l in raw['sorted'][i][j][k]:
                raw['root'][codenameToINT(j,k,l)] = correctCodeName(j,k,l) + " " + i
                "jj.kk.ll"

current = raw['root'][max(raw['root'].keys())]