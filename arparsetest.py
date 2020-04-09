
import argparse


parser = argparse.ArgumentParser(description='Client to interact with either the gRPC or XML-RPC store inventory server')
subparsers = parser.add_subparsers(title='command', dest='cmd', required=True)

grpc_server = subparsers.add_parser(name='grpc', description='Interact with the grpc server')
xml_server = subparsers.add_parser(name='xml', description='Interact with the xml-rpc server')

grpc_server.add_argument('--add', choices=['add', 'remove'], help='Add a product to the inventory database')

args = parser.parse_args()

if args.cmd == 'grpc':
    print('grp did it')
elif args.cmd == 'xml':
    print('doing the xml')
else:
    print('doing the else')

