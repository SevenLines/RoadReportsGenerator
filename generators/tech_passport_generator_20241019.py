from generators.base_generator import BaseGenerator
from table_generators.generators import VodootvodTableGenerator, SignTableGenerator, SidewalksTableGenerator, \
    ZastroikaTableGenerator, DirectDevicesTableGenerator, GreenTableGenerator, CrossTableGenerator, \
    BusStopsTableGenerator, BridgesTableGenerator, TubesTableGenerator, CommunicationsTableGenerator, \
    LightTableGenerator, BarriersTableGenerator, CurveTableGenerator, RoadKromkaWidthTableGenerator, \
    RoadBrovkaWidthTableGenerator


class TechPassportGenerator20241019(BaseGenerator):
    template = "tech_passport_generator2.docx"

    tables_generators = {
        'SignTableGenerator': SignTableGenerator, # +
        'VodootvodTableGenerator': VodootvodTableGenerator, # +
        'SidewalksTableGenerator': SidewalksTableGenerator, # +
        'ZastroikaTableGenerator': ZastroikaTableGenerator, # TODO
        'DirectDevicesTableGenerator': DirectDevicesTableGenerator, # +
        'GreenTableGenerator': GreenTableGenerator, # TODO
        'CrossTableGenerator': CrossTableGenerator, # +
        'BusStopsTableGenerator': BusStopsTableGenerator, # +
        'BridgesTableGenerator': BridgesTableGenerator, # TODO
        'TubesTableGenerator': TubesTableGenerator, # +
        'CommunicationsTableGenerator': CommunicationsTableGenerator,
        'LightTableGenerator': LightTableGenerator, # +
        'BarriersTableGenerator': BarriersTableGenerator, # +
        'CurveTableGenerator': CurveTableGenerator, # +
        'RoadKromkaWidthTableGenerator': RoadKromkaWidthTableGenerator, # +
        'RoadBrovkaWidthTableGenerator': RoadBrovkaWidthTableGenerator, # +
    }





