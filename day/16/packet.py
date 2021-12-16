from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from functools import reduce
from logging import debug, info, warning, error, exception, critical
from operator import mul, gt, lt, eq
from typing import Generic, Literal

from bitarray import bitarray
from bitarray.util import ba2int

from aoc import indent


class PacketType(Enum):
	SUM=0
	PRODUCT=1
	MIN=2
	MAX=3
	LITERAL=4
	GREATER=5
	LESS=6
	EQUAL=7
	
	# Fill in other possible values with generic names
	# From timespan example in official docs
	_ignore_ = ['i']
	for i in range(8):
		if i not in {LITERAL}:
			vars()[f'OPERATOR_{i}'] = i


@dataclass(slots=True)
class LiteralPacket:
	version: int
	packet_type: Literal[PacketType.LITERAL] = field(
		init=False, default=PacketType.LITERAL)
	value: int
	
	def evaluate(self):
		debug(f'{indent}Evaluating literal packet {self.value}')
		return self.value


@dataclass(slots=True)
class OperatorPacket:
	version: int
	packet_type: PacketType
	children: list[Packet]
	
	def evaluate(self):
		debug(f'{indent}Evaluating {self.packet_type} packet')
		with indent:
			children_values = (child.evaluate() for child in self.children)
			def binop(op):
				lhs, rhs = children_values
				return int(op(lhs, rhs))
			
			match self.packet_type:
				case PacketType.SUM:
					return sum(children_values)
				case PacketType.PRODUCT:
					return reduce(mul, children_values, 1)
				case PacketType.MIN:
					return min(children_values)
				case PacketType.MAX:
					return max(children_values)
				case PacketType.GREATER:
					return binop(gt)
				case PacketType.LESS:
					return binop(lt)
				case PacketType.EQUAL:
					return binop(eq)
				case op:
					raise ValueError(f'Unknown op: {op}')


Packet = LiteralPacket | OperatorPacket


def parse_int(bits: bitarray, length) -> tuple[int, bitarray]:
	return ba2int(bits[:length]), bits[length:]


def parse_packet_type(bits: bitarray) -> tuple[PacketType, bitarray]:
	match parse_int(bits, 3):
		case t, bits:
			return PacketType(t), bits


def parse_literal(bits: bitarray) -> tuple[int, bitarray]:
	value = bitarray()
	while True:
		more, group, bits = bits[0], bits[1:5], bits[5:]
		value.extend(group)
		if not more:
			return ba2int(value), bits


def parse_packet(bits: bitarray) -> tuple[Packet, bitarray]:
	version, bits = parse_int(bits, 3)
	packet_type, bits = parse_packet_type(bits)
	debug(f'{indent}Parsing packet version {version}, type {packet_type}')
	with indent:
		if packet_type == PacketType.LITERAL:
			value, bits = parse_literal(bits)
			debug(f'{indent}Value: {value}')
			return LiteralPacket(version, value), bits
		else:  # Operator
			children = []
			length_type, bits = bits[0], bits[1:]
			if length_type:  # count by sub-packets
				count, bits = parse_int(bits, 11)
				debug(f'{indent}There are {count} children')
				for _ in range(count):
					child, bits = parse_packet(bits)
					children.append(child)
			else: # count by bit length
				length, bits = parse_int(bits, 15)
				debug(f'{indent}Children take up {length} bits')
				subpacket_bits, bits = bits[:length], bits[length:]
				while subpacket_bits:
					child, subpacket_bits = parse_packet(subpacket_bits)
					children.append(child)
			return OperatorPacket(version, packet_type, children), bits
