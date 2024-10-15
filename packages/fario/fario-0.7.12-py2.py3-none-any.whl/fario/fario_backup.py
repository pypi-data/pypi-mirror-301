#!/usr/bin/env python
import os
import sys
from time import sleep
from dotenv import load_dotenv
from farcaster.HubService import HubService
from farcaster.fcproto.message_pb2 import MessageType, Message
import base64
import argparse
from . config import get_conf
from . __about__ import version


def get_all_messages(method, fid, page_size, wait):
	page_token="1strun"
	while page_token:
		if page_token == "1strun":
			page_token = None
		response = method(fid=fid, page_size=page_size, page_token=page_token)
		for message in response.messages:
			out = base64.b64encode(message.SerializeToString()).decode('ascii')
			yield out
		page_token = response.next_page_token
		sleep(wait)

def main():		
	parser = argparse.ArgumentParser(prog="fario-backup", description="Export Farcaster data.")
	parser.add_argument('--version', action='version', version='%(prog)s v'+version)
	parser.add_argument("fid", type=int, help="Export messages from fid=FID")
	parser.add_argument("--hub", help="Use the hub at <HUB>. Ex. --hub 192.168.1.1:2283", type=str)
	parser.add_argument("--ssl", help="Use SSL", action="store_true")
	parser.add_argument("--wait", type=int, help="Wait for <WAIT> milliseconds between reads.", default=0)
	args = parser.parse_args()

	conf = get_conf(required=['hub'], args=args)

	hub = HubService(conf['hub'], use_async=False, use_ssl=conf['ssl'])

	for c in get_all_messages(hub.GetAllCastMessagesByFid, args.fid, 1000, args.wait):
		print(c)
	#for c in get_data(hub.GetLinksByFid, args.fid, 100, args.limit, args.wait):
	#	print(c)
	# for c in get_reactions(hub.GetReactionsByFid, args.fid, None, 1000, args.wait):
	#	print(c)
	#for c in get_data(hub.GetUserDataByFid, args.fid, 100, args.limit, args.wait):
	#	print(c)

if __name__ == '__main__':
	main()