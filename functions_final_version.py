from json.tool import main
import random
import copy
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from numpy.core.fromnumeric import argmin
import statistics
import time
import math

from sympy import sec


class Node:
    """Klasa reprezentująca węzeł listy jednokierunkowej."""

    def __init__(self, time=0, iteration_time=0, win_t=-1):  # samochód
        self.time = time
        self.next = None
        self.iteration_time = iteration_time
        self.win_t = win_t


class Window:
    """Klasa reprezentująca bramkę na autostradzie"""

    def __init__(self, window_type=None, windowtime=0, how_many_clients=0, is_client=0):  # okienko
        self.window_type = window_type
        self.windowtime = windowtime
        self.how_many_clients = how_many_clients
        self.is_client = is_client
        self.queue = SingleList()
        self.car = None


class SingleList:
    """Klasa reprezentująca całą listę jednokierunkową."""  # kolejka

    def __init__(self):
        self.head = None
        self.counters = 0
        self.is_open = 1

    def append_car(self, time, win_t_1):

        next_node = Node(time, win_t=win_t_1)

        if self.head is None:
            self.head = next_node
            self.counters = 1
        else:
            current_node = self.head
            while current_node.next is not None:
                current_node = current_node.next
            current_node.next = next_node
            next_node.next = None
            self.counters += 1

    def add_existing_car(self, car):

        if self.head is None or self.counters == 0:
            self.head = car
            self.counters = 1
        else:
            current_node = self.head

            licznik = 0
            while current_node.next is not None:
                current_node = current_node.next

            current_node.next = car
            car.next = None
            self.counters += 1
            return

    def length(self):
        current_node = self.head
        if self.head is None:
            return 0
        index = 1
        while current_node.next is not None:
            current_node = current_node.next
            index += 1
        return index

    def take_the_first_car(self):
        if self.counters == 1:
            node = self.head
            self.head = None
            self.counters -= 1
            node.next = None
            return node

        node = self.head
        self.head = self.head.next
        self.counters -= 1
        node.next = None
        return node

    def take_last_car(self):
        if self.counters == 1:
            self.counters -= 1
            current_node = self.head
            self.head = None
            return current_node

        if self.counters == 2:
            current_node = self.head.next
            self.head.next = None
            self.counters -= 1
            return current_node

        if self.counters > 2:

            current_node = self.head
            while current_node.next.next is not None:
                current_node = current_node.next
            self.counters -= 1
            node_to_return = current_node.next
            current_node.next = None
            return node_to_return

    def show(self):
        current_node = self.head
        print(current_node.time)
        while current_node.next is not None:
            print(current_node.next.time)
            current_node = current_node.next

    def plus_iteration_time(self):

        if self.counters == 1:
            self.head.iteration_time += 1
            return

        if self.counters == 2:
            self.head.iteration_time += 1
            self.head.next.iteration_time += 1

        else:
            current_node = self.head
            current_node.iteration_time += 1
            while current_node.next is not None:
                if current_node != self.head:
                    current_node.iteration_time += 1
                current_node = current_node.next
            return


def random_time():  
    return random.randint(1, 2)

def open_office(queue_0, office_1, queue_1, limit):

    windows_closed = 0
    iteration = 0
    car_times = []

    while 1:
        if windows_closed == len(office_1):
            break

        if queue_1.counters < limit:
            if queue_0.counters > 0:
                if queue_0.head.time == 0:
                    client = queue_0.take_the_first_car()
                    queue_1.add_existing_car(client)

        for i in range(len(office_1)):
            if office_1[i].windowtime == 0:
                if queue_1.counters > 0:

                    client = queue_1.take_the_first_car()
                    office_1[i].car = client

                    office_1[i].how_many_clients += 1
                    office_1[i].is_client = 1

                    office_1[i].windowtime = client.win_t

                else:
                    if queue_0.counters == 0 and queue_1.counters == 0:
                        office_1[i].windowtime = -2
                        windows_closed += 1

            if office_1[i].is_client == 1:
                office_1[i].windowtime -= 1
                office_1[i].car.iteration_time += 1

            if office_1[i].windowtime == 0:
                office_1[i].is_client = 0

                if office_1[i].car is not None:
                    car_times += [office_1[i].car.iteration_time]
                    office_1[i].car = None

        if queue_0.counters > 0 and queue_0.head.time > 0:
            queue_0.head.time -= 1

        if queue_1.counters > 0:
            queue_1.plus_iteration_time()
            
        iteration += 1

    return iteration, car_times


