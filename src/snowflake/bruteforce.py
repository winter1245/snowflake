import socket
import sys

try:
    from snowflake.params import args
    import snowflake.helper as helper
except ImportError:
    from params import args
    import helper

def resolve():
   
    resolved=[]
    fl=helper.fromFile('subdomains.txt')
    for subdomain in fl:
        if not args.quiet:
            sys.stdout.write('\r')
            sys.stdout.write(f'{helper.GREEN}[INFO]{helper.WHITE} Query Dns [{fl.index(subdomain)+1} of {len(fl)}]')     
            sys.stdout.flush()
        try:
            result=socket.gethostbyname(subdomain)
            resolved.append(subdomain)
        except socket.gaierror:
            continue 
    
    helper.appendFile('resolved.txt',resolved)
    print()
    return

def bruteforce():
    
    resolve()
    return
