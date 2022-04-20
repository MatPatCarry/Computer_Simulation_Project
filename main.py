from functions_final_version import *

def main_zad(number_gates, full_len, frequency, first_stretch, second_stretch, service_times_common_queue,
             service_times_separate_queues, number_of_cars):
             
    office_common = []

    for i in range(number_gates):
        office_common += [Window('A', 0)]

    office_seperate = copy.deepcopy(office_common)

    finally_clients_common = []
    finally_clients_sepeate = []

    full_length = full_len

    queue_zero_common = SingleList()
    queue_zero_seperate = SingleList()

    queue_first_common = SingleList()
    queue_first_seperate = SingleList()

    freq_time_normal = generator_normal(number_of_cars + 1)
    freq_time_normal_2 = generator_normal(number_of_cars + 1)

    for i in range(number_of_cars):
        temp = int(freq_time_normal[i]*5 + frequency)
        temp_2 = int(freq_time_normal_2[i]*5 + frequency)
       
        queue_zero_common.append_car(time=temp, win_t_1=service_times_common_queue[i])
        queue_zero_seperate.append_car(time=temp_2, win_t_1=service_times_separate_queues[i])


    iteration_common, car_times_common = open_office(queue_zero_common, office_common, queue_first_common, limit=full_length)
    iteration_seperate, car_times_separate = open_office_seperate(queue_zero_seperate, office_seperate, queue_first_seperate, limit=first_stretch, queues_length=second_stretch)


    for i in office_common:
        finally_clients_common.append(i.how_many_clients)

    for i in office_seperate:
        finally_clients_sepeate.append(i.how_many_clients)

    return sum(car_times_common) / len(car_times_common), sum(car_times_separate) / len(car_times_separate)


'''
Plan badań
Typ planu - plan trzypoziomowy, całkowity
Zbadana dziedzina parametrów: 
Częstotliwość przyjazdów samochodów: min - 5 iteracji (5 sec) , max - 1800 iteracji (30min)
Liczba bramek: min - 2, max - 8
Czas obłsugi bramek: min - 30 (30 sec) , max - 600 (10min) iteracji
Długość odcinka całkowitego (podany w liczbie średniej długości aut) : min -  10, max - 60
Stosunek odcinka między pierwszym, a drugim checkpointem do odcinka między drugim checkpointem, a bramkami: min - 1/6, max - 5/6
Liczba układów eksperymentów : 3 ^ 3
'''

number_of_gates = [2, 5, 8]
car_coming_frequency = [5, 25, 45]
proportions = [1 / 6, 1 / 2, 5 / 6]
full_length_stretch = 60

all_three_experiments = []

for _ in range(5):
    experiment_result = []

    b = 500
    a = 10
    total_number_of_cars = 50
    service_times_common_queue = []
    service_times_separate_queues = []

    for i in range(total_number_of_cars):
        time_to_be_serviced_common_queue = int(((b - a) * random.betavariate(2, 5) + a).__round__(0))
        time_to_be_serviced_separate_queues = int(((b - a) * random.betavariate(2, 5) + a).__round__(0))

        service_times_common_queue.append(time_to_be_serviced_common_queue)
        service_times_separate_queues.append(time_to_be_serviced_separate_queues)


    for frequency in car_coming_frequency:
        for proportion in proportions:
            for gate in number_of_gates:

                current_arrangement = []
                first_stretch = int(proportion * full_length_stretch)
                second_stretch = int((1 - proportion) * full_length_stretch)
                
                if second_stretch == 9:
                    second_stretch = 10

                experiment_result += [main_zad(gate, full_length_stretch, frequency, first_stretch, second_stretch,
                                               service_times_common_queue=service_times_common_queue, service_times_separate_queues=service_times_separate_queues,
                                               number_of_cars=total_number_of_cars)]

    all_three_experiments.append(experiment_result)


final_result_to_show = []
common_queue_final_results = []
separate_queues_final_results = []
std_common = []
std_separate = []

for n in range(27):
    common_queue_final_results.append([])
    separate_queues_final_results.append([])

for idx, experiment in enumerate(all_three_experiments):
    for index in range(len(experiment)):
        common_queue_final_results[index].append(experiment[index][0])
        separate_queues_final_results[index].append(experiment[index][1])

copy_common_queue_final_results = copy.deepcopy(common_queue_final_results)
copy_separate_queue_final_results = copy.deepcopy(separate_queues_final_results)

for k in range(len(common_queue_final_results)):
    common_queue_final_results[k] = float('{:.2f}'.format(np.mean(common_queue_final_results[k]).round(2)))
    separate_queues_final_results[k] = float('{:.2f}'.format(np.mean(separate_queues_final_results[k]).round(2)))

for k in range(len(copy_common_queue_final_results)):
    std_common += [float('{:.2f}'.format(statistics.stdev(copy_common_queue_final_results[k])))]
    std_separate += [float('{:.2f}'.format(statistics.stdev(copy_separate_queue_final_results[k])))]

print(f'Common queue results:\n{common_queue_final_results}\n')
print(f'Separate queue results:\n{separate_queues_final_results}\n')

print(f'Standard variation of times - common queue:\n{std_common}\n')
print(f'Standard variation of times - separate queues:\n{std_separate}\n')

two_gates_results = []
five_gates_results = []
eight_gates_results = []

car_coming_frequency_strings = ['5', '25', '45']
x_ticks = np.arange(len(car_coming_frequency_strings))

i = 0
width = 0.25
start = 0
end = 3

