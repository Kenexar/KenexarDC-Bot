import argparse


args_to_parse = ['channel', 'name', 'coggers']


parser = argparse.ArgumentParser()
parser.add_argument('name', help='Change name')

print(parser.parse_args(args_to_parse))
