import datetime
import random
from enum import Enum
from time import sleep


# i'm wondering if the types in Robot state (current temperature in Celsius ( float16 )" are a hint to the usage of database
# but it was expected to setup a simple mock so i think db is too complex for a simple mock


class State(Enum):
    IDLE = "idle"
    RUNNING = "running"
    OFFLINE = "offline"
    ERROR = "error"


class RobotMock:
    def __init__(self):
        self._temperature = random.randint(20, 30)
        self._fan_speed = 0
        self._state = State.OFFLINE
        self._uptime = "N/A"
        self._fan_mode = "linear"

        self.__max_power = 20
        self.__running_since = datetime.datetime.now()

    def __str__(self):
        return f"RobotMock(temperature={self.temperature}, fan_speed={self.fan_speed}, state={self.state}, uptime={self.uptime})"

    def toJson(self):
        return {
            "temperature": self.temperature,
            "fan_speed": self.fan_speed,
            "state": self.state.value,
            "uptime": str(self.uptime),
            "power_consumption": self.power_consumption,
        }

    @property
    def temperature(self):
        return self._temperature * (1 - (self._fan_speed / 2))

    @property
    def power_consumption(self):
        match self._state:
            case State.IDLE | State.ERROR:
                return random.randint(7, 10)
            case State.RUNNING:
                return random.randint(15, self.__max_power)
            case State.OFFLINE:
                return "N/A"

    @property
    def fan_speed(self):
        return self._fan_speed

    def set_fan_speed(self, fan_mode, value=None):
        self._fan_mode = fan_mode
        if self._fan_mode != "linear":
            self._fan_speed = value
        else:
            self._fan_speed = self.power_consumption / self.__max_power * 100

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: State):
        if value != State.OFFLINE and self._state == State.OFFLINE:
            self.__running_since = datetime.datetime.now()
        self._state = value

    @property
    def uptime(self):
        if self._state == State.OFFLINE:
            return "N/A"
        else:
            return datetime.datetime.now() - self.__running_since


# robot = RobotMock()
# robot.state = State.IDLE
# print(robot)
# sleep(1)
# robot.set_fan_speed("custom", 0.5)
# print(robot)
# robot.set_fan_speed("custom", 0.5)
# print(robot)
