import asyncio
import random
from server_execution import *

QUERY_TYPES = ['usr1', 'usr2', 'usr3']

NUM_QUERIES = 10

QUERY_PARAMS = {
    'usr1': {'time': 1, 'cpu_load': 10},
    'usr2': {'time': 2, 'cpu_load': 20},
    'usr3': {'time': 3, 'cpu_load': 70}
}


# def handle_query(q: dict):
#     print(q['type'])
#     time.sleep(q['time'])
#
#
# def async_handle_query(t: float):
#     asyncio.sleep(t)


def threads_server(query_list: list):
    server = ThreadServer()
    start_time = time.time()
    server.run(query_list)
    stop_time = time.time()
    print(f"Threads_time: {(stop_time - start_time):.3f} s")


def processes_server(query_list: list):
    server = ProcessServer()
    start_time = time.time()
    server.run(query_list)
    stop_time = time.time()
    print(f"Processes_time: {(stop_time - start_time):.3f} s")


async def async_server(query_list: list):

    start_time = time.time()
    task_list = []
    for q in query_list:
        print("Username:", q['type'], "sent request.", "Ex.type:async.")
        task = asyncio.create_task(asyncio.sleep(q['time']))
        task_list.append(task)

    for task in task_list:
        await task

    stop_time = time.time()
    print(f"Async_time: {(stop_time - start_time):.3f} s")


if __name__ == "__main__":

    q_list = []
    for i in range(NUM_QUERIES):
        query_type = random.choice(QUERY_TYPES)
        query_time = QUERY_PARAMS[query_type]['time']
        query_cpu_load = QUERY_PARAMS[query_type]['cpu_load']
        q_list.append({'type': query_type, 'time': query_time, 'cpu_load': query_cpu_load})

    sequential_server(q_list)
    threads_server(q_list)
    processes_server(q_list)
    asyncio.run(async_server(q_list))
    print(f"Initial time needed: {sum([q['time'] for q in q_list])} s")
