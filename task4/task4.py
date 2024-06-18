import random
import string
import time
from abc import ABC, abstractmethod
from multiprocessing import Pool
from typing import List

import numpy as np


class Data:
    def __init__(self):
        self.data = self._generate_random_string(10)

    def _generate_random_string(self, length: int) -> str:
        characters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def get_data(self) -> str:
        return self.data


class BigBatch(ABC):
    @abstractmethod
    def init_data(self, size: int):
        pass

    @abstractmethod
    def big_batch_handler(self) -> List[str]:
        pass


class BigBatchArray(BigBatch):
    def __init__(self):
        self.data_batch = []

    def init_data(self, batch_size: int):
        self.data_batch = [Data() for _ in range(batch_size)]

    def big_batch_handler(self) -> List[str]:
        result = []
        for data in self.data_batch:
            modified_data = data.get_data().replace("f", "에프") if "f" in data.get_data() else data.get_data()
            result.append(modified_data)
        return result


class BigBatchList(BigBatch):
    def __init__(self):
        self.data_batch = []

    def init_data(self, batch_size: int):
        self.data_batch = [Data() for _ in range(batch_size)]

    def big_batch_handler(self) -> List[str]:
        return [data.get_data().replace("f", "에프") if "f" in data.get_data() else data.get_data() for data in
                self.data_batch]


class BigBatchMap(BigBatch):
    def __init__(self):
        self.data_batch = {}

    def init_data(self, batch_size: int):
        self.data_batch = {i: Data() for i in range(batch_size)}

    def big_batch_handler(self) -> List[str]:
        return [data.get_data().replace("f", "에프") if "f" in data.get_data() else data.get_data() for data in
                self.data_batch.values()]


class BigBatchThreadArray(BigBatch):
    def __init__(self):
        self.data_batch = []

    def init_data(self, batch_size: int):
        self.data_batch = [Data() for _ in range(batch_size)]

    def _process_data(self, data):
        return data.get_data().replace("f", "에프") if "f" in data.get_data() else data.get_data()

    def big_batch_handler(self) -> List[str]:
        num_cores = 4  # 사용할 프로세스 수
        df_split = np.array_split(self.data_batch, num_cores)  # 데이터를 나누기

        with Pool(num_cores) as pool:
            result = pool.map(self._process_data_batch, df_split)  # 병렬 처리

        return [item for sublist in result for item in sublist]  # 결과 합치기

    def _process_data_batch(self, data_batch):
        return [self._process_data(data) for data in data_batch]


def run(big_batch: BigBatch, time_list: List[float]):
    for _ in range(3):
        batch_size = 1000000

        start_time = time.perf_counter()

        big_batch.init_data(batch_size)
        modified_data = big_batch.big_batch_handler()

        end_time = time.perf_counter()
        execution_time = end_time - start_time

        print(f"Execution Time: {execution_time:.2f} seconds")
        time_list.append(execution_time)

    avg_time = sum(time_list) / len(time_list)
    print(f"avgTime = {avg_time} {big_batch.__class__.__name__}")
    time_list.clear()


if __name__ == "__main__":
    time_list = []

    big_batch_list = BigBatchList()
    run(big_batch_list, time_list)

    big_batch_thread_array = BigBatchThreadArray()
    run(big_batch_thread_array, time_list)


    big_batch_array = BigBatchArray()
    run(big_batch_array, time_list)

    big_batch_map = BigBatchMap()
    run(big_batch_map, time_list)
