def codenameToINT(int1: int, int2: int, int3: int) -> int:
    return int1 * 10000 + int2 * 1000 + int3

def correctCodeName(int1: int, int2: int, int3: int) -> str:
    return f"{'%02d' % int1}.{'%02d' % int2}.{'%03d' % int3}"


published = {
    'sorted': {
        'stable': {},

        'unstable': {
            0: {9: [100]} 
        },

        'dev': {
            0: {9: [101, 102, 103, 104, 105]} 
        }
    },
    'root': {
        #convertedINT: currentCodeName
    }
}
for i in published['sorted'].keys():
    for j in published['sorted'][i].keys():
        for k in published['sorted'][i][j].keys():
            for l in published['sorted'][i][j][k]:
                published['root'][codenameToINT(j,k,l)] = correctCodeName(j,k,l) + " " + i
                "jj.kk.ll"

current = published['root'][max(published['root'].keys())]