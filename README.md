# FUME-Fuzzing-MQTT-Brokers

A successor to [MosquittoByte](https://github.com/PBearson/MosquittoByte).

![FUME Markov Models](images/fuzz_algorithm_both.jpg)

FUME is a fuzzing engine targeted directly at MQTT brokers. It both generation-guided and mutation-guided fuzzing techniques to craft fuzzy MQTT payloads to send to your target. It also leverages a response feedback mechanism for monitoring new behavior from the broker -- specifically, behavior in the form of MQTT responses and console responses (standard output). When FUME spots sufficiently new behavior, the responsible request to an input queue for further fuzzing later on.

FUME is modeled as a finite state machine using Markov modeling. Basically, FUME needs to make several choices during a single fuzzing round, such as whether to select mutation-guided or generation-guided fuzzing, which packet types to select or generate, how intensely to fuzz the input seed (and which fuzzing operations are carried out), etc. To illustrate this decision-making process, we model it as a stochastic process with several parameters that are fully configurable by the end user. For example, as shown in the figure above, the user could give `X1` a high probability (e.g., 0.9) and `X2` a low probability (e.g., 0.1). This would produce input seeds that are small (e.g., a single CONNECT packet) but heavily fuzzed. The full details of FUME are provided in the research paper, which will become available at a later date.

A demo of FUME can be viewed [on Youtube](https://www.youtube.com/watch?v=99gAayiIcEo).

## Get Started

## Configuring your Fuzzing Session

## Crash Triage

## Bugs Discovered with FUME

If you want to test FUME yourself on the same brokers we did, please refer to [this repository](https://github.com/PBearson/FUME_Targets).

* [CVE-2021-28166](https://nvd.nist.gov/vuln/detail/CVE-2021-28166): In Mosquitto v2.0.0 - 2.0.9, a null pointer dereference occurs when a client sends MQTT v5 CONNACK packet.
* [CVE-2021-34432](https://nvd.nist.gov/vuln/detail/CVE-2021-34432): In Mosquitto v2.0.7 and earlier, the server crashes if the client sends a PUBLISH packet with topic length = 0.
* [KMQTT broken pipe error](https://github.com/davidepianca98/KMQTT/commit/7a4e31567c1a850e86bdc0660e243e7e6e9a33cf): In KMQTT version 0.2.7 and earlier, the server may crash if it tries on send a packet (e.g., SUBACK) to a closed TCP connection.
* [aedes malformed DISCONNECT](https://github.com/mqttjs/mqtt-packet/pull/107): In aedes 0.45.0, the server may crash if a client tries to send a malformed DISCONNECT packet.
  * This is actually due to a bug in mqtt-tools 6.9.0, a node package which aedes depends on.
