from generators.utils import Range, RangeCustom
from models import SVPDPoint, Attribute, Road
from table_generators.base import TableGeneratorBase


class SignTableGenerator(TableGeneratorBase):
    condition = "[like '1401%']"


class SignAggregateGenerator(SignTableGenerator):
    def _get_raw_data(self):
        result = super()._get_raw_data()

        types = {
            '1': 'предупреждающие',
            '2': 'приоритета',
            '3': 'запрещающие',
            'З': 'запрещающие',
            '4': 'предписывающие',
            '5': 'особых предписаний',
            '6': 'информационно-указательные',
            '7': 'сервисные',
            '8': 'дополнительной информации',
            'К': 'дополнительной информации',
        }

        output_result = {
            'предупреждающие': 0,
            'приоритета': 0,
            'запрещающие': 0,
            'предписывающие': 0,
            'особых предписаний': 0,
            'информационно-указательные': 0,
            'сервисные': 0,
            'дополнительной информации': 0,
            'total': 0,
        }

        for s in result:
            type = types.get(str(s.name[0]).strip())
            if type is None:
                print(s.name[0])
            output_result[type] += 1
            output_result['total'] += 1

        return output_result


class VodootvodTableGenerator(TableGeneratorBase):
    title = "Ведомость водоотвода с проезжей части на автомобильной дороге"
    condition = "[like '010203%']"


class SidewalksTableGenerator(TableGeneratorBase):
    title = "Ведомость наличия и технического состояния тротуаров и пешеходных дорожек на автодороге"
    condition = "[in ('0405')]"

    def _get_raw_data(self):
        data = super()._get_raw_data()

        for item in data:
            item.params['width'] = round(abs(item.points[0].a - item.points[-1].a), 1)

        return data


class ZastroikaTableGenerator(TableGeneratorBase):
    title = "Ведомость застройки прилегающих к автомобильной дороге территорий"
    condition = "[in ('0805')]"

    def _get_raw_data(self):
        data = super()._get_raw_data()

        result = []
        if data:
            for item in data:
                if item.length > 0:
                    result.append(item)

        return result


class DirectDevicesTableGenerator(TableGeneratorBase):
    title = "Ведомость наличия направляющих устройств на автомобильной дороге"
    condition = "[in ('020302')]"

    def _get_raw_data(self):
        data = super()._get_raw_data()

        for item in data:
            item.params['count'] = len(item.points)

            between_distance = 0

            for i in range(len(item.points) - 1):
                between_distance += SVPDPoint.distance(item.points[i], item.points[i + 1])

            item.params['between_distance'] = round(between_distance / len(item.points), 1)

        return data


class GreenTableGenerator(TableGeneratorBase):
    title = "Ведомость наличия и технического состояния озеленения на автомобильной дороге"
    condition = "[in ('080304')]"

    def _get_raw_data(self):
        data = super()._get_raw_data()

        result = []
        if data:
            for item in data:
                if item.length > 0:
                    result.append(item)

        return result


class CrossTableGenerator(TableGeneratorBase):
    title = "Ведомость пересечений и примыканий на автомобильной дороге"
    condition = "[in ('040401','040404','040409')]"


class CrossAggregateGenerator(CrossTableGenerator):
    def _get_raw_data(self):
        data = super()._get_raw_data()

        result = {
            'цементобетон': {'length': 0, 'count': 0},
            'асфальтобетон': {'length': 0, 'count': 0},
            'щебень/гравий, обр. вяжущим': {'length': 0, 'count': 0},
            'щебень/гравий': {'length': 0, 'count': 0},
            'грунт': {'length': 0, 'count': 0},
            'ж/б плиты': {'length': 0, 'count': 0},
            'булыжник': {'length': 0, 'count': 0},
            'брусчатка': {'length': 0, 'count': 0},
            'тротуарная плитка': {'length': 0, 'count': 0},
            'прочие': {'length': 0, 'count': 0},
            'total': {'length': 0, 'count': 0},
        }
        for item in data:
            if 'Тип покрытия' in item.params:
                result[item.params['Тип покрытия']]['length'] += item.distance
                result[item.params['Тип покрытия']]['count'] += 1
            else:
                result['прочие']['length'] += item.distance
                result['прочие']['count'] += 1
            result['total']['length'] += item.distance
            result['total']['count'] += 1

        for k in result:
            result[k]['length'] = f"{result[k]['length']:.2f}"

        return result


class BusStopsTableGenerator(TableGeneratorBase):
    title = "Ведомость наличия и технического состояния автобусных остановок на автомобильной дороге"
    condition = "[in ('040202')]"


class BridgesTableGenerator(TableGeneratorBase):
    title = "Ведомость наличия и технического состояния мостов (путепроводов) на автомобильной дороге"
    condition = "[in ('1302')]"

    def _get_raw_data(self):
        data = super()._get_raw_data()

        result = []
        if data:
            for item in data:
                if item.length > 0:
                    result.append(item)

        return result


