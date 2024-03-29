from kafka import KafkaConsumer, KafkaProducer
from base64 import b64encode
import sys
import argparse

SINK_TIMEOUT = 10  # how long to wait for sending message to the sink

# argument handling
parser = argparse.ArgumentParser()
parser.add_argument(
    "--server", help="the bootstrap server of both the source and the sink"
)
parser.add_argument(
    "--source", help="the bootstrap server of source from which to consume (read) data"
)
parser.add_argument(
    "--sink", help="the bootstrap server of the sink to write data. (can use 'stdout')"
)
parser.add_argument("--topic", help="the topic of both the source and the sink")
parser.add_argument("--source-topic")
parser.add_argument("--sink-topic")
parser.add_argument("--from-beginning", action="store_true", help="Read from the beginning of the topic")
parser.add_argument("-n", help="How many messages to read", type=int, default=10)
args = parser.parse_args()

# handle source/sink
assert any(
    (args.server, args.source, args.sink)
), "You need to define either a server or source and sink"
assert not (
    args.server and (args.source or args.sink)
), "Ambiguous combination of server/source/sink"

if args.server and args.source is None and args.sink is None:
    args.source = args.sink = args.server


# handle topic(s)
assert any(
    (args.topic, args.source_topic, args.sink_topic)
), "You need to define either a common 'topic' or source/sink topic"
assert not (
    args.topic and (args.source_topic or args.sink_topic)
), "Ambiguous combination of server/source/sink topics"

if args.topic and args.source_topic is None and args.sink_topic is None:
    args.source_topic = args.sink_topic = args.topic


# Double check that we're not trying to read and write to the same place
assert not (
    (args.source_topic == args.sink_topic) and (args.source == args.sink)
), "Attempting to read and write to the same server/topic. You probably don't want that"


def source_gen(server, topic, value_only=False, from_beginning=False):
    "A generator function for reading (binary) messages"
    src_consumer = KafkaConsumer(topic, group_id=None, bootstrap_servers=server, auto_offset_reset='earliest' if from_beginning else 'latest')
    for message in src_consumer:
        yield message.value if value_only else message


def sink_fn(server, topic):
    "Returns a function (lambda) for sending messages"
    if server.lower() == "stdout":
        # special handling for "stdout" sink: just print out the messages
        return print
    elif server.lower() == "stdout64":
        # special handling for "stdout64" sink: print the messages in a base64 encoding
        return lambda bites: print(str(b64encode(message), "utf-8"))

    sink_producer = KafkaProducer(bootstrap_servers=server)
    _sink = lambda msg: sink_producer.send(topic, msg).get(timeout=SINK_TIMEOUT)
    return _sink


print(
    "Consuming data from {}[{}] -> {}[{}]".format(
        args.source, args.source_topic, args.sink, args.sink_topic
    ), file=sys.stderr
)

# create a generator for reading messages
source = source_gen(args.source, args.source_topic, value_only=True, from_beginning=args.from_beginning)
# create function for sending messages
sink = sink_fn(args.sink, args.sink_topic)

for _ in range(args.n):
    message = next(source)
    print(">", end="", file=sys.stderr)
    sink(message)
