import subprocess

try:
    from snowflake.params import args
    import snowflake.helper as helper
except ImportError:
    from params import args
    import helper




def imv():
    
    p=subprocess.run('imv data/*/*/*.png', shell=True,stdout=subprocess.PIPE)
    out=p.stdout.decode('utf8').split('\n')
    out=out[:-1]
    list=[]
    for i in range(len(out)):
        out[i]=out[i].split('/')[-3]
        out[i]=out[i].replace('_','.')
        list.append('https://' + out[i] + '\n')
        print('https://' + out[i])

    helper.writeFile('current.txt',list)
    return