def open_office_seperate(queue_0, office_1, queue_1, limit, queues_length):

    windows_closed = 0
    iteration = 0
    client_from_0 = 0
    client_from_1 = 0
    car_times = []
    client_nr = 0

    while 1:
        windows_closed = 0

        if queue_0.counters == 0 and queue_1.counters == 0:
            for window in office_1:
                if window.windowtime == 0 and window.queue.counters == 0:
                    windows_closed += 1
        
            if windows_closed == len(office_1):
                break

        if queue_1.counters < limit:
            if queue_0.counters > 0:
                if queue_0.head.time == 0:

                    client = queue_0.take_the_first_car()
                    queue_1.add_existing_car(client)

                    client_from_0 += 1

        for j in range(len(office_1)):
            if queue_1.counters > 0:
                if office_1[j].windowtime == 0 and office_1[j].queue.counters == 0:
                    
                    office_1[j].queue.add_existing_car(queue_1.take_the_first_car())

        current_queue_lengths = []

        for j in range(len(office_1)):
            current_queue_lengths += [office_1[j].queue.counters]

        while queue_1.counters > 0 and sum(current_queue_lengths) < queues_length * len(office_1):

            shortest_queue_index = argmin(current_queue_lengths)

            if office_1[shortest_queue_index].queue.counters < queues_length:
       
                client = queue_1.take_the_first_car()

                office_1[shortest_queue_index].queue.add_existing_car(client)

                client_from_1 += 1
                current_queue_lengths[shortest_queue_index] += 1
    

        for i in range(len(office_1)):
            if office_1[i].windowtime == 0:
                if office_1[i].queue.counters > 0:

                    client = office_1[i].queue.take_the_first_car()
                    office_1[i].car = client

                    client_nr += 1

                    office_1[i].how_many_clients += 1
                    office_1[i].is_client = 1

                    if office_1[i].window_type == 'A':
                        office_1[i].windowtime = client.win_t

            if office_1[i].is_client == 1 and office_1[i].windowtime != 0:
                office_1[i].windowtime -= 1
                office_1[i].car.iteration_time += 1

            if office_1[i].windowtime == 0:
                office_1[i].is_client = 0

                if office_1[i].car is not None:
                    car_times += [office_1[i].car.iteration_time]
                    office_1[i].car = None

        if queue_0.counters > 0 and queue_0.head.time > 0:
            queue_0.head.time -= 1

        dic_of_trues = {}

        for i in range(len(office_1)):
            if office_1[i].queue.counters > 0:

                if i == 0:

                    if office_1[i].queue.counters - office_1[i + 1].queue.counters >= 2 or (
                            office_1[i + 1].windowtime == 0 and office_1[i + 1].queue.counters == 0):
                        client_to_change = office_1[i].queue.take_last_car()
                        office_1[i + 1].queue.add_existing_car(client_to_change)

                elif i == len(office_1) - 1:
                    if office_1[i].queue.counters - office_1[i - 1].queue.counters >= 2 or (
                            office_1[i - 1].windowtime == 0 and office_1[i - 1].queue.counters == 0):
                        client_to_change = office_1[i].queue.take_last_car()
                        office_1[i - 1].queue.add_existing_car(client_to_change)
                        
                else:
                    smaller_q = [office_1[i - 1].queue.counters, office_1[i + 1].queue.counters]

                    dic_of_trues['+'] = 0
                    dic_of_trues['-'] = 0
                    if office_1[i].queue.counters - office_1[i - 1].queue.counters >= 2 or (
                            office_1[i - 1].windowtime == 0 and office_1[i - 1].queue.counters == 0):
                        dic_of_trues['-'] = 1

                    elif office_1[i].queue.counters - office_1[i + 1].queue.counters >= 2 or (
                            office_1[i + 1].windowtime == 0 and office_1[i + 1].queue.counters == 0):
                        dic_of_trues['+'] = 1
                    
                    if len(dic_of_trues.keys()) == sum(dic_of_trues.values()):

                        client_to_change = office_1[i].queue.take_last_car()
                        office_1[smaller_q.index(min(smaller_q))].queue.add_existing_car(client_to_change)
                        
                    elif dic_of_trues['-'] == 1:
                        client_to_change = office_1[i].queue.take_last_car()
                        office_1[i - 1].queue.add_existing_car(client_to_change)
                    
                    elif dic_of_trues['+'] == 1:
                        client_to_change = office_1[i].queue.take_last_car()
                        office_1[i + 1].queue.add_existing_car(client_to_change)
                        
        for i in range(len(office_1)):
            if office_1[i].queue.counters > 0:
                office_1[i].queue.plus_iteration_time()

        if queue_1.counters > 0:
            queue_1.plus_iteration_time()

        iteration += 1

    return iteration, car_times

def generator_uniform(n):
    seed = int(time.time() * 1000) 
    list_of_numbers = []
    k = 4
    a = [3456, 567, 12890, 4567]
    b = 4443
    m = 10000
    list_of_numbers += [seed % m / (10**4)]

    for i in range(1,n):
        temp = b

        for j in range(k):
            if i-j-1 >= 0:
                temp += a[j]*list_of_numbers[i-j-1]

        temp = temp % m
        list_of_numbers += [temp/m]

    return list_of_numbers


def generator_normal(n):

    k = 12
    list_of_normal = []
    numbers_uniform = generator_uniform(k*n)
    j = 0

    for i in range(k, k*n, k):
        average_uniform = (sum(numbers_uniform[j:i]))/k
        final_number = (average_uniform - 0.5)/(math.sqrt(1/12))
        list_of_normal += [final_number]
        j = j + k

    return list_of_normal


