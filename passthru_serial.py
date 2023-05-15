class Passthru:
    def __init__(self, jtagulator_object):
        self._jtagulator_object = jtagulator_object

    def write(self, message):
        self._jtagulator_object._connection.write(message)

    def read(self):
        return self._jtagulator_object._connection.read()

    def interact(self, message):
        self.write(message)
        return self.read()
