from enum import IntEnum

from MrKWatkins.OakEmu.Machines.ZXSpectrum.Games import ManicMiner as CSharpManicMiner  # noqa

from oakemu.machines.zxspectrum.game import Game


class ManicMinerAction(IntEnum):
    NONE = (0,)
    MOVE_LEFT = (1,)
    MOVE_RIGHT = (2,)
    JUMP_UP = (3,)
    JUMP_LEFT = (4,)
    JUMP_RIGHT = 5


class ManicMiner(Game):
    def __init__(self):
        super().__init__(CSharpManicMiner(), ManicMinerAction)
