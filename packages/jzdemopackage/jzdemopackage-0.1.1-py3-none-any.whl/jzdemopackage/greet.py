import argparse


def sayhello(name):

    print("Hello ", name)



if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--name', help='name')

    args = parser.parse_args()
    
    sayhello(args.name)

