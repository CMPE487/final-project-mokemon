from enum import Enum, auto
class State(Enum):
    ActionList = auto()
    CreateRoom = auto()
    ListRooms = auto()
    CreateTournament = auto()
    JoinTournament = auto()
    InRoom = auto()
    Battle = auto()