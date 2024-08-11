from table_generators.base import TableGeneratorBase


class SignTableGenerator(TableGeneratorBase):
    condition = "[like '1401%' or Attribute.ID_Type_Attr in ('0301')]"


class VodootvodTableGenerator(TableGeneratorBase):
    title = "Ведомость водоотвода с проезжей части на автомобильной дороге"
    condition = "[like '010203%']"


class SidewalksTableGenerator(TableGeneratorBase):
    title = "Ведомость наличия и технического состояния тротуаров и пешеходных дорожек на автодороге"
    condition = "[in ('0405')]"


class ZastroikaTableGenerator(TableGeneratorBase):
    title = "Ведомость застройки прилегающих к автомобильной дороге территорий"
    condition = "[in ('0301','0805')]"


class DirectDevicesTableGenerator(TableGeneratorBase):
    title = "Ведомость наличия направляющих устройств на автомобильной дороге"
    condition = "[in ('020302')]"


class GreenTableGenerator(TableGeneratorBase):
    title = "Ведомость наличия и технического состояния озеленения на автомобильной дороге"
    condition = "[in ('0301','080304')]"


class CrossTableGenerator(TableGeneratorBase):
    title = "Ведомость пересечений и примыканий на автомобильной дороге"
    condition = "[in ('040401','040404','040409')]"


class BusStopsTableGenerator(TableGeneratorBase):
    title = "Ведомость наличия и технического состояния автобусных остановок на автомобильной дороге"
    condition = "[in ('040202')]"


class BridgesTableGenerator(TableGeneratorBase):
    title = "Ведомость наличия и технического состояния мостов (путепроводов) на автомобильной дороге"
    condition = "[in ('1302','0301')]"


class TubesTableGenerator(TableGeneratorBase):
    title = "Ведомость наличия и технического состояния труб на автомобильной дороге"
    condition = "[in ('130101','0301')]"


class CommunicationsTableGenerator(TableGeneratorBase):
    title = "Ведомость наличия коммуникаций в пределах полосы отвода на автомобильной дороге"
    condition = "[like '06%' or Attribute.ID_Type_Attr in ('0301')]"


class LightTableGenerator(TableGeneratorBase):
    title = "Ведомость наличия и технического состояния столбов освещения"
    condition = "[in ('0301','0401')]"


class BarriersTableGenerator(TableGeneratorBase):
    title = "Ведомость наличия и технического состояния ограждений на автомобильной дороге"
    condition = "[in ('020301','020303','020304','020305','020306','020307')]"