plt.style.use('seaborn-darkgrid')
titles = ['Two', 'Five', 'Eight']
proportions_strings = ['1 / 5', '3 / 3', '5 / 1']
y_plus = [4, 3, 3]
x_minus = [0.3, 0.27, 0.27]
x_plus = [0.04, 0.04, 0.04]

axes_font = {'family': 'serif',
             'color': '#0C090A',
             'weight': 'normal',
             'size': 18,
             }

titles_font = {'family': 'serif',
               'color': '#0C090A',
               'weight': 'normal',
               'size': 22,
               }

subplot_title = {'family': 'serif',
                 'color': '#0C090A',
                 'weight': 'normal',
                 'size': 40,
                 }

for j in range(3):

    plt.subplot(1, 3, 1)
    plt.bar(x_ticks - 0.15, common_queue_final_results[start:end], width=width, color='#FF8040', edgecolor='black',
            label='Common queue')
    for inx1, result1 in enumerate(common_queue_final_results[start:end]):
        plt.text(x_ticks[inx1] - x_minus[j], result1 + y_plus[j], str(result1), fontsize=15)

    plt.bar(x_ticks + 0.15, separate_queues_final_results[start:end], width=width, color='#A74AC7', edgecolor='black',
            label='Separate queues')

    for inx2, result2 in enumerate(separate_queues_final_results[start:end]):
        plt.text(x_ticks[inx2] + x_plus[j], result2 + y_plus[j], str(result2), fontsize=15)

    common_queue_first_bar_height = max(common_queue_final_results[start:end])
    separate_queue_first_bar_height = max(separate_queues_final_results[start:end])
    first_highest_bar = max(common_queue_first_bar_height, separate_queue_first_bar_height)
    plt.ylim([0, first_highest_bar + first_highest_bar // 4])

    plt.legend(fontsize=20, loc='best')
    plt.title('Stretches proportions: ' + proportions_strings[0], fontdict=titles_font)
    plt.xlabel('Number of gates', fontdict=axes_font)
    plt.ylabel('Average time', fontdict=axes_font)
    plt.xticks(ticks=x_ticks, labels=titles, fontsize=15)
    plt.yticks(fontsize=15)


    plt.subplot(1, 3, 2)
    plt.bar(x_ticks - 0.15, common_queue_final_results[start + 3:end + 3], width=width, color='#FF8040',
            edgecolor='black', label='Common queue')

    for inx1, result1 in enumerate(common_queue_final_results[start + 3:end + 3]):
        plt.text(x_ticks[inx1] - x_minus[j], result1 + y_plus[j], str(result1), fontsize=15)

    plt.bar(x_ticks + 0.15, separate_queues_final_results[start + 3:end + 3], width=width, color='#A74AC7', edgecolor='black',
            label='Separate queues')

    for inx2, result2 in enumerate(separate_queues_final_results[start + 3:end + 3]):
        plt.text(x_ticks[inx2] + x_plus[j], result2 + y_plus[j], str(result2), fontsize=15)

    common_queue_second_bar_height = max(common_queue_final_results[start + 3:end + 3])
    separate_queue_second_bar_height = max(separate_queues_final_results[start + 3:end + 3])
    second_highest_bar = max(common_queue_second_bar_height, separate_queue_second_bar_height)
    plt.ylim([0, second_highest_bar + second_highest_bar // 4])

    plt.legend(fontsize=20, loc='best')
    plt.title('Stretches proportions: ' + proportions_strings[1], fontdict=titles_font)
    plt.xlabel('Number of gates', fontdict=axes_font)
    plt.ylabel('Average time', fontdict=axes_font)
    plt.xticks(ticks=x_ticks, labels=titles, fontsize=15)
    plt.yticks(fontsize=15)

    plt.subplot(1, 3, 3)
    plt.bar(x_ticks - 0.15, common_queue_final_results[start + 6:end + 6], width=width, color='#FF8040',
            edgecolor='black', label='Common queue')

    for inx1, result1 in enumerate(common_queue_final_results[start + 6:end + 6]):
        plt.text(x_ticks[inx1] - x_minus[j], result1 + y_plus[j], str(result1), fontsize=15)

    plt.bar(x_ticks + 0.15, separate_queues_final_results[start + 6:end + 6], width=width, color='#A74AC7', edgecolor='black',
            label='Separate queues')

    for inx2, result2 in enumerate(separate_queues_final_results[start + 6:end + 6]):
        plt.text(x_ticks[inx2] + x_plus[j], result2 + y_plus[j], str(result2), fontsize=15)

    common_queue_third_bar_height = max(common_queue_final_results[start + 6:end + 6])
    separate_queue_third_bar_height = max(separate_queues_final_results[start + 6:end + 6])
    third_highest_bar = max(common_queue_third_bar_height, separate_queue_third_bar_height)
    plt.ylim([0, third_highest_bar + third_highest_bar // 4])

    plt.legend(fontsize=20, loc='best')
    plt.title('Stretches proportions: ' + proportions_strings[2], fontdict=titles_font)
    plt.xlabel('Number of gates', fontdict=axes_font)
    plt.ylabel('Average time', fontdict=axes_font)
    plt.xticks(ticks=x_ticks, labels=titles, fontsize=15)
    plt.yticks(fontsize=15)

    plt.suptitle('Car coming frequency in iterations: '+car_coming_frequency_strings[j], fontsize=40, fontweight='bold')
    plt.show()

    start += 9
    end += 9