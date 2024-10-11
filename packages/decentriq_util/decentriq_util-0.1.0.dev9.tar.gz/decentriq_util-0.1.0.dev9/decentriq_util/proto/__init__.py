from typing import Tuple
from google.protobuf.message import Message
from google.protobuf.internal.encoder import _VarintBytes # type: ignore
from google.protobuf.internal.decoder import _DecodeVarint32 # type: ignore


def parse_length_delimited(serialized_bytes: bytes, deserialized_object: Message) -> int:
    """
    Decodes a binary content and returns a parsed object of a given type
    """
    res: Tuple[int, int] = _DecodeVarint32(serialized_bytes, 0)
    message_length, offset = res
    end_offset = offset + message_length
    deserialized_object.ParseFromString(bytes(serialized_bytes[offset:end_offset]))
    return end_offset


def serialize_length_delimited(message_object: Message) -> bytes:
    """
    Encodes an object of a given type to binary
    """
    serialized: bytes = _VarintBytes(message_object.ByteSize())
    serialized += message_object.SerializeToString()
    return serialized
