import sys
import os


def main():
    if len(sys.argv) > 0:
        print(sys.argv[0])
    else:
        print("No args supplied")

    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            print(os.path.join(root, name))
        for name in dirs:
            print(os.path.join(root, name))


if __name__ == "__main__":
    main()
