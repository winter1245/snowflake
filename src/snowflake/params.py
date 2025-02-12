import argparse
parser = argparse.ArgumentParser(description="work in progress recon tool")
parser.add_argument("-a", "--all",action="store_true", help="run all scripts successively")
parser.add_argument("-sc", "--scope",action="store_true", help="seperate scope")
parser.add_argument("-v", "--verbose",action="store_true", help="more verbose logging")
parser.add_argument("-q", "--quiet",action="store_true", help="no output to stdout")
parser.add_argument("-sub", "--subdomains",action="store_true", help="enumerate subdomains")
parser.add_argument("-th", "--threading",action="store_true", help="enable multithreading")
parser.add_argument("-c", "--cycle",action="store_true", help="do a cycle")
parser.add_argument("-brute", "--bruteforce",action="store_true", help="bruteforce subdommains and resolve through dns queries")
parser.add_argument("-view", "--view",action="store_true", help="view images")
args = parser.parse_args()
