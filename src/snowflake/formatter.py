import sys
try:
    from snowflake.params import args
    import snowflake.helper
except ImportError:
    from params import args
    import helper

def formatScope():
    
    scope=helper.fromFile('scope.txt')
    lineCount= len(scope)
    domains = []
    alive = []
    i=0
    for line in scope:
        i+=1
        if not args.quiet:
            sys.stdout.write('\r')
            sys.stdout.write(f'{helper.GREEN}[INFO]{helper.WHITE} seperating scope [{str(i)} of {str(lineCount)}]')     
            sys.stdout.flush()

        if line[0]=='*':
            domains.append(line)
            if args.verbose and not args.quiet:
                print(f"\ncopy {line[:-1]} to wildcard.txt")

        else :
            alive.append(line)
            if args.verbose and not args.quiet:
                print(f"\ncopy {line[:-1]} to alive.txt")


    helper.writeFile('domains.txt',domains)
    helper.writeFile('alive.txt', alive)                   
    helper.removeWildcard('domains.txt')
    
    sys.stdout.write('\n')
    return 
