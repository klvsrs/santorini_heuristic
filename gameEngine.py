from itertools import combinations


def gen_starting_state(n):
    return [
        'p1',
        'pick god',
        '',
        [['p{}'.format(i+1), ''] for i in range(n)],
        [[0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0]],
        [['', '', '', '', ''],
         ['', '', '', '', ''],
         ['', '', '', '', ''],
         ['', '', '', '', ''],
         ['', '', '', '', '']]
    ]


def gen_god():
    return ['Appolo', 'Atlas']


def gen_place_worker(state):
    action_list = []
    for i in range(5):
        for j in range(5):
            if state[5][i][j] == '':
                action_list.append([i, j])
    worker_combinations = list(combinations(action_list, 2))
    return worker_combinations


def get_worker_loc(state, worker_id):
    for i in range(5):
        for j in range(5):
            if state[5][i][j] == worker_id:
                return i,j


def gen_worker_move(state):
    action_list = []
    for w in range(2):
        worker_id = state[0]+'w'+str(w+1)
        i, j = get_worker_loc(state, worker_id)
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if 0 <= i + x <= 4 and 0 <= j + y <= 4 and not (x == 0 and y == 0):
                    if state[5][i+x][j+y] == '' and state[4][i+x][j+y] != 4 and (state[4][i][j]+1 == state[4][i+x][j+y] or state[4][i][j] >= state[4][i+x][j+y]):
                        action_list.append([worker_id, i+x, j+y])
    return action_list


def gen_worker_build(state):
    action_list = []
    worker_id = state[2]
    i, j = get_worker_loc(state, worker_id)
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            if 0 <= i + x <= 4 and 0 <= j + y <= 4 and not (x == 0 and y == 0):
                if state[5][i+x][j+y] == '' and state[4][i+x][j+y] != 4:
                    action_list.append([i+x, j+y])
    return action_list


def gen_valid_moves(state):
    if state[1] == 'pick god':
        return gen_god()
    elif state[1] == 'place worker':
        return gen_place_worker(state)
    elif state[1] == 'move':
        return gen_worker_move(state)
    elif state[1] == 'build':
        return gen_worker_build(state)


def next_player(state):
    for i in range(len(state[3])):
        if state[3][i][0] == state[0]:
            if i+1 == len(state[3]):
                state[0] = state[3][0][0]
            else:
                state[0] = state[3][i+1][0]
            break
    return state


def f_heuristic(state, list_action, action):
    heuristic = 0
    if len(list_action) != 0:
        if state[1] == 'move':
            target_height = state[4][list_action[action][1]][list_action[action][2]]
            if target_height == 0:
                heuristic = 1
            elif target_height == 1:
                heuristic = 2
            elif target_height == 2:
                heuristic = 5
            elif target_height == 3:
                heuristic = 100
        elif state[1] == 'build':
            i, j = get_worker_loc(state, state[2])
            current_height = state[4][i][j]
            target_height = state[4][list_action[action][0]][list_action[action][1]]
            if current_height == target_height:
                if target_height == 0:
                    heuristic = 1
                elif target_height == 1:
                    heuristic = 2
                elif target_height == 1:
                    heuristic = 5
    return heuristic


def next_state(state, list_action, action):
    if len(list_action) == 0:
        state[1] = 'lose'
    elif state[1] == 'pick god':
        for i in range(len(state[3])):
            if state[3][i][0] == state[0]:
                state[3][i][1] = list_action[action]
                state = next_player(state)
                if i+1 == len(state[3]):
                    state[1] = 'place worker'
                break
    elif state[1] == 'place worker':
        state[5][list_action[action][0][0]][list_action[action][0][1]] = state[0]+'w1'
        state[5][list_action[action][1][0]][list_action[action][1][1]] = state[0]+'w2'
        count = 0
        for i in range(5):
            for j in range(5):
                if state[5][i][j] != '':
                    count = count+1
        if count == len(state[3])*2:
            state[1] = 'move'
        state = next_player(state)
    elif state[1] == 'move':
        i, j = get_worker_loc(state, list_action[action][0])
        temp_w = state[5][i][j]
        state[5][i][j] = state[5][list_action[action][1]][list_action[action][2]]
        state[5][list_action[action][1]][list_action[action][2]] = temp_w
        state[2] = list_action[action][0]
        if state[4][list_action[action][1]][list_action[action][2]] == 3:
            state[1] = 'win'
        else:
            state[1] = 'build'
    elif state[1] == 'build':
        state[4][list_action[action][0]][list_action[action][1]] = state[4][list_action[action][0]][list_action[action][1]]+1
        state[2] = ''
        state[1] = 'move'
        state = next_player(state)
    return state
