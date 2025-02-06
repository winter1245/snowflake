import sys
try:
    from snowflake.params import args
except ImportError:
    from params import args

def formatScope():
    
    with open("scope.txt", "rb") as f:
        lineCount = sum(1 for _ in f)

    with open('scope.txt') as scope:
        i=0
        for line in scope:
            i+=1
            if not args.quiet:
                sys.stdout.write('\r')
                sys.stdout.write(f'{'\033[92m'}[INFO]{'\033[0m'} seperating scope [{str(i)} of {str(lineCount)}]')
                sys.stdout.flush()

            if line[0]=='*':
               
                wildcard=line[1:] # remove *
                if wildcard[0]=='.':
                    wildcard=wildcard[1:] # remove .
                try:
                    with open('wildcard.txt', 'a') as file:
                        file.write(wildcard)
                    if args.verbose and not args.quiet:
                        print(f"\ncopy {line[:-1]} to wildcard.txt")

                except OSError:
                    print("Writing to wildcard.txt failed")

            else:
                try:
                    with open('active.txt', 'a') as file:
                        file.write("https://" + line)
                    if args.verbose and not args.quiet:
                        print(f"\ncopy {line[:-1]} to active.txt")

                except OSError:
                    print("Writing to active.txt failed")


        sys.stdout.write('\n')
        return 
