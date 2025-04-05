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
        self.logs = []
        self.__max_power = 20
        self.__running_since = datetime.datetime.now()

    def __str__(self):
        return f"RobotMock(temperature={self.temperature}, fan_speed={self.fan_speed}, state={self.state}, uptime={self.uptime})"

    def toJson(self):
        return {
            "temperature": self.temperature,
            "fan_speed": self.fan_speed,
            "state": self.state.name,
            "uptime": str(self.uptime),
            "power_consumption": self.power_consumption,
            "logs": self.logs,
        }

    @property
    def temperature(self):
        return self._temperature * (100 - (self._fan_speed / 2)) / 100

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
            self.log(f"Fan speed set to custom value {value}")
        else:
            self._fan_speed = self.power_consumption / self.__max_power * 100
            self.log(f"Fan speed set to linear value {self._fan_speed}")

    @property
    def state(self):
        return self._state

    def reset_timer(self):
        self.__running_since = datetime.datetime.now()

    @state.setter
    def state(self, value: State):
        if value != State.OFFLINE and self._state == State.OFFLINE:
            self.reset_timer()
        if not self.check_state(value):
            raise ValueError(
                f"Invalid state transition from {self._state.value} to {value.value}"
            )
        self.check_state(value)
        self._state = value
        self.log(f"State changed to {value.value}")

    # So here i don't understand because in the pdf it says
    # on/off →switch state of the robot from idle → running
    # reset → switch from error or idle → to idle
    # but it doesn't say anything about offline so i'm assuming that you have to turn on the robot before starting it
    # so like offline->idle->running->offline/idle
    # also nothing about error, so i'm assuming you can go from running to error and then to idle after reset

    def check_state(self, value):
        match self.state:
            case State.OFFLINE:
                if value != State.IDLE:
                    return False
            case State.IDLE:
                if value not in [State.RUNNING, State.OFFLINE]:
                    return False
            case State.RUNNING:
                if value not in [State.IDLE, State.ERROR, State.OFFLINE]:
                    return False
            case State.ERROR:
                if value not in [State.IDLE, State.OFFLINE]:
                    return False
        return True

    @property
    def uptime(self):
        if self._state == State.OFFLINE:
            return "N/A"
        else:
            return datetime.datetime.now() - self.__running_since

    def log(self, message):
        self.logs.append(f"{datetime.datetime.now()}: {message}")

    def clear_logs(self):
        self.logs = []
        self.log("Logs cleared")

    def reset(self):
        if self.state not in [State.ERROR, State.RUNNING]:
            raise ValueError("Cannot reset robot in current state")
        self.clear_logs()
        self.state = State.IDLE
        self.reset_timer()
