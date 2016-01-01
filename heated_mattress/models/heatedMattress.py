import pickle
import time
import os
import wiringpi2
from time import sleep


# TODO make ABC of HeatedMattress and make this an AveragingHeatedMattress
class HeatedMattress:
    """
    HeatedMattress provides basic power manipulation for a heated mattress.
    this class will also serve as basis for future TemperatureHeatedMattress, which will include
    a feedback circuit for monitoring temperature
    """

    # At the moment, rather than generating pulses we are using a replay attack to play one of
    # 10 pre-recorded pulses. This is a prototype, and will change once signal analysis provides
    # an algorithm for generation of pulse
    # Load the off pickled data

    dir = os.path.join(os.path.dirname(__file__), '../resources/pulseData/')

    pulse_file = open(os.path.join(dir, 'off1.200k.wav.pkl'), 'rb')
    off_pulse_data = pickle.load(pulse_file)
    pulse_file.close()

    # Load the all on pickled datas
    pulse_file = open(os.path.join(dir, 'on_111_111.pkl'), 'rb')
    on_1_pulse_data = pickle.load(pulse_file)
    pulse_file.close()

    pulse_file = open(os.path.join(dir, 'on_222_222.pkl'), 'rb')
    on_2_pulse_data = pickle.load(pulse_file)
    pulse_file.close()

    pulse_file = open(os.path.join(dir, 'on_333_333.pkl'), 'rb')
    on_3_pulse_data = pickle.load(pulse_file)
    pulse_file.close()

    pulse_file = open(os.path.join(dir, 'on_444_444.pkl'), 'rb')
    on_4_pulse_data = pickle.load(pulse_file)
    pulse_file.close()

    pulse_file = open(os.path.join(dir, 'on_555_555.pkl'), 'rb')
    on_5_pulse_data = pickle.load(pulse_file)
    pulse_file.close()

    pulse_file = open(os.path.join(dir, 'on_666_666.pkl'), 'rb')
    on_6_pulse_data = pickle.load(pulse_file)
    pulse_file.close()

    pulse_file = open(os.path.join(dir, 'on_777_777.pkl'), 'rb')
    on_7_pulse_data = pickle.load(pulse_file)
    pulse_file.close()

    pulse_file = open(os.path.join(dir, 'on_888_888.pkl'), 'rb')
    on_8_pulse_data = pickle.load(pulse_file)
    pulse_file.close()

    pulse_file = open(os.path.join(dir, 'on_999_999.pkl'), 'rb')
    on_9_pulse_data = pickle.load(pulse_file)
    pulse_file.close()

    pulse_file = open(os.path.join(dir, 'on_101010_101010.pkl'), 'rb')
    on_10_pulse_data = pickle.load(pulse_file)
    pulse_file.close()

    average_pulse_datas = [off_pulse_data, on_1_pulse_data, on_2_pulse_data, on_3_pulse_data, on_4_pulse_data,
                           on_5_pulse_data, on_6_pulse_data, on_7_pulse_data, on_8_pulse_data, on_9_pulse_data,
                           on_10_pulse_data]

    # This is just test data
    # average_pulse_datas = [
    #     [[1,1],[0,1]],
    #     [[1,1],[0,1],[1,1],[0,1]],
    #     [[1,1],[0,1],[1,1],[0,1],[1,1],[0,1]],
    #     [[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1]],
    #     [[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1]],
    #     [[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1]],
    #     [[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1]],
    #     [[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1]],
    #     [[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1]],
    #     [[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1]],
    #     [[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1]]
    # ]

    wiringpi2.wiringPiSetup() # For sequential pin numbering, one of these MUST be called before using IO functions
    wiringpi2.pinMode(0,1)  # Setup pin 11 (GPIO1)


    @staticmethod
    def usleep(x):
        """
        usleep sleeps x  microseconds
        :param x: microseconds to sleep
        """
        time.sleep(x / 1000000.0)

    def __init__(self):
        self.left_foot_power = 0
        self.left_middle_power = 0
        self.left_head_power = 0
        self.right_foot_power = 0
        self.right_middle_power = 0
        self.right_head_power = 0
        self._power_on = False

    @property
    def average_power(self):
        return (self.left_foot_power + self.left_middle_power + self.left_head_power + self.right_foot_power +
                self.right_middle_power + self.right_head_power) // 6

    @property
    def sum_power(self):
        return self.left_foot_power + self.left_middle_power + self.left_head_power + self.right_foot_power + \
               self.right_middle_power + self.right_head_power

    def power_off(self):
        self.left_foot_power = 0
        self.left_middle_power = 0
        self.left_head_power = 0
        self.right_foot_power = 0
        self.right_middle_power = 0
        self.right_head_power = 0
        self._power_on = False
        self.send_command()

    def full_power(self):
        self.left_foot_power = 10
        self.left_middle_power = 10
        self.left_head_power = 10
        self.right_foot_power = 10
        self.right_middle_power = 10
        self.right_head_power = 10
        self._power_on = True
        self.send_command()

    def set_power(self, left_foot_power, left_middle_power, left_head_power, right_foot_power, right_middle_power,
                  right_head_power):
        self.left_foot_power = left_foot_power
        self.left_middle_power = left_middle_power
        self.left_head_power = left_head_power
        self.right_foot_power = right_foot_power
        self.right_middle_power = right_middle_power
        self.right_head_power = right_head_power
        self._power_on = True
        self.send_command()

    def set_power(self):
        print("Setting average power {}".format(self.average_power))
        average_power = self.average_power
        self.left_foot_power = average_power
        self.left_middle_power = average_power
        self.left_head_power = average_power
        self.right_foot_power = average_power
        self.right_middle_power = average_power
        self.right_head_power = average_power
        self._power_on = True
        self.send_command()

    def send_command(self):
        """
        Sends current state
        """
        self.__send_command(self.__get_pulse_data())

    def __get_pulse_data(self):
        """
        Computes pulse data for current state
        In this case, it's returning one of 10 average states, future implementations will compute the exact pulse
        data with zoned heating and perhaps later subclasses may use thermal feedback to reach goal temperatures
        instead of merely power settings
        :return: pulse data
        """
        if self._power_on and self.sum_power == 0:  # all 0 indicates we actually mean to turn this off
            self._power_on = False
            return self.off_pulse_data
        elif self.average_power >= 10:  # prevent any out of bounds issues
            return self.average_pulse_datas[10]
        elif self.average_power == 0 and self.sum_power > 0:  # because we average round up from 0 if not exactly 0
            return self.average_pulse_datas[1]
        else:
            return self.average_pulse_datas[self.average_power]

    def __send_command(self, pulse_data):
        for pulse_pair in pulse_data:
            if pulse_pair[0] == 0:
                wiringpi2.digitalWrite(0,0)  # Turn off
            else:
                wiringpi2.digitalWrite(0,1)  # Turn on
            self.usleep(pulse_pair[1])

        wiringpi2.digitalWrite(0,0)  # Turn off

