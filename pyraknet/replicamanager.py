import asyncio
import logging

from pyraknet.bitstream import BitStream, c_bit, c_ubyte, c_ushort
from pyraknet.messages import Message

log = logging.getLogger(__name__)

class ReplicaManager:
	def __init__(self):
		self._participants = set()
		self._network_ids = {}
		self._current_network_id = 0

	def add_participant(self, address):
		self._participants.add(address)
		for obj in self._network_ids:
			self.construct(obj, (address,), new=False)

	def on_disconnect_or_connection_lost(self, data, address):
		self._participants.discard(address)

	def construct(self, obj, recipients=None, new=True):
		# recipients is needed to send replicas to new participants
		if recipients is None:
			recipients = self._participants

		if new:
			self._network_ids[obj] = self._current_network_id
			self._current_network_id += 1

		out = BitStream()
		out.write(c_ubyte(Message.ReplicaManagerConstruction))
		out.write(c_bit(True))
		out.write(c_ushort(self._network_ids[obj]))
		out.write(obj.send_construction())

		for recipient in recipients:
			self.send(out, recipient)

	def serialize(self, obj):
		out = BitStream()
		out.write(c_ubyte(Message.ReplicaManagerSerialize))
		out.write(c_ushort(self._network_ids[obj]))
		out.write(obj.serialize())

		for participant in self._participants:
			self.send(out, participant)

	def destruct(self, obj):
		log.debug("destructing %s", obj)
		obj.on_destruction()
		out = BitStream()
		out.write(c_ubyte(Message.ReplicaManagerDestruction))
		out.write(c_ushort(self._network_ids[obj]))

		for participant in self._participants:
			self.send(out, participant)

		del self._network_ids[obj]
