from abc import ABC
import time
import threading
import multiprocessing


def sequential_server(query_list: list):
    start_time = time.time()
    for q in query_list:
        print("Username:", q['type'], "sent request.", "Ex.type:seq.")
        time.sleep(q['time'])
        print("Username:", q['type'], "request complete.", "Ex.type:seq.")

    stop_time = time.time()
    print(f"Sequential_time: {(stop_time - start_time):.3f} s")


class Server(ABC):
    def __init__(self) -> None:
        super(ABC).__init__()


    def processing(self, q: dict):
        print("  ", q['type'])
        time.sleep(q['time'])


class ThreadServer(Server):
    def __init__(self) -> None:
        super().__init__()
        self.load = 0
        self.load_cond = threading.Condition()

    def processing(self, q: dict):

        if self.load + q['cpu_load'] > 100:
            print('T: overloaded \n')
            with self.load_cond:
                self.load_cond.wait()

        self.load += q['cpu_load']
        print("Username:", q['type'], "sent request.", "Ex.type:thrd.")
        time.sleep(q['time'])
        self.load -= q['cpu_load']
        print("Username:", q['type'], "request complete.", "Ex.type:thrd.")
        with self.load_cond:
            self.load_cond.notify()

    def run(self, list_of_query: list):
        thread_list = []
        for q in list_of_query:
            thread = threading.Thread(
                target=self.processing, args=(q,), daemon=False)
            thread_list.append(thread)
            thread.start()

        for thread in thread_list:
            thread.join()


class ProcessServer(Server):
    def __init__(self) -> None:
        super().__init__()
        self.load = 0
        self.load_cond = multiprocessing.Condition()

    def processing(self, q: dict):
        if self.load + q['cpu_load'] > 100:
            print('P: overloaded \n')
            with self.load_cond:
                self.load_cond.wait()

        self.load += q['cpu_load']
        print("Username:", q['type'], "sent request.", "Ex.type:proc.")
        time.sleep(q['time'])
        self.load -= q['cpu_load']
        print("Username:", q['type'], "request complete.", "Ex.type:proc.")
        with self.load_cond:
            self.load_cond.notify()

    def run(self, list_of_query: list):
        p_list = []
        for q in list_of_query:
            p = multiprocessing.Process(
                target=self.processing, args=(q,), daemon=False)
            p_list.append(p)
            p.start()

        for p in p_list:
            p.join()