from blessed import Terminal
import pickle


def load_from_pickle(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data


def format_worker(s):
    if s == '':
        return '    '
    else:
        return s

def get_color(term, value):
    # Determine the color based on the integer value
    colors = {
        0: term.normal,
        1: term.blue,
        2: term.purple,
        3: term.gold,
        4: term.red
    }
    return colors.get(value, term.normal)


def get_color_worker(term, value):
    # Determine the color based on the integer value
    colors = {
        '': term.normal,
        'p1w1': term.aqua,
        'p1w2': term.bright_cyan,
        'p2w1': term.green,
        'p2w2': term.bright_green
    }
    return colors.get(value, term.normal)

def draw_info(term, turn, player,action, act_wrk,player_1_god,player_2_god):
    print('Turn          :'+str(turn+1))
    print('Player        :'+player)
    print('Player 1 God  :'+player_1_god)
    print('Player 2 God  :'+player_2_god)
    print('Action        :'+action)
    print('Active Worker :'+act_wrk)

def draw_grid(term, state):
    x = 0
    for i in range(16):
        if i in (0,3,6,9,12,15):
            print('+------+------+------+------+------+')
            if x != 5:
                print('|'+str(x)+',0   '+'|'+str(x)+',1   '+'|'+str(x)+',2   '+'|'+str(x)+',3   '+'|'+str(x)+',4   |')
                x = x+1
        elif i in (1,4,7,10,13):
            l_index = i // 3
            row = '|'
            for j in range(5):
                value = state[4][l_index][j]
                color = get_color(term, value)
                row += color+'H:'+str(value)+'   '+ term.normal+'|'
            print(row)
        else:
            l_index = (i - 2) // 3
            row = '|'
            for j in range(5):
                worker = format_worker(state[5][l_index][j])
                color_func = get_color_worker(term, state[5][l_index][j])  # Get the color function
                row += color_func+'W:'+worker+term.normal+'|'
            print(row)


def draw_ai_info(term, file_loc):
    t_arr = file_loc.split('_')
    function_name = ['random','norm heuristic','god heuristic']
    print('Player 1 Heuristic :'+function_name[int(t_arr[3])])
    print('Player 2 Heuristic :'+function_name[int(t_arr[4])])

def draw_heuristic_info(term, s):
    if (s[1] == 'move' or s[1] == 'build') and len(s)==9:
        print('Action Choosen: '+str(s[6]))
        for i in range(len(s[7])):
            joined_str = ','.join([str(item) for item in s[7][i]])
            if len(s[8])>1:
                print(str(i)+':'+joined_str+' HVal:' + str(s[8][i]))
            else:
                print(str(i)+':'+joined_str+' HVal: 0')
def clear_screen():
    term = Terminal()
    print(term.home + term.clear)


if __name__ == '__main__':
    term = Terminal()
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        file_loc = 'saved_state/game_state_1_0_0.pkl'
        s = load_from_pickle(file_loc)
        show_index = 0
        draw_info(term,show_index,s[show_index][0],s[show_index][1],s[show_index][2],s[show_index][3][0][1],s[show_index][3][1][1])
        draw_grid(term,s[show_index])
        draw_ai_info(term, file_loc)
        if len(s[show_index])>6:
            draw_heuristic_info(term, s[show_index])
        while True:
            key = term.inkey(timeout=5)  # Wait for a single keypress
            #left
            if key.lower() == 'a':
                if show_index > 0:
                    show_index = show_index - 1
                else:
                    show_index = len(s)-1
                clear_screen()
                draw_info(term,show_index,s[show_index][0],s[show_index][1],s[show_index][2],s[show_index][3][0][1],s[show_index][3][1][1])
                draw_grid(term,s[show_index])
                draw_ai_info(term, file_loc)
                if len(s[show_index])>6:
                    draw_heuristic_info(term, s[show_index])
            elif key.lower() == 'd':
                if show_index < len(s)-1:
                    show_index = show_index + 1
                else:
                    show_index = 0
                clear_screen()
                draw_info(term,show_index,s[show_index][0],s[show_index][1],s[show_index][2],s[show_index][3][0][1],s[show_index][3][1][1])
                draw_grid(term,s[show_index])
                draw_ai_info(term, file_loc)
                if len(s[show_index])>6:
                    draw_heuristic_info(term, s[show_index])
            elif key.lower() == 'q':
                print("Quitting.")
                break
