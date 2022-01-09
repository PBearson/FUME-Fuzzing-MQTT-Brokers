# FUME: Fuzzing MQTT Brokers

## Table of Contents
1. [Introduction](#introduction)
2. [Get Started](#get-started)
3. [Configuring your Fuzzing Session](#configuring-your-fuzzing-session)
4. [Crash Triage](#crash-triage)
5. [Bugs Discovered with FUME](#bugs-discovered-with-fume)

## Introduction

![FUME Markov Models](images/fuzz_algorithm_both.jpg)

FUME is a fuzzing engine targeted directly at MQTT brokers. It uses both generation-guided and mutation-guided fuzzing techniques to craft fuzzy MQTT payloads to send to your target. It also leverages a response feedback mechanism for monitoring new behavior from the broker -- specifically, behavior in the form of MQTT responses and console responses (standard output). When FUME spots sufficiently new behavior, the responsible request is appended to the input queue for further fuzzing later on.

FUME is modeled as a finite state machine using Markov modeling. Basically, FUME needs to make several choices during a single fuzzing round, such as whether to select mutation-guided or generation-guided fuzzing, which packet types to select or generate, how intensely to fuzz the input seed (and which fuzzing operations are carried out), etc. To illustrate this decision-making process, we model it as a stochastic process with several parameters that are fully configurable by the end user. For example, as shown in the figure above, the user could give `X1` a high probability (e.g., 0.9) and `X2` a low probability (e.g., 0.1). This would produce input seeds that are small (e.g., a single CONNECT packet) but heavily fuzzed. The full details of FUME are provided in the research paper, which will become available at a later date.

A demo of FUME can be viewed [on Youtube](https://www.youtube.com/watch?v=99gAayiIcEo).

## Get Started

Download this repository:

```
git clone https://github.com/PBearson/FUME-Fuzzing-MQTT-Brokers.git
```

FUME is written entirely in Python. It is incompatible with Python 2. So far I have only tested it with Python 3.8.10, but most other versions of Python 3 will probably work just fine. To get started, download your favorite MQTT broker and run it. [Here is a list of brokers](https://github.com/PBearson/FUME_Targets) that we tested directly.

When it is running (ideally on localhost and port 1883), simply run the fuzz script to start attacking it:

```
python3 fuzz.py
```

You will see a printout of your configuration, and the fuzzing session will begin. As it runs, it will alert you when unique network responses are detected. If you get lucky, the target will eventually crash, and you will see a dump of the last 5 payloads that FUME sent to the target. These payloads are also logged to a file for analysis later on.

## Configuring Your Fuzzing Session

You can pass a configuration file as an argument to customize your fuzzing session:

```
python3 fuzz.py <config file>
```

The configuration file is defined as a list of key-value pairs, separated by a `=` sign. FUME supports a fairly extensive number of configuration options. The obvious ones are the Markov model parameters, i.e., `X1`, `X2`, `X3`, `b`, etc. However, there are several more options that are worth mentioning directly:

* `TARGET_ADDR` and `TARGET_PORT` define the target IP address and port.
* `START_COMMAND` sets the command for starting the target directly. This is the only way to monitor console responses.
* `TARGET_START_TIME` sets the expected amount of time it takes for the target to start up (and more specifically, to expose its MQTT port).
* `SIMILARITY_THRESHOLD` sets the similarity threshold value for console responses. FUME discards responses that are at least this similar to previously seen responses. For instance, a value of 0.3 means that if a console response is at least 30% similar to any previously seen response, then it is not logged.
* `CRASH_DIRECTORY` and `CRASH_FILENAME_PREFIX` set the directory and filename prefix of the request queue when it is dumped due to a crash. The file always has the structure `<CRASH_DIRECTORY>/<CRASH_FILENAME_PREFIX>-<timestamp>`.

The script will strip all whitespace away from the config file to parse it more easily. If, for some reason, you need whitespace in one of your options, just place a `@@` wherever you want to place the whitespace. You will probably only want this when you set `START_COMMAND`, for example:

`
START_COMMAND = ./mosquitto@@-c@@mosquitto.conf@@-p@@1884 # --> Parsed as './mosquitto -c mosquitto.conf -p 1884'
`

The full list of supported configuration options can be viewed in the file _config.sample_.

## Crash Triage

## Bugs Discovered with FUME

If you want to test FUME yourself on the same brokers we did, please refer to [this repository](https://github.com/PBearson/FUME_Targets).

* [CVE-2021-28166](https://nvd.nist.gov/vuln/detail/CVE-2021-28166): In Mosquitto v2.0.0 - 2.0.9, a null pointer dereference occurs when a client sends MQTT v5 CONNACK packet.
* [CVE-2021-34432](https://nvd.nist.gov/vuln/detail/CVE-2021-34432): In Mosquitto v2.0.7 and earlier, the server crashes if the client sends a PUBLISH packet with topic length = 0.
* [KMQTT broken pipe error](https://github.com/davidepianca98/KMQTT/commit/7a4e31567c1a850e86bdc0660e243e7e6e9a33cf): In KMQTT version 0.2.7 and earlier, the server may crash if it tries on send a packet (e.g., SUBACK) to a closed TCP connection.
* [aedes malformed DISCONNECT](https://github.com/mqttjs/mqtt-packet/pull/107): In aedes 0.45.0, the server may crash if a client tries to send a malformed DISCONNECT packet.
  * This is actually due to a bug in mqtt-tools 6.9.0, a node package which aedes depends on.
