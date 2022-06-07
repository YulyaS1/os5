import threading
from collections import deque
from random import randint
from time import sleep


def add(num, event):
    global queue, is_sleeping
    while not event.wait(3):
        with locker:
            if not is_sleeping and len(queue) < 99:
                queue.append(randint(1, 100))
                print(f"Производитель {num} добавил: {queue[-1]}, длина: {len(queue)}")
                if len(queue) >= 99:
                    is_sleeping = True
            else:
                if len(queue) <= 80:
                    is_sleeping = False


def take(num, event):
    global queue
    sleep(3)
    while len(queue) > 0 and not event.wait(3):
        with locker:
            print(f"Потребитель {num} забрал: {queue[0]}")
            queue.popleft()
    if event:
        while len(queue) != 0:
            with locker:
                if len(queue) != 0:
                    print(f"Потребитель {num} забрал: {queue[0]}")
                    queue.popleft()
            sleep(2)


is_sleeping = False
locker = threading.Lock()
event = threading.Event()
queue = deque([], 200)
for i in range(3):
    t = threading.Thread(target=add, name=f'Производитель {i + 1}', args=(i+1, event)).start()
for i in range(2):
    t = threading.Thread(target=take, name=f'Потребитель {i + 1}', args=(i+1, event)).start()
letter = ''
while letter != 'q':
    letter = input()
event.set()
print("Текущая очередь:", queue, "\n")