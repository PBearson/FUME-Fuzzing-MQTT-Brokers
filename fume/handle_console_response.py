def handle_console_response(proc):
    for line in iter(proc.stdout.readline, b''):
        # TODO add similarity threshold to config file
        # TODO log line if it is unique enough
        pass