import abc
from enum import IntEnum

from MrKWatkins.OakEmu.Machines.ZXSpectrum.Game import Game as DotNetGame  # noqa

from oakemu.machines.zxspectrum.stepresult import StepResult
from oakemu.machines.zxspectrum.zxspectrum import ZXSpectrum


class Game(metaclass=abc.ABCMeta):  # noqa: B024
    def __init__(self, game: DotNetGame, action):
        if not issubclass(action, IntEnum):
            raise TypeError("action is not an IntEnum.")

        game.InitializeAsync().Wait()

        self._game = game
        self._zx = ZXSpectrum(game.Spectrum)
        self._actions = [e for e in action]

    @property
    def spectrum(self) -> ZXSpectrum:
        return self._zx

    @property
    def name(self) -> str:
        return self._game.Name

    @property
    def actions(self) -> list:
        return self._actions

    def reset(self) -> None:
        self._game.reset()

    def start_episode(self) -> None:
        self._game.StartEpisode()

    def execute_step(self, action_index: int | None) -> StepResult:
        return StepResult(self._game.ExecuteStep(action_index))

    def get_random_action(self) -> str | None:
        return self._game.GetRandomAction()
