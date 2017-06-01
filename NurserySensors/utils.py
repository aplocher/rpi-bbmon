class Utils:
    @staticmethod
    def convert_c_to_f(tempC):
        temp = tempC * 1.8
        temp = temp + 32
        return temp

    @staticmethod
    def convert_f_to_c(tempF):
        temp = tempF - 32
        temp = temp / 1.8
        return temp