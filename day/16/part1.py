#!/usr/bin/env python
from logging import debug, info, warning, error, exception, critical
from pprint import pprint, pformat

from bitarray.util import ba2int, hex2ba

import aoc
from packet import parse_packet, Packet, LiteralPacket, OperatorPacket


def version_sum(packet: Packet) -> int:
	match packet:
		case LiteralPacket(version, _):
			return version
		case OperatorPacket(version, _, children):
			return version + sum(version_sum(child) for child in children)


def main(args):
	message = hex2ba(args.input.read().strip())
	info(f'Read {len(message)} bits')
	packet, rest = parse_packet(message)
	if rest.any():
		warning(f'Extra data after packet: {rest}')
	if len(rest) >= 4:
		warning(f'More than one nybble ({len(rest)} bits) of extra data')
	
	print(f'Version sum of packets is {version_sum(packet)}')


if __name__ == '__main__':
	parser = aoc.get_argparser()
	# Add problem-specifc args here
	args = aoc.parse_args(parser)
	
	main(args)