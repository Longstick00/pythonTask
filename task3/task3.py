from abc import ABC, abstractmethod


class Task(ABC):
    def __init__(self):
        self.removed_odds = []

    @abstractmethod
    def remove_odds_with_loop(self):
        pass

    @abstractmethod
    def remove_odds_without_loop(self):
        pass

    @abstractmethod
    def add_back_removed_odd(self, number):
        pass

    def print_removed_odds_descending(self):
        self.removed_odds.sort(reverse=True)
        print("desc order:", " ".join(map(str, self.removed_odds)))
        self.removed_odds.sort()

    def _remove_if_odd(self, number):
        if number % 2 != 0:
            self.removed_odds.append(number)
            return True
        return False


class ListTask(Task):
    def __init__(self, size):
        super().__init__()
        self.my_data = [i for i in range(size)]

    def remove_odds_with_loop(self):
        for number in list(self.my_data):
            if number % 2 != 0:
                self.my_data.remove(number)
                self.removed_odds.append(number)

    def remove_odds_without_loop(self):
        self.my_data = [number for number in self.my_data if not self._remove_if_odd(number)]

    def add_back_removed_odd(self, number):
        if number in self.removed_odds:
            self.removed_odds.remove(number)
            self.my_data.append(number)
            self.my_data.sort()


class SetTask(Task):
    def __init__(self, size):
        super().__init__()
        self.my_data = {i for i in range(size)}

    def remove_odds_with_loop(self):
        for number in list(self.my_data):
            if number % 2 != 0:
                self.my_data.remove(number)
                self.removed_odds.append(number)

    def remove_odds_without_loop(self):
        self.my_data = {number for number in self.my_data if not self._remove_if_odd(number)}

    def add_back_removed_odd(self, number):
        if number in self.removed_odds:
            self.removed_odds.remove(number)
            self.my_data.add(number)


class DictTask(Task):
    def __init__(self, size):
        super().__init__()
        self.my_data = {i: i for i in range(size)}

    def remove_odds_with_loop(self):
        for number in list(self.my_data.keys()):
            if number % 2 != 0:
                del self.my_data[number]
                self.removed_odds.append(number)

    def remove_odds_without_loop(self):
        self.my_data = {number: number for number in self.my_data if not self._remove_if_odd(number)}

    def add_back_removed_odd(self, number):
        if number in self.removed_odds:
            self.removed_odds.remove(number)
            self.my_data[number] = number


def process_task(task, size):
    print(f"{type(task).__name__}:", task.my_data)

    # 1. Loop 직접 순회하며 홀수 삭제
    task.remove_odds_with_loop()

    # 초기화
    task = type(task)(size)

    # 2. Loop 직접 순회하지 않고 홀수 삭제
    task.remove_odds_without_loop()

    # 3. 삭제한 홀수들을 내림차순으로 출력
    task.print_removed_odds_descending()

    # 4. 삭제한 홀수들을 별도로 저장 후, 해당 자료구조에서 다시 삭제하면 원본의 자료구조에 생성
    delete_num = 5
    task.add_back_removed_odd(delete_num)

    print(f"{type(task).__name__} after adding back {delete_num}:", task.my_data)
    print(f"{type(task).__name__} after adding back {delete_num}:", task.removed_odds)
    print()


if __name__ == "__main__":
    size = 20
    process_task(ListTask(size), size)
    process_task(SetTask(size), size)
    process_task(DictTask(size), size)
