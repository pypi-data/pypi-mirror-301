#!/usr/bin/env python

import sys
import base64
from farcaster.fcproto.message_pb2 import MessageType, Message
from google.protobuf.json_format import MessageToDict, MessageToJson
import argparse
import json

def main():
	parser = argparse.ArgumentParser(prog="fario2json", description="Convert fario export to json")
	parser.add_argument("--lines", type=int, help="Only parse first <LINES>", default=0)
	args = parser.parse_args()

	print("[")
	separator = ''
	count=0
	for line in sys.stdin:
		m = Message.FromString(base64.b64decode(line))

		out = MessageToJson(m)
		out = json.loads(out)
		out['signer'] = base64.b64decode(out['signer']).hex()
		out['hash'] = base64.b64decode(out['hash']).hex()
		out = json.dumps(out)
		print(separator+str(out))
		if not separator:
			separator = ', '
		if args.lines and count >= args.lines:
			break
			
	print("]")

if __name__ == '__main__':
	main()