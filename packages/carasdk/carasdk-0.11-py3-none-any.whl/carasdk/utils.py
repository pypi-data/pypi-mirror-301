import yaml


def parse_yaml(file_path: str):
    """
    Parses a YAML file and returns its content.

    :param file_path: The path to the YAML file
    :return: The parsed Python object (usually a dictionary or list)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        return data
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

from datetime import datetime, timezone
from google.protobuf import timestamp_pb2 as _timestamp_pb2

class TimestampExt:
    def __init__(self, dt: datetime):
        """Initialize by saving the datetime object"""
        self._datetime = dt

    @staticmethod
    def from_unix_time(seconds: int, nanos: int = 0) -> 'TimestampExt':
        """Create a TimestampExt object from seconds and nanoseconds"""
        dt = datetime.fromtimestamp(seconds + nanos / 1_000_000_000, tz=timezone.utc)
        return TimestampExt(dt)

    @staticmethod
    def from_millis(millis: int) -> 'TimestampExt':
        """Create a TimestampExt object from milliseconds"""
        dt = datetime.fromtimestamp(millis / 1000.0, tz=timezone.utc)
        return TimestampExt(dt)

    @staticmethod
    def now() -> 'TimestampExt':
        """Get the current time and return a TimestampExt object"""
        return TimestampExt(datetime.now(tz=timezone.utc))

    def to_millis(self) -> int:
        """Convert the datetime object in the current instance to a millisecond timestamp"""
        epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
        delta = self._datetime - epoch
        return int(delta.total_seconds() * 1000)

    def to_protobuf_timestamp(self) -> _timestamp_pb2.Timestamp:
        """Convert the datetime object in the instance to a protobuf Timestamp object"""
        ts = _timestamp_pb2.Timestamp()
        total_seconds = int(self._datetime.timestamp())
        millis = int(self._datetime.microsecond / 1000)  # microseconds to milliseconds
        ts.seconds = total_seconds
        ts.nanos = millis * 1_000_000  # milliseconds to nanoseconds
        return ts

    @staticmethod
    def from_protobuf_timestamp(ts: _timestamp_pb2.Timestamp) -> 'TimestampExt':
        """Parse a protobuf Timestamp object into a TimestampExt object"""
        return TimestampExt.from_unix_time(ts.seconds, ts.nanos)

    @staticmethod
    def from_protobuf_timestamp_to_millis(ts: _timestamp_pb2.Timestamp) -> int:
        """Parse a millisecond timestamp from a protobuf Timestamp"""
        millis = ts.seconds * 1000 + ts.nanos // 1_000_000
        return millis

    def __repr__(self):
        """Custom output for class instances"""
        return f"TimestampExt({self._datetime.isoformat()})"
    
# Example usage
if __name__ == "__main__":
    # Get the current time
    now_ext = TimestampExt.now()
    print(f"Current TimestampExt: {now_ext}")

    # Convert the current time to a millisecond timestamp
    millis = now_ext.to_millis()
    print(f"Current timestamp in millis: {millis}")

    # Restore a TimestampExt object from a millisecond timestamp
    restored_ext = TimestampExt.from_millis(millis)
    print(f"Restored TimestampExt from millis: {restored_ext}")

    # Create a TimestampExt object from a Unix timestamp
    custom_ext = TimestampExt.from_unix_time(1632999280, 123000000)
    print(f"Custom TimestampExt from Unix time: {custom_ext}")

    # Convert the instance to a protobuf Timestamp
    protobuf_ts = now_ext.to_protobuf_timestamp()
    print(f"Protobuf Timestamp: seconds={protobuf_ts.seconds}, nanos={protobuf_ts.nanos}")

    # Restore a TimestampExt object from a protobuf Timestamp object
    restored_from_protobuf = TimestampExt.from_protobuf_timestamp(protobuf_ts)
    print(f"Restored TimestampExt from protobuf Timestamp: {restored_from_protobuf}")