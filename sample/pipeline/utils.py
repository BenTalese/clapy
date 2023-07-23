import time

async def report_time(message: str):
    print(f"{message}{time.time()}!")
