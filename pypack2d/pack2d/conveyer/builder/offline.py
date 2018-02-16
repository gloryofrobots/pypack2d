from pypack2d.pack2d.conveyer.accumulator import Accumulator
from pypack2d.pack2d.conveyer.sorter import Sorter
from pypack2d.pack2d.conveyer.control.control import PackingControl
from pypack2d.pack2d.conveyer.builder.builder import PackingConveyerBuilder


class PackingConveyerBuilderOffline(PackingConveyerBuilder):
    def _on_build(self, conveyer, factory, settings):
        accumulator = Accumulator()
        conveyer.push_unit(accumulator)

        if settings.sortOrder is not None:
            sorting = factory.create_instance(settings.sortKey)
            sorter = Sorter(sorting, settings.sortOrder)
            conveyer.push_unit(sorter)
            pass

        packer = factory.create_instance(settings.packingAlgorithm)
        control = PackingControl(packer, factory, settings)
        conveyer.push_unit(control)
        pass

    pass