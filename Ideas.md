# Ideas for FUME

This is a list of some ideas I have for FUME, written in the order in which I am most likely to add them.

## Add `ENFORCE_MAXIMUM_PAYLOAD` option

Currently, there may be cases where the payload can exceed `MAXIMUM_PAYLOAD_LENGTH`, which may not be desirable. For example, suppose that before executing the BOF state, the payload size is 200 bytes; after executing the BOF state, the payload is now 600 bytes. If `MAXIMUM_PAYLOAD_LENGTH` is set to 500, then the payload will not execute any more states that increase the payload size, but the payload size will remain at 600 bytes. It would be nice to have an option that forces the payload size to never exceed `MAXIMUM_PAYLOAD_LENGTH`. A simple implementation is to just truncate the payload immediately before we send it to the broker.

## ADD `MINIMUM_PAYLOAD_SIZE` and `ENFORCE_MINIMUM_PAYLOAD` options

Since we already have an option for restricting how large a payload can get, a logical next step is to restrict how _small_ a payload can get (so that the Delete state does not remove too many bytes). Of course, this raises a question: How do we pad the payload when it too small? By default, we can probably just pad it with 0's. Maybe the pad byte can be selected by the user, though it probably won't make too much difference.

## Add `CHOOSE_NETWORK_RESPONSE` option (alternatively, split `b` into `b1` and `b2`)

Right now, when the fuzzer selects an input from the response log, the chance of selecting from the network response log is 50% (same with console response log, obviously). There is no reason why the user should not be able to set this probability. In truth, this also probably warrants a modification to the Markov model.

## Prioritize inputs from the response log according to the order they are found

Inputs from the response log are selected completely randomly, regardless of when they are discovered or any other factors. It would be much better to select these inputs in the order that they are found. A circular queue will get the job done.

## Verify console responses

To monitor console responses, FUME executes the target as a process a thread to monitor its output. Since this thread runs asynchronously to the main fuzzing script, it is possible for the payload to reset before the console response is received and processed. To avoid this, we should verify which input triggers the console response in question. If none of the tested inputs trigger the console response, then chances are likely either 1) it was not directly caused by the user's input, or 2) it was a state-dependent response. In either case, that response cannot possibly be represented by a single input, so we ignore it.
