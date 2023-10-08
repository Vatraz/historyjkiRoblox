from enum import Enum


class Action(Enum):
    JOIN_ROOM = 'join room'
    LEAVE_ROOM = 'leave room'
    TURN_ON_CAMERA = 'turn on camera'
    TURN_OFF_CAMERA = 'turn off camera'
    CHANGE_SKIN = 'change skin'
