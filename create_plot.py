import matplotlib.pyplot as plt

def create_plot(timestamps: list, title):
    # Separate timestamps into start and end times
    events = {}
    for event, elapsed_time, type in timestamps:
        if event not in events:
            events[event] = {'start': None, 'end': None}
        events[event][type] = elapsed_time

    # Create a Gantt chart with elapsed time in milliseconds
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, (event, times) in enumerate(events.items()):
        start = times['start']
        end = times['end']
        
        # Skip plotting if either start or end time is missing
        if start is None or end is None:
            print(f"Warning: Missing start or end time for event '{event}'")
            continue
        
        duration = end - start
        ax.barh(event, duration, left=start, align='center')

    # Setting labels for milliseconds display
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Event")
    plt.title(title or "Parallel Execution of Async Tasks (Time in ms)")
    plt.tight_layout()
    plt.show()
