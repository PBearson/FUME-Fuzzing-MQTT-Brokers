# MosquittoByte

MosquittoByte is a versatile mutation-based fuzzer for MQTT brokers. It is written completely in Python, so it is largely portable. It can fuzz MQTT brokers on your local system or on remote servers. It can run for a fixed number of iterations or indefinitely. It can replay payloads that triggered interesting (or devastating) responses. It can display payload details (i.e., what packets were sent, and how were they fuzzed) without actually sending them. It can log network responses and even stdout/stderr responses, which may guide the fuzzing engine. It can send fuzzed packets in-order (e.g., CONNECT, SUBSCRIBE, DISCONNECT) or unfuzzed packets out-of-order (e.g., SUBSCRIBE, PUBREL, CONNECT). It can fuzz as fast or as slow as you want, as gently or intensely as you want. In short, it can do almost anything.

## Get Started

Assuming you have an MQTT broker running on your system (on port 1883), using MosquittoByte is as simple as this:

```
python mosquitto_byte.py
```

If you want to fuzz a remote broker, or if the broker is running on another port, you can customize the host/port as follows:

```
python mosquitto_byte.py -H <host> -P <port> 
```

MosquittoByte supports over 20 different options for customizing your fuzzing strategy. They will not all be covered here; however, you can see what is available to you by running the help option:

```
python mosquitto_byte.py -h
```

## Fuzzing Details

At its core, MosquittoByte is a simple mutation based fuzzer. Valid MQTT packets are sampled from the ___mqtt_corpus___ directory. Each packet can be fuzzed either by removing bytes, adding bytes, or mutating bytes. The number of bytes added, removed, or mutated is mostly random, but configurable. Furthermore, fuzzed packets can still be sent in a typical order (e.g., begin with CONNECT and end with DISCONNECT, never send server-to-client packets such as CONNACK, and so forth), or they can be sent out-of-order, which is also configurable. 

However, MosquittoByte enhances its fuzzing engine by observing 2 types of output from the broker: network responses and filestream (stdout, stderr) responses. When these responses are logged, the payloads that triggered them become part of the MQTT corpus. In this way, the fuzzer can tweak payloads that previously triggered valid (or invalid) responses, which may lead to more findings. Output files will be stored in an ___outputs___ directory, and all entries are timestamped. Be mindful that filestream responses can only be captured if the broker is running locally.

If MosquittoByte manages to crash the broker, details about the crash are logged in a ___crashes.txt___ file. Payloads which generate a crash also become part of the corpus, and the user can discover more payloads which generate the same crash. Moreover, if the broker is running locally, the fuzzer can restart the broker when it crashes.

All of these fuzzing techniques are highly customizable, and the user does not have to employ any of them if he doesn't want to. For instance, there may be cases where the broker is too verbose, and so the user does not want to record (or mutate) network packets.

## Some Examples

The fuzzer waits about 100 ms between each fuzzing attempt. You can change this duration:

```
python mosquitto_byte -fd 0.01  # Wait 10 ms
```

The fuzz intensity (e.g., percentage of packets which are fuzzed) is ranked from 0 to 10, while the construct intensity (e.g., the ordering of packets) is ranked from 0 to 3. By default, the fuzz intensity is set to 3 while the construct intensity is set to 0. Both are configurable:

```
python mosquitto_byte -fi 9 -ci 3 # Sets fuzz intensity to 9 and construct intensity to 3
```

```
python mosquitto_byte -afi  # Fuzz intensity is randomized on every iteration
```

```
python mosquitto_byte -aci  # Construct intensity is randomized on every iteration
```

You can start the broker from within the fuzzer. Then you will capture output from stdout/stderr that will be added to the corpus.

```
python mosquitto_byte -B "/usr/sbin/<broker>"  # Start the broker and log output from stdout/stderr
```

```
python mosquitto_byte -B "/usr/sbin/<broker>" -R  # Restart the broker in case it crashes.
```

But what if the broker is not a simple executable or shell script, or what if the filestream output is separate from the broker process? These cases can be handled as well:

```
python mosquitto_byte -B "java -jar <jarfile>"  # Run a JAR application
```

```
python mosquitto_byte -B "docker attach <container>"  # Read output from a Docker container.
```

You can run the fuzzer for a fixed number of iterations:

```
python mosquitto_byte -m 1000 # Terminate after 1000 iterations
```

## Findings

- [Mosquitto segmentation fault](https://github.com/eclipse/mosquitto/issues/2163). Patched in v2.0.10.

This section will (hopefully) be gradually updated as MosquittoByte discovers more bugs.
# FUME-Fuzzing-MQTT-Brokers