class TubesTableGenerator(TableGeneratorBase):
    title = "Ведомость наличия и технического состояния труб на автомобильной дороге"
    condition = "[in ('130101')]"


class TubesAggregateGenerator(TubesTableGenerator):
    def _get_raw_data(self):
        data = super()._get_raw_data()
        result = {
            'ж/б': {'length': 0, 'count': 0},
            'металл': {'length': 0, 'count': 0},
            'металл. гофрированная': {'length': 0, 'count': 0},
            'пластик': {'length': 0, 'count': 0},
            'дерево': {'length': 0, 'count': 0},
            'кирпич': {'length': 0, 'count': 0},
            'резина': {'length': 0, 'count': 0},
            'асбоцемент': {'length': 0, 'count': 0},
            'камень': {'length': 0, 'count': 0},
            'прочие': {'length': 0, 'count': 0},
            'полиэтиленовая гофрированная': {'length': 0, 'count': 0},
            'полиэтиленовая гофрированная "корсис"': {'length': 0, 'count': 0},
            'total': {'length': 0, 'count': 0},
        }
        for i in data:
            if 'Материал' in i.params:
                result[i.params['Материал'].lower().strip()]['length'] += i.distance
                result[i.params['Материал'].lower().strip()]['count'] += 1
            else:
                result['прочие']['length'] += i.distance
                result['прочие']['count'] += 1
            result['total']['length'] += i.distance
            result['total']['count'] += 1

        for k in result:
            result[k]['length'] = f"{result[k]['length']:.2f}"

        return result


class CommunicationsTableGenerator(TableGeneratorBase):
    title = "Ведомость наличия коммуникаций в пределах полосы отвода на автомобильной дороге"
    condition = "[like '06%']"


class CommunicationsAggregateGenerator(CommunicationsTableGenerator):
    def _get_raw_data(self):
        data = super()._get_raw_data()

        length = 0
        for i in data:
            if i.name == 'Воздушная коммуникация':
                length += i.length
        return {
            'length': length
        }


class LightTableGenerator(TableGeneratorBase):
    title = "Ведомость наличия и технического состояния столбов освещения"
    # condition = "[in ('0301','0401')]"
    condition = "[in ('0401')]"

    def _get_raw_data(self):
        data = super()._get_raw_data()

        result = []
        if data:
            previous_item = data[0]
            previous_item.params['counter'] = 1
            for item in data[1:]:
                if item.position == previous_item.position and abs(item.begin - previous_item.end) <= 100:
                    previous_item.end = item.begin
                    previous_item.end_km = item.begin_km
                    previous_item.end_m = item.begin_m
                    previous_item.params['counter'] += 1
                else:
                    result.append(previous_item)
                    previous_item = item
                    previous_item.params['counter'] = 1

            result.append(previous_item)

        return result


class LightAggregateGenerator(TableGeneratorBase):
    condition = "[in ('0401')]"
    def _get_raw_data(self):
        data = super()._get_raw_data()

        result = []
        if data:
            previous_item = data[0]
            previous_item.params['counter'] = 1
            for item in data[1:]:
                if abs(item.begin - previous_item.end) <= 100:
                    previous_item.end = item.begin
                    previous_item.end_km = item.begin_km
                    previous_item.end_m = item.begin_m
                    previous_item.length = previous_item.end - previous_item.begin
                    previous_item.params['counter'] += 1
                else:
                    result.append(previous_item)
                    previous_item = item
                    previous_item.params['counter'] = 1

            result.append(previous_item)

        return {
            'length': sum(i.length for i in result) if result else 0
        }


class CurveTableGenerator(TableGeneratorBase):
    title = "Кривые в плане"
    condition = "[ in ('23120104')]"


class ProfileGenerator(TableGeneratorBase):
    title = "Продольный профиль"
    condition = "[ in ('23120201')]"


class BarriersTableGenerator(TableGeneratorBase):
    title = "Ведомость наличия и технического состояния ограждений на автомобильной дороге"
    condition = "[in ('020301','020303','020304','020305','020306','020307')]"


class BarriersAggregateGenerator(BarriersTableGenerator):

    def _get_raw_data(self):
        data = super()._get_raw_data()
        length = 0
        for item in data:
            length += item.length
        return {
            'length': f"{length / 1000:.2f}"
        }


class CoverTypeTableAggregateGenerator(TableGeneratorBase):
    title = "Ведомость наличия покрытий на автомобильной дороге"
    condition = "[in ('2320')]"

    def _get_raw_data(self):
        data = super()._get_raw_data()
        result = {
            'цементобетон': 0,
            'асфальтобетон': 0,
            'щебень/гравий, обр. вяжущим': 0,
            'щебень/гравий': 0,
            'грунт': 0,
            'ж/б плиты': 0,
            'булыжник': 0,
            'брусчатка': 0,
            'тротуарная плитка': 0,
            'total': 0,
        }
        for item in data:
            result[item.params['Тип покрытия']] += item.length
            result['total'] += item.length

        return result


