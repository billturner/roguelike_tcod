import tcod.event
from typing import Dict

from game_states import GameStates


class InputHandler(tcod.event.EventDispatch):
    def __init__(self):
        self._input_queue = []
        self.state: GameStates = GameStates.PLAYERS_TURN

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        if self.state == GameStates.PLAYERS_TURN:
            self.handle_player_turn_keys(event)
        elif self.state == GameStates.CHARACTER_SCREEN:
            self.handle_character_screen_keys(event)
        elif self.state == GameStates.MAIN_MENU:
            self.handle_main_menu(event)
        elif self.state == GameStates.LEVEL_UP:
            self.handle_level_up_menu(event)
        elif self.state == GameStates.PLAYER_DEAD:
            self.handle_player_dead_keys(event)
        elif self.state == GameStates.TARGETING:
            self.handle_player_targeting_keys(event)
        elif self.state in (GameStates.DROP_INVENTORY, GameStates.SHOW_INVENTORY):
            self.handle_inventory_keys(event)

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> None:
        if self.state == GameStates.TARGETING:
            x, y = event.tile
            if event.button == tcod.event.BUTTON_LEFT:
                self._input_queue.append({'left_click': (x, y)})
            elif event.button == tcod.event.BUTTON_RIGHT:
                self._input_queue.append({'right_click': (x, y)})

    def ev_quit(self, event: tcod.event.Quit) -> None:
        raise SystemExit()

    def get_user_input(self) -> Dict:
        if self._input_queue:
            return self._input_queue.pop(0)
        else:
            return {}

    def handle_character_screen_keys(self, event: tcod.event.KeyDown) -> None:
        if event.sym == tcod.event.K_ESCAPE:
            self._input_queue.append({'exit': True})

    def handle_inventory_keys(self, event: tcod.event.KeyDown) -> None:
        index = event.sym - ord('a')

        if index >= 0:
            self._input_queue.append({'inventory_index': index})
        elif event.sym == tcod.event.K_ESCAPE:
            self._input_queue.append({'exit': True})

    def handle_level_up_menu(self, event: tcod.event.KeyDown) -> None:
        if event.sym == tcod.event.K_a:
            self._input_queue.append({'level_up': 'hp'})
        elif event.sym == tcod.event.K_b:
            self._input_queue.append({'level_up': 'str'})
        elif event.sym == tcod.event.K_c:
            self._input_queue.append({'level_up': 'def'})

    def handle_main_menu(self, event: tcod.event.KeyDown) -> None:
        if event.sym == tcod.event.K_a:
            self._input_queue.append({'new_game': True})
        elif event.sym == tcod.event.K_b:
            self._input_queue.append({'load_game': True})
        elif event.sym in (tcod.event.K_c, tcod.event.K_ESCAPE):
            self._input_queue.append({'exit_game': True})

    def handle_player_dead_keys(self, event: tcod.event.KeyDown) -> None:
        if event.sym == tcod.event.K_1:
            self._input_queue.append({'show_inventory': True})
        elif event.sym == tcod.event.K_ESCAPE:
            self._input_queue.append({'exit': True})

    def handle_player_targeting_keys(self, event: tcod.event.KeyDown) -> None:
        if event.sym == tcod.event.K_ESCAPE:
            self._input_queue.append({'exit': True})

    def handle_player_turn_keys(self, event: tcod.event.KeyDown) -> None:
        if event.sym == tcod.event.K_UP or event.sym == tcod.event.K_k:
            self._input_queue.append({"move": (0, -1)})
        elif event.sym == tcod.event.K_DOWN or event.sym == tcod.event.K_j:
            self._input_queue.append({"move": (0, 1)})
        elif event.sym == tcod.event.K_LEFT or event.sym == tcod.event.K_h:
            self._input_queue.append({"move": (-1, 0)})
        elif event.sym == tcod.event.K_RIGHT or event.sym == tcod.event.K_l:
            self._input_queue.append({"move": (1, 0)})
        elif event.sym == tcod.event.K_y:
            self._input_queue.append({'move': (-1, -1)})
        elif event.sym == tcod.event.K_u:
            self._input_queue.append({'move': (1, -1)})
        elif event.sym == tcod.event.K_b:
            self._input_queue.append({'move': (-1, 1)})
        elif event.sym == tcod.event.K_n:
            self._input_queue.append({'move': (1, 1)})
        elif event.sym == tcod.event.K_z:
            self._input_queue.append({'wait': True})

        elif event.sym == tcod.event.K_RETURN:
            self._input_queue.append({'take_stairs': True})

        elif event.sym == tcod.event.K_g:
            self._input_queue.append({'pickup': True})

        elif event.sym == tcod.event.K_i:
            self._input_queue.append({'show_inventory': True})

        elif event.sym == tcod.event.K_d:
            self._input_queue.append({'drop_inventory': True})

        elif event.sym == tcod.event.K_c:
            self._input_queue.append({'show_character_screen': True})

        elif event.sym == tcod.event.K_ESCAPE:
            self._input_queue.append({"exit": True})

    def set_game_state(self, state: GameStates) -> None:
        self.state = state
