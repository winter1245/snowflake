import argparse
parser = argparse.ArgumentParser(description="seperate scope")
parser.add_argument("-a", "--all",action="store_true", help="run all scripts successively")
parser.add_argument("-sc", "--scope",action="store_true", help="seperate scope")
parser.add_argument("-v", "--verbose",action="store_true", help="more verbose logging")
parser.add_argument("-q", "--quiet",action="store_true", help="no output to stdout")
args = parser.parse_args()
