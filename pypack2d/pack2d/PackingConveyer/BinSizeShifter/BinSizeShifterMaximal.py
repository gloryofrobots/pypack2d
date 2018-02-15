from pypack2d.pack2d.PackingConveyer.BinSizeShifter.BinSizeShifter import BinSizeShifter

class BinSizeShifterMaximal(BinSizeShifter):
    def _onShift(self, binSet):
        maxRight = 0
        maxBottom = 0
        for bin in binSet:
            if bin.right > maxRight:
                maxRight = bin.right
                pass
            if bin.bottom > maxBottom:
                maxBottom = bin.bottom
                pass
            pass

        binSet.setSize(maxRight, maxBottom)
        pass
    pass