class RoadBrovkaWidthTableGenerator(TableGeneratorBase):
    condition = "[in ('010107')]"
    attribute = '010107'

    def _prepare_ranges(self, rng):
        ranges = {
            'year': 2024,
            '8': 0,
            '8-10': 0,
            '10-12': 0,
            '12-15': 0,
            '15-27.5': 0,
            '27.5': 0,
        }
        for r in rng.ranges:
            if r[2] is None:
                continue

            if r[2] < 8:
                ranges['8'] += (r[1] - r[0]) / 1000
            elif 8 <= r[2] < 10:
                ranges['8-10'] += (r[1] - r[0]) / 1000
            elif 10 <= r[2] < 12:
                ranges['10-12'] += (r[1] - r[0]) / 1000
            elif 12 <= r[2] < 15:
                ranges['12-15'] += (r[1] - r[0]) / 1000
            elif 15 <= r[2] < 27.5:
                ranges['15-27.5'] += (r[1] - r[0]) / 1000
            else:
                ranges['27.5'] += (r[1] - r[0]) / 1000

        return ranges


    def _get_raw_data(self):
        with self.db.session() as s:
            attributes = Attribute.query_by_high(s, self.high_id).filter(
                Attribute.ID_Type_Attr == self.attribute
            )
            attributes = list(attributes)

            start, end = self.road.get_length(s)

        # get periods by
        kromka_periods = RangeCustom(
            min=max(0, start),
            max=end,
            join_function=lambda x, y: (x or set()).union({y})
        )

        for idx, a in enumerate(attributes):
            points = sorted(a.points, key=lambda x: x.l)
            previous_point = points[0]
            for p in points[1:]:
                kromka_periods.add_subrange(previous_point.l, p.l, idx)
                previous_point = p

        rng = RangeCustom(
            min=max(0, start),
            max=end,
            join_function=lambda x, y: (x or 0) + (y or 0)
        )

        for _start, _end, idxs in kromka_periods.ranges:
            if idxs:
                idxs = list(idxs)
                if len(idxs) == 2:
                    left_points = attributes[idxs[0]].points
                    right_points = attributes[idxs[1]].points
                    left_points.sort(key=lambda x: x.l)
                    right_points.sort(key=lambda x: x.l)

                    if left_points[0].a >= right_points[0].a:
                        left_points, right_points = right_points, left_points

                    for points in (left_points, right_points):
                        previous_point = points[0]
                        for p in points[1:]:
                            value = abs((((previous_point.a + p.a) / 2) // 0.5) * 0.5)
                            rng.add_subrange(
                                max(_start, previous_point.l),
                                min(_end, p.l),
                                value,
                            )
                            previous_point = p

        # remove duplicates
        out_range = Range(
            min=max(0, start),
            max=end,
        )

        ranges = self._prepare_ranges(rng)
        for r in ranges:
            if r != 'year':
                ranges[r] = f"{(ranges[r]):.3f}"

        return [ranges]


class RoadKromkaWidthTableGenerator(RoadBrovkaWidthTableGenerator):
    condition = "[in ('010108')]"
    attribute = '010108'

    def _prepare_ranges(self, rng):
        ranges = {
            'year': 2024,
            '4': 0,
            '4-4.5': 0,
            '4.5-6': 0,
            '6-6.5': 0,
            '6.5-7': 0,
            '7-7.5': 0,
            '7.5-10': 0,
            '10-15': 0,
            '15-27': 0,
            '27': 0,
        }
        for r in rng.ranges:
            if r[2] is None:
                continue

            if r[2] < 4:
                ranges['4'] += (r[1] - r[0]) / 1000
            elif 4 <= r[2] < 4.5:
                ranges['4-4.5'] += (r[1] - r[0]) / 1000
            elif 4.5 <= r[2] < 6:
                ranges['4.5-6'] += (r[1] - r[0]) / 1000
            elif 6 <= r[2] < 6.5:
                ranges['6-6.5'] += (r[1] - r[0]) / 1000
            elif 6.5 <= r[2] < 7:
                ranges['6.5-7'] += (r[1] - r[0]) / 1000
            elif 7 <= r[2] < 7.5:
                ranges['7-7.5'] += (r[1] - r[0]) / 1000
            elif 7.5 <= r[2] < 10:
                ranges['7.5-10'] += (r[1] - r[0]) / 1000
            elif 10 <= r[2] < 15:
                ranges['10-15'] += (r[1] - r[0]) / 1000
            elif 15 <= r[2] < 27:
                ranges['15-27'] += (r[1] - r[0]) / 1000
            else:
                ranges['27'] += (r[1] - r[0]) / 1000

        return ranges