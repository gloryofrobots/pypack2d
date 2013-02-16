__author__ = 'human88998999877'
from PyPack2D.Packing2D.PackingConveyer.BinSizeShifter.BinSizeShifterPow2 import BinSizeShifterPow2,getLowPow2

class BinSizeShifterPow2MinimizeLast(BinSizeShifterPow2):
    def _onEndToPack(self, result):
        super(BinSizeShifterPow2, self)._onEndToPack(result)

        index = len(result) - 1
        result[index] = self.findMinimalSize(result[index])
        return True
        pass

    def findMinimalSize(self, binSet):
        width = getLowPow2(binSet.getWidth())
        height = getLowPow2(binSet.getHeight())
        if width is None or height is None:
            return binSet
            pass

        self.packer.setSize(int(width), int(height))
        bins = binSet.getBins()
        for bin in bins:
            clone = bin.clone()
            if self.packer.packBin(clone) is False:
                return binSet
                pass
            pass

        result = self.packer.flush()
        self.normaliseSize(result)
        
        if result.getEfficiency() < binSet.getEfficiency():
            return binSet
            pass

        return self.findMinimalSize(result)
        pass
    pass