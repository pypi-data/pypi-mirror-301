import typing

import numpy as np
from MrKWatkins.OakAsm.IO.ZXSpectrum.Z80Snapshot import Z80SnapshotFormat as DotNetZ80SnapshotFormat  # noqa
from MrKWatkins.OakEmu.Machines.ZXSpectrum import ZXSpectrum as DotNetZXSpectrum  # noqa
from MrKWatkins.OakEmu.Machines.ZXSpectrum.Screen import ScreenConverter as DotNetScreenConverter  # noqa
from System.IO import File  # noqa

from oakemu.machines.zxspectrum.keyboard import Keyboard
from oakemu.machines.zxspectrum.memory import Memory


class ZXSpectrum:
    def __init__(self, zx: DotNetZXSpectrum | None = None):
        self._zx = zx if zx else DotNetZXSpectrum.Create48k()
        self.memory = Memory(self._zx.Memory)
        self.keyboard = Keyboard(self._zx.Keyboard)

    def load_snapshot(self, path: str) -> None:
        file = File.OpenRead(path)
        try:
            snapshot = DotNetZ80SnapshotFormat.Instance.Read(file)
            self._zx.LoadSnapshot(snapshot)
        finally:
            file.Dispose()

    def set_program_counter(self, address: int) -> None:
        self._zx.Cpu.Registers.PC = address

    def get_pixel_colour_screenshot(
        self,
    ) -> np.ndarray[typing.Any, np.dtype[np.float64]]:
        pixel_colours = bytes(self._zx.GetScreenshot().ToPixelColourBytes())
        image_array = np.frombuffer(pixel_colours, dtype=np.uint8)
        return image_array.reshape((192, 256))  # Rows first, then columns. 192 arrays, each containing an array of 256 elements.

    def get_rgb_screenshot(self) -> np.ndarray[typing.Any, np.dtype[np.float64]]:
        rgb = bytes(self._zx.GetScreenshot().ToRgb24())
        image_array = np.frombuffer(rgb, dtype=np.uint8)
        return image_array.reshape((192, 256, 3))

    def get_screen(self) -> np.ndarray[typing.Any, np.dtype[np.float64]]:
        screen = bytes(self._zx.CopyScreen())
        return np.frombuffer(screen, dtype=np.uint8)

    def execute_frames(self, frames: int = 1) -> None:
        self._zx.ExecuteFrames(frames)
