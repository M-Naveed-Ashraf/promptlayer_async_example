import time

def log_time( timestamps: list, start_time, event_name, start=True,):
    current_time = time.time()
    elapsed_time = (current_time - start_time) * 1000  # Convert to milliseconds
    timestamps.append((event_name, elapsed_time, 'start' if start else 'end'))
    return current_time
