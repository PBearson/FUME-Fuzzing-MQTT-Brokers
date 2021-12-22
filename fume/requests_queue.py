import globals as g
import helper_functions.print_verbosity as pv

# Push to the requests queue
def push(request):
    if len(g.request_queue) == g.REQUEST_QUEUE_SIZE:
        g.request_queue.pop(0)
    g.request_queue.append(request)

# Print requests queue
def print_queue():
    if len(g.request_queue) == 0:
        return

    pv.normal_print("Request queue (starting from most recent):")
    g.request_queue.reverse()
    for index, req in enumerate(g.request_queue):
        pv.normal_print("%d: %s" % (index, req.hex()))

    # TODO dump request queue to file - if we restart the target,
    # then each queue should be stored in a new file.
    # TODO make request queue size a config var