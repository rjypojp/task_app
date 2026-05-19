def create_events(tasks):
    return [
        {
            "title": task["title"],
            "start": task["deadline"]
        }
        for task in tasks
        if task["deadline"]
    ]  