# Kpipe
This is a simple script for forwarding/repeating/piping kafka messages from one server/topic to another.  
It's inteded to be useful, particularly for **binary** messages. For text messages I suggest you use 
[`kafka-console-producer.sh`](https://kafka.apache.org/quickstart#quickstart_send) or, even better, 
[`kcat`](https://github.com/edenhill/kcat) ([reff](https://docs.confluent.io/platform/current/app-development/kafkacat-usage.html))(formelly `kafkacat`).  
kcat is a great tool, described as a ["swiss-army knife of tools"](https://docs.confluent.io/platform/current/app-development/kafkacat-usage.html) by confdluent themselves, but it does not (easily) support binary messages. This is why I wrote `kpipe`.  

Use this at your own risk, and be sure to check [the code](pipe.py).


# Running from docker vs directly
This script has a [single python dependency](requirements.txt), `kafka-python`. If this
dependency is satisfied in your local environment (virtual or otherwise) you can simply run the
python script with `python pipe.py ...args...`.  
If you can't be bothered, kpipe is packaged [in docker](https://hub.docker.com/repository/docker/cmantas/kpipe#), so
you can run it with `docker run -i cmantas/kpipe ..args...`.  
The rest of this readme assumes an alias is set for kpipe. Either

``` shell
alias kpipe="/path/to/python /path/top/kpipe/pipe.py"
```
or

``` shell
alias kpipe="docker run -i cmantas/kpipe"
```

# Usage examples

You can test that you can read from your source by setting a `stdout` sink (specially handled). Set the
`--source` arg to the bootstrap server and specify a `--topic`
``` shell
$ kpipe --source a-kafka-bootstrap.domain.com --topic topic_name --sink stdout
```
*Note:* no parsing is attempted for binary messages. If the data are in a binary format (which they probably will,
otherwise why are you not using [kcat](https://github.com/edenhill/kcat)) the printout will brobably not be legible.

The following arguments are available

- `-n` : the number of messages we will pipe (default is 10)
- `--source` : the source (input) kafka bootstrap server we will be reading from (optionally with port)
- `--sink` : the sink (output) kafka bootstrap server we will be writing to (optional port)
- `--source-topic` : the topic to read from
- `--sink-topic` : the topic to write to
- `--server` : use this as shorthand if `--source` and `--sink` are the same server
- `--topic` : use this as shorthand if `--source-topic` and `--sink-topic` are the same

So when specifying everything:

``` shell
$ kpipe \
	--source a-kafka-bootstrap.domain.com \
	--source-topic topic_name \
	--sink another-kafka-bootstrap.foo.com \
	--sink-topic foobar \
	-n 5
```
Example repating a topic to another topic in the same kafka cluster:
``` shell
$ kpipe \
	--server a-kafka-bootstrap.domain.com \
	--source-topic src_topic_name \
	--sink-topic sink_topic_name \
	-n 5
```

Example repating the same topic to another kafka cluster:
``` shell
$ kpipe \
	--topic topic_name \
	--source a-kafka-bootstrap.domain.com \
	--sink another-kafka-bootstrap.foo.com \
	-n 3 
```

