from pypack2d.pack2d.conveyer.size_shifter.size_shifter_pow2 import BinSizeShifterPow2,get_low_pow2

class BinSizeShifterPow2MinimizeLast(BinSizeShifterPow2):
    def _on_end_to_pack(self, result):
        #TODO FIXME
        if len(result) is 0:
            return True
            pass

        #get last binSet and try to pack all it bins to smaller
        index = len(result) - 1
        minimized = self.find_minimal_size(result[index])
        #minimize all binSets
        super(BinSizeShifterPow2, self)._on_end_to_pack(result)

        #compare last minimized binSet with old last binSet
        self.normalise_size(minimized)
        old = result[index]
        if old.getEfficiency() < minimized.getEfficiency():
            result[index] = minimized
            pass

        return True
        pass

    def find_minimal_size(self, binSet):
        width = get_low_pow2(binSet.getWidth())
        height = get_low_pow2(binSet.getHeight())
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
        return self.find_minimal_size(result)
        pass
    pass