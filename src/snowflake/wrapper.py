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

def gf(pattern):

    print(f'gf {pattern}')
    p=subprocess.run((f'gf {pattern}'), shell=True,stdout=subprocess.PIPE)
    out=p.stdout.decode('utf8').split('\n')
    out=out[:-1]

    return out

def notify(notification):
    
    p=subprocess.run(f'notify-send {notification}',shell=True)

    return
