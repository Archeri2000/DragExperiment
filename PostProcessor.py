import sys

def main():
    args = sys.argv[1:]
    f = open(args[0], "w+")

    MAX_BUFFER = 100

    ls = []
    while True:
        for line in sys.stdin:
            if line == "exit\n":
                f.writelines(ls)
                f.close()
                exit()
            ls.append(line)
            if len(ls) > MAX_BUFFER:
                f.writelines(ls)
                ls = []

if __name__ == '__main__':
    main()