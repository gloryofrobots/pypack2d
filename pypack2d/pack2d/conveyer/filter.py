from pypack2d.pack2d.conveyer.unit import Unit
from pypack2d.pack2d.conveyer.signal import Signal,SignalType

#split input sequence S on groups of sub sequences S1..Sn where  length each of them == count
class Filter(Unit):
    def _on_init(self, count):
        self.count = count
        self.connect(SignalType.PUSH_INPUT, self._onPushInput)
        pass

    def _onPushInput(self, input):
        if self.count <= 0:
            return
            pass

        if self.nextUnit is None:
            return
            pass

        newInput = []
        count = self.count
        for image in input:
            newInput.append(image)
            count -= 1

            if count > 0:
                continue
                pass

            newSignal = Signal(SignalType.PUSH_INPUT, newInput)
            self._process_next(newSignal)

            newInput = []
            count = self.count
            pass

        #return False to stop this signal
        return False
        pass
    pass