from environs import Env
from dataclasses import dataclass


@dataclass
class Key:
    secret_key: str


@dataclass
class Settings:
    key: Key


def get_key(path: str):
    env = Env()
    env.read_env(path)
    return Settings(
        key=Key(
            secret_key=env.str('KEY')
        )
    )


# print(get_key('../Danger').key.key)
