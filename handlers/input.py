import tcod.event
from typing import Dict

from game_states import GameStates


class InputHandler(tcod.event.EventDispatch):
    def __init__(self):
        self._input_queue = []
        self.state: GameStates = GameStates.PLAYERS_TURN

    def ev_quit(self, event: tcod.event.Quit) -> None:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        print('ev_keydown', event)
        if self.state == GameStates.MAIN_MENU:
            self.handle_main_menu(event)

    def get_user_input(self) -> Dict:
        if self._input_queue:
            return self._input_queue.pop(0)
        else:
            return {}

    def handle_main_menu(self, event: tcod.event.KeyDown) -> None:
        if event.sym == tcod.event.K_a:
            self._input_queue.append({'new_game': True})
        elif event.sym == tcod.event.K_b:
            self._input_queue.append({'load_game': True})
        elif event.sym in (tcod.event.K_c, tcod.event.K_ESCAPE):
            self._input_queue.append({'exit_game': True})

    def set_game_state(self, state: GameStates) -> None:
        self.state = state
