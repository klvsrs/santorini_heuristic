import gameEngine
import random
import concurrent.futures
from random import choice
from random import randint
from tqdm import tqdm

def run_single_game(p1_func, p2_func):
    s = gameEngine.gen_starting_state(2)
    latch = True
    p1_win = 0
    p2_win = 0
    while latch:
        action_list = gameEngine.gen_valid_moves(s)
        if len(action_list) == 0:
            s[1] = 'lose'
        else:
            if s[0] == 'p1':
                if p1_func == 0:
                    selected_index = randint(0, len(action_list)-1)
                elif p1_func == 1:
                    heuristic_list = []
                    for i in range(len(action_list)):
                        heuristic_list.append(gameEngine.f_heuristic(s,action_list,i))
                    max_value = max(heuristic_list)
                    max_value_indexes = [index for index, value in enumerate(heuristic_list) if value == max_value]
                    selected_index = choice(max_value_indexes)
                else:
                    heuristic_list = []
                    for i in range(len(action_list)):
                        heuristic_list.append(gameEngine.f_heuristic_god(s,action_list,i))
                    max_value = max(heuristic_list)
                    max_value_indexes = [index for index, value in enumerate(heuristic_list) if value == max_value]
                    selected_index = choice(max_value_indexes)
            else:
                if p2_func == 0:
                    selected_index = randint(0, len(action_list)-1)
                elif p2_func == 1:
                    heuristic_list = []
                    for i in range(len(action_list)):
                        heuristic_list.append(gameEngine.f_heuristic(s,action_list,i))
                    max_value = max(heuristic_list)
                    max_value_indexes = [index for index, value in enumerate(heuristic_list) if value == max_value]
                    selected_index = choice(max_value_indexes)
                else:
                    heuristic_list = []
                    for i in range(len(action_list)):
                        heuristic_list.append(gameEngine.f_heuristic_god(s,action_list,i))
                    max_value = max(heuristic_list)
                    max_value_indexes = [index for index, value in enumerate(heuristic_list) if value == max_value]
                    selected_index = choice(max_value_indexes)
            gameEngine.next_state(s,action_list,selected_index)
        if s[1] == 'win':
            if s[0] == 'p1':
                p1_win = p1_win + 1
            else:
                p2_win = p2_win + 1
            latch = False
        elif s[1] == 'lose':
            if s[0] == 'p2':
                p1_win = p1_win + 1
            else:
                p2_win = p2_win + 1
            latch = False
    return p1_win, p2_win


def run_games_batch(start_index, end_index):
    results = []
    for index in range(start_index, end_index):
        p1_func, p2_func = player_pairs[index]
        p1_win, p2_win = run_single_game(p1_func, p2_func)  # A function to simulate a batch of games and return results
        results.append((p1_func, p2_func, p1_win, p2_win))
    return results


random.seed(101)
function_name = ['random','norm heuristic','god heuristic']
function_arr = [0,1,2]
game_max = 10000000
batch_size = 10000
player_pairs = [(p1, p2) for p1 in range(len(function_name)) for p2 in range(len(function_name)) for i in range(game_max)]
indices = list(range(len(player_pairs)))
num_batches = len(player_pairs) // batch_size + (1 if len(player_pairs) % batch_size != 0 else 0)

print('Total Games: '+str(game_max*9))
print('Batch Size : '+str(batch_size))

with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
    future_to_batch = {executor.submit(run_games_batch, i * batch_size, min((i + 1) * batch_size, len(player_pairs))): i for i in range(num_batches)}
    results = []
    for future in tqdm(concurrent.futures.as_completed(future_to_batch), total=len(future_to_batch)):
        batch_result = future.result()
        results.extend(batch_result)

    sum_arr = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
    sum_cnt_p1 = [0,0,0,0,0,0,0,0,0]
    sum_cnt_p2 = [0,0,0,0,0,0,0,0,0]
    for i in range(len(sum_arr)):
        for j in range(len(results)):
            if sum_arr[i][0]==results[j][0] and sum_arr[i][1]==results[j][1]:
                if results[j][2]==1:
                    sum_cnt_p1[i] = sum_cnt_p1[i] + 1
                else:
                    sum_cnt_p2[i] = sum_cnt_p2[i] + 1
    function_name = ['random','norm heuristic','god heuristic']
    for i in range(len(sum_arr)):
        print('-----------')
        print('p1 func:'+function_name[sum_arr[i][0]])
        print('p2 func:'+function_name[sum_arr[i][1]])
        print('p1 win :'+str(sum_cnt_p1[i]))
        print('p2 win :'+str(sum_cnt_p2[i]))