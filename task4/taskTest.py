import random
import string
import time
from concurrent.futures import ThreadPoolExecutor

class BigBatchData:
    def __init__(self, data_number, data):
        self.data_number = data_number
        self.data = data

class BigBatch:
    def __init__(self, batch_size):
        self.batch_size = batch_size
        # 데이터를 한 번에 생성하여 슬라이싱
        full_data = ''.join(random.choices(string.ascii_lowercase + string.digits, k=batch_size * 10))
        self.data_batch = [BigBatchData(i, full_data[i*10:(i+1)*10]) for i in range(batch_size)]

    def bigBatchHandler(self):
        # 멀티스레딩을 사용한 데이터 처리
        with ThreadPoolExecutor() as executor:
            result = list(executor.map(self.process_data, self.data_batch))
        return result

    @staticmethod
    def process_data(data):
        return data.data.replace('f', '에프') if 'f' in data.data else data.data

# 실행 시간 측정 시작
start_time = time.perf_counter()

# BigBatch 인스턴스 생성 및 데이터 핸들링
batch_size = 500000
big_batch = BigBatch(batch_size)
modified_data = big_batch.bigBatchHandler()

# 실행 시간 측정 종료
end_time = time.perf_counter()
execution_time = end_time - start_time

print(f"Execution Time: {execution_time:.2f} seconds")
