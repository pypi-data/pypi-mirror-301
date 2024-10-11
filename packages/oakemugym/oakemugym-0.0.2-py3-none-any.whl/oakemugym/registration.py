from collections.abc import Sequence
from typing import NamedTuple

import gymnasium


class EnvConfig(NamedTuple):
    version: str


def register_envs(games: Sequence[str], obs_types: Sequence[str], configs: Sequence[EnvConfig]):
    for game in games:
        for obs_type in obs_types:
            for config in configs:
                gymnasium.register(
                    id=f"{game}-{config.version}",
                    entry_point="oakemugym:OakEmuEnv",
                    kwargs=dict(
                        game_type=game,
                        obs_type=obs_type,
                    ),
                )


def register():
    games = ["ManicMiner"]
    obs_types = ["ram", "rgb", "spectrum"]
    versions = [EnvConfig(version="v0")]

    register_envs(games, obs_types, versions)
