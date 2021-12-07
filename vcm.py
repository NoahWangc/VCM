#!/usr/bin/python3
# coding=utf-8
import distance as dt
import datetime
from collections import Counter

vehicle_queue = {1: ['低栏车', 8000, 40, [108.322574, 22.833533], [113.263955, 23.154211], [2019050709, 2019051915]],
                 2: ['高栏车', 8000, 60, [113.263955, 23.154211], [108.322574, 22.833533], [2019050812, 2019052516]],
                 3: ['厢式车', 6000, 50, [108.322574, 22.833533], [114.420973, 23.159162], [2019050710, 2019051012]],
                 4: ['冷藏车', 7000, 45, [108.322574, 22.833533], [112.476087, 23.080553], [2019050908, 2019051512]],
                 5: ['通风箱车', 10000, 80, [109.395618, 24.315365], [113.263955, 23.154211], [2019050708, 2019052215]],
                 6: ['厢式车', 6000, 50, [113.263955, 23.154211], [110.28662, 25.267723], [2019050616, 2019052116]],
                 7: ['低栏车', 8000, 40, [113.434202, 22.519376], [108.655118, 22.060841], [2019050608, 2019051416]],
                 8: ['高栏车', 8000, 60, [113.263955, 23.154211], [110.28662, 25.267723], [2019050612, 2019052616]]}
cargo_queue = {1: ['日用百货', 5000, 30, [108.322574, 22.833533], [113.263955, 23.154211], [2019051212, 2019052516]],
               2: ['特殊货物', 7000, 40, [109.395618, 24.315365], [113.263955, 23.154211], [2019051209, 2019052315]],
               3: ['特殊货物', 5000, 35, [108.322574, 22.833533], [113.263955, 23.154211], [2019051109, 2019052512]],
               4: ['日用百货', 8000, 70, [110.28662, 25.267723], [108.322574, 22.833533], [2019051209, 2019052216]],
               5: ['日用百货', 5000, 50, [109.395618, 24.315365], [113.263955, 22.833533], [2019051109, 2019052314]]}

# type_match_list = [['低栏车', '日用百货', 0.8], ['低栏车', '特殊货物', 0.3],
#                    ['高栏车', '日用百货', 0.8], ['高栏车', '特殊货物', 0.5],
#                    ['厢式车', '日用百货', 1], ['厢式车', '特殊货物', 0.6],
#                    ['冷藏车', '日用百货', 0.1], ['冷藏车', '特殊货物', 0.1],
#                    ['通风箱车', '日用百货', 0.8], ['通风箱车', '特殊货物', 0.6]]
type_match_list = [['低栏车', '日用百货', 0.8], ['低栏车', '特殊货物', 0.3], ['低栏车', '机器零件', 1], ['低栏车', '生鲜果蔬', 0.5],
                   ['低栏车', '砂石散货', 0.8], ['低栏车', '五金机械', 1],
                   ['高栏车', '日用百货', 0.8], ['高栏车', '特殊货物', 0.5], ['高栏车', '机器零件', 1], ['高栏车', '生鲜果蔬', 0.5],
                   ['高栏车', '砂石散货', 1], ['高栏车', '五金机械', 1],
                   ['厢式车', '日用百货', 1], ['厢式车', '特殊货物', 0.8], ['厢式车', '机器零件', 1], ['厢式车', '生鲜果蔬', 0.5],
                   ['厢式车', '砂石散货', 0.8], ['厢式车', '五金机械', 1],
                   ['冷藏车', '日用百货', 0.1], ['冷藏车', '特殊货物', 0.1], ['冷藏车', '机器零件', 0.1], ['冷藏车', '生鲜果蔬', 1],
                   ['冷藏车', '砂石散货', 0.1], ['冷藏车', '五金机械', 0.1],
                   ['通风箱车', '日用百货', 0.8], ['通风箱车', '特殊货物', 0.5], ['通风箱车', '机器零件', 0.8], ['通风箱车', '生鲜果蔬', 1],
                   ['通风箱车', '砂石散货', 0.5], ['通风箱车', '五金机械', 0.8],
                   ['平板车', '日用百货', 0.6], ['平板车', '特殊货物', 0.6], ['平板车', '机器零件', 0.8], ['平板车', '生鲜果蔬', 0.6],
                   ['平板车', '砂石散货', 0.5], ['平板车', '五金机械', 0.8]]


# 类型匹配度
def getTypeMatch(vehicle, cargo):
    # vehicle = '厢式车'
    # cargo = '特殊货物'
    typeMatchDegree = 0
    for item in type_match_list:
        if vehicle == item[0] and cargo == item[1]:
            typeMatchDegree = item[2]
    return typeMatchDegree


# 质量或体积匹配度
def getQualityVolumeMatch(vQ, vV, cQ, cV):
    """
    :param vQ: 车辆质量
    :param vV: 车辆体积
    :param cQ: 货物质量
    :param cV: 货物体积
    :return:
    """
    # vQ = 8000
    # vV = 40
    # cQ = 5000
    # cV = 30
    QualityVolumeMatchDegree = 0
    # 判断货物是重货还是轻货，重货使用体积，轻货则使用体积
    if (cV / 0.006) > cQ:
        QualityVolumeMatchDegree = cV / vV
    else:
        QualityVolumeMatchDegree = cQ / vQ
    # 如果出现cQ>vQ,cV>Vv, 匹配度直接为0
    if QualityVolumeMatchDegree > 1:
        QualityVolumeMatchDegree = 0
    return QualityVolumeMatchDegree


# getQualityVolumeMatch(6000, 50, 7000, 40)

# 路程匹配度
def getFlowMatch(vO, vD, cO, cD):
    """
    :param vO: vehicle origin:车辆起始地
    :param vD: vehicle Destination:车辆目的地
    :param cO: cargo origin:货物起始地
    :param cD: cargo Destination:货物目的地
    :return:
    """
    # 分别表示，货物起始点到终点距离，车辆货物起始地距离，车辆货物终点距离
    cargo_origin_destination = 0
    vehicle_cargo_origin = 0
    vehicle_cargo_destination = 0
    flowMatchDegree = 0
    # vO = 108.322574, 22.833533
    vO = ",".join('%s' % id for id in vO)
    vD = ",".join('%s' % id for id in vD)
    cO = ",".join('%s' % id for id in cO)
    cD = ",".join('%s' % id for id in cD)
    # vD = '113.263955, 23.154211'
    # cO = '108.322574, 22.833533'
    # cD = '113.263955, 23.154211'
    cargo_origin_destination = int(dt.getDistance(vO, vD)) // 1000
    vehicle_cargo_origin = int(dt.getDistance(vO, cO)) // 1000
    vehicle_cargo_destination = int(dt.getDistance(vD, cD)) // 1000
    flowMatchDegree = cargo_origin_destination / (
            cargo_origin_destination + vehicle_cargo_origin + vehicle_cargo_destination)
    # print(cargo_origin_destination, vehicle_cargo_origin, vehicle_cargo_destination)
    # print(flowMatchDegree)
    return flowMatchDegree


# getFlowMatch([108.322574, 22.833533], [113.263955, 23.154211], [108.322574, 22.833533], [113.263955, 23.154211])

# 时间匹配度
def timeMatch(vS, vD, cS, cD):
    """
    :param vS: vehicle-start:车辆进入时间
    :param vD: vehicle_deadline:车辆截止时间
    :param cS: cargo-start:货物进入时间
    :param cD: cargo-deadline:货物截止时间
    :return:
    """
    timeMatchDegree = 0
    # vS = 2019050709
    # vD = 2019051915
    # cS = 2019051212
    # cD = 2019052516
    vS_list = [int(str(vS)[0:4]), int(str(vS)[4:6]), int(str(vS)[6:8])]
    vD_list = [int(str(vD)[0:4]), int(str(vD)[4:6]), int(str(vD)[6:8])]
    cS_list = [int(str(cS)[0:4]), int(str(cS)[4:6]), int(str(cS)[6:8])]
    cD_list = [int(str(cD)[0:4]), int(str(cD)[4:6]), int(str(cD)[6:8])]
    # 最小截止时间
    min_deadline = min(vD, cD)
    # 最大开始时间
    max_start = max(vS, cS)
    min_deadline_list = [int(str(min_deadline)[0:4]), int(str(min_deadline)[4:6]), int(str(min_deadline)[6:8])]
    max_start_list = [int(str(max_start)[0:4]), int(str(max_start)[4:6]), int(str(max_start)[6:8])]
    # print(min_deadline, max_start, min_deadline_list, max_start_list)
    # d1-d2表示最小截止时间减去最大开始时间。 d3-d4表示货物开始和截止时间之间的天数
    d1 = datetime.date(min_deadline_list[0], min_deadline_list[1], min_deadline_list[2])
    d2 = datetime.date(max_start_list[0], max_start_list[1], max_start_list[2])
    d3 = datetime.date(cS_list[0], cS_list[1], cS_list[2])
    d4 = datetime.date(cD_list[0], cD_list[1], cD_list[2])
    interval_days = (d1 - d2).days
    cargo_interval_days = (d4 - d3).days
    # print(interval_days, cargo_interval_days)
    if interval_days > 0:
        timeMatchDegree = interval_days / cargo_interval_days
    else:
        timeMatchDegree = 0
    # print(timeMatchDegree)
    return timeMatchDegree


# timeMatch()

# 车辆属性分布概率
def vehicleAttrDis(vehicle_queue):
    length = len(vehicle_queue)
    type_list = []
    quality_list = []
    volume_list = []
    start_list = []
    destination_list = []
    time_list = []
    for item, value in vehicle_queue.items():
        type_list.append(value[0])
        quality_list.append(value[1])
        volume_list.append(value[2])
        start_list.append(value[3])
        destination_list.append(value[4])
        time_list.append(value[5])
    # type_count存放各类型车出现的次数
    type_count = Counter(type_list)
    # quality_count存放不同质量出现次数
    quality_count = Counter(quality_list)
    # volume_count存放不同体积出现次数
    volume_count = Counter(volume_list)

    # start_count表示起始地相同的有几个
    def cal_start_count(abc):
        start_count = 0
        for start in start_list:
            if abc == start:
                start_count += 1
        return start_count

    # destination_count表示目的地相同的有多少个
    def cal_destination_count(abc):
        destination_count = 0
        for destination in destination_list:
            if abc == destination:
                destination_count += 1
        return destination_count

    # time_count表示时间起始，截止相同的个数
    def cal_time_count(abc):
        time_count = 0
        for time in time_list:
            if abc == time:
                time_count += 1
        return time_count

    # 存放每一辆车的各个具体属性的分布
    attr_distri_list = []
    # 计算每辆车的属性分布
    for item, value in vehicle_queue.items():
        vehicle_attr = []
        type_distri = type_count[value[0]] / length
        quality_distri = quality_count[value[1]] / length
        volume_distri = volume_count[value[2]] / length
        start_distri = cal_start_count(value[3]) / length
        destination_distri = cal_destination_count(value[4]) / length
        time_distri = cal_time_count(value[5]) / length
        vehicle_attr.append(type_distri)
        vehicle_attr.append(quality_distri)
        vehicle_attr.append(volume_distri)
        vehicle_attr.append(start_distri)
        vehicle_attr.append(destination_distri)
        vehicle_attr.append(time_distri)
        attr_distri_list.append(vehicle_attr)

    total_attr = 0
    for i in attr_distri_list:
        total_attr += sum(i)
    # print(total_attr)

    # 存放每一辆车的整体属性分布
    vehicle_attr_list = []
    for i in attr_distri_list:
        vehicle_attr_list.append(sum(i))
    # print(vehicle_attr_list)

    # 车辆属性分布概率（先验概率）  最终的结果
    attr_distribution_final_all = [round(i / total_attr, 2) for i in vehicle_attr_list]
    # print(attr_distribution_final_all)
    return attr_distribution_final_all


# vehicleAttrDis()

# 货物属性分布概率
def cargoAttrDis(cargo_queue):
    length = len(cargo_queue)
    type_list = []
    quality_list = []
    volume_list = []
    start_list = []
    destination_list = []
    time_list = []
    for item, value in cargo_queue.items():
        type_list.append(value[0])
        quality_list.append(value[1])
        volume_list.append(value[2])
        start_list.append(value[3])
        destination_list.append(value[4])
        time_list.append(value[5])
    # type_count存放各类型货物出现的次数
    type_count = Counter(type_list)
    # quality_count存放不同质量出现次数
    quality_count = Counter(quality_list)
    # volume_count存放不同体积出现次数
    volume_count = Counter(volume_list)

    # start_count表示起始地相同的有几个
    def cal_start_count(abc):
        start_count = 0
        for start in start_list:
            if abc == start:
                start_count += 1
        return start_count

    # destination_count表示目的地相同的有多少个
    def cal_destination_count(abc):
        destination_count = 0
        for destination in destination_list:
            if abc == destination:
                destination_count += 1
        return destination_count

    # time_count表示时间起始，截止相同的个数
    def cal_time_count(abc):
        time_count = 0
        for time in time_list:
            if abc == time:
                time_count += 1
        return time_count

    # 存放每一个货物的各个具体属性的分布
    attr_distri_list = []
    # 计算每个货物的属性分布
    for item, value in cargo_queue.items():
        vehicle_attr = []
        type_distri = type_count[value[0]] / length
        quality_distri = quality_count[value[1]] / length
        volume_distri = volume_count[value[2]] / length
        start_distri = cal_start_count(value[3]) / length
        destination_distri = cal_destination_count(value[4]) / length
        time_distri = cal_time_count(value[5]) / length
        vehicle_attr.append(type_distri)
        vehicle_attr.append(quality_distri)
        vehicle_attr.append(volume_distri)
        vehicle_attr.append(start_distri)
        vehicle_attr.append(destination_distri)
        vehicle_attr.append(time_distri)
        attr_distri_list.append(vehicle_attr)

    total_attr = 0
    for i in attr_distri_list:
        total_attr += sum(i)
    # print(total_attr)

    # 存放每一货物的整体属性分布
    vehicle_attr_list = []
    for i in attr_distri_list:
        vehicle_attr_list.append(sum(i))
    # print(vehicle_attr_list)

    # 货物属性分布概率（先验概率）  最终的结果
    attr_distribution_final_all = [round(i / total_attr, 2) for i in vehicle_attr_list]
    # print(attr_distribution_final_all)
    return attr_distribution_final_all


# cargoAttrDis()

a = ['低栏车', 8000, 40, [108.322574, 22.833533], [113.263955, 23.154211], [2019050709, 2019051915]]
b = ['日用百货', 5000, 30, [108.322574, 22.833533], [113.263955, 23.154211], [2019051212, 2019052516]]
c = ['日用百货', 5000, 50, [109.395618, 24.315365], [113.263955, 22.833533], [2019051109, 2019052314]]


def VCM(a, b, w1=0.2, w2=0.1, w3=0.4, w4=0.3):
    # w1 = 0.2
    # w2 = 0.1
    # w3 = 0.4
    # w4 = 0.3
    typeMatch = getTypeMatch(a[0], b[0])
    qvMatch = getQualityVolumeMatch(a[1], a[2], b[1], b[2])
    flowMatch = getFlowMatch(a[3], a[4], b[3], b[4])
    timeMatchs = timeMatch(a[5][0], a[5][1], b[5][0], b[5][1])
    attrMatch = w1 * typeMatch + w2 * qvMatch + w3 * flowMatch + w4 * timeMatchs
    attrMatch = round(attrMatch, 2)
    if typeMatch == 0 or qvMatch == 0 or flowMatch == 0 or timeMatchs == 0:
        attrMatch = 0
    # vcm_final = attrMatch
    # print(attrMatch)
    return attrMatch


def rePaperVCM(a, b, w1=0.16, w2=0.09, w3=0.47, w4=0.28):
    # w1 = 0.2
    # w2 = 0.1
    # w3 = 0.4
    # w4 = 0.3
    typeMatch = getTypeMatch(a[0], b[0])
    qvMatch = getQualityVolumeMatch(a[1], a[2], b[1], b[2])
    flowMatch = getFlowMatch(a[3], a[4], b[3], b[4])
    timeMatchs = timeMatch(a[5][0], a[5][1], b[5][0], b[5][1])
    # attrMatch = w1 * typeMatch + w2 * qvMatch + w3 * flowMatch + w4 * timeMatchs
    attrMatch = typeMatch * qvMatch * flowMatch * timeMatchs
    attrMatch = round(attrMatch, 2)
    if typeMatch == 0 or qvMatch == 0 or flowMatch == 0 or timeMatchs == 0:
        attrMatch = 0
    # vcm_final = attrMatch
    # print(attrMatch)
    return attrMatch


# vehicle_prior = vehicleAttrDis()
# cargo_prior = cargoAttrDis()
# print(vehicle_prior, cargo_prior)
# for vehicleKey, vehicleValue in vehicle_queue.items():
#     for cargoKey, cargoValue in cargo_queue.items():
#         attrMatch = VCM(vehicleValue, cargoValue)
#         finalMatch = (attrMatch * vehicle_prior[vehicleKey - 1]) / cargo_prior[cargoKey - 1]
#         print(round(finalMatch, 2), end=" ")
#     print()


# 从数据集中读取数据添加到vehicle_queue
def appendVehicle(vehicle_df, vehicle_maxNum, vehicle_queue, t):
    # 如果车辆队列中车辆少于10辆。那么读取数据集并添加至十辆车
    if (len(vehicle_queue) < 10):
        for index, row in vehicle_df.iterrows():
            vehicle_attr = []
            # 上一次vehicle_queue中存放着的车辆的最大编号是num。那么在少于十辆车继续添加车的时候，就应该从num+1开始读取数据
            if t == 0:
                num = 0
            else:
                num = vehicle_maxNum[t - 1]
            # 0 是表头，
            if index > num:
                for i in range(0, len(row)):
                    if i == 1:
                        row[i] = int(row[i])
                    if i == 2:
                        row[i] = int(row[i])
                    if i == 3 or i == 4:
                        row[i] = (row[i])[1:-1]
                        row[i] = row[i].split(',')
                        for j in range(0, len(row[i])):
                            row[i][j] = float(row[i][j])
                    if i == 5:
                        row[i] = (row[i])[1:-1]
                        row[i] = row[i].split(',')
                        for j in range(0, len(row[i])):
                            row[i][j] = int(row[i][j])
                    vehicle_attr.append(row[i])
                vehicle_queue[index] = vehicle_attr
                if len(vehicle_queue) == 10:
                    vehicle_maxNum.append(index)
                    break


# 从数据集中读取数据添加到cargo_queue
# 参数：1：数据集的df形式，2：队列最大的货物编号，3：货物队列，4：时间
def appendCargo(cargo_df, cargo_maxNum, cargo_queue, t):
    # 如果车辆队列中车辆少于10辆。那么读取数据集并添加至十辆车
    if (len(cargo_queue) < 10):
        for index, row in cargo_df.iterrows():
            cargo_attr = []
            # 上一次vehicle_queue中存放着的车辆的最大编号是num。那么在少于十辆车继续添加车的时候，就应该从num+1开始读取数据
            if t == 0:
                num = 0
            else:
                num = cargo_maxNum[t - 1]
            # 0 是表头，
            if index > num:
                for i in range(0, len(row)):
                    if i == 1:
                        row[i] = int(row[i])
                    if i == 2:
                        row[i] = int(row[i])
                    if i == 3 or i == 4:
                        row[i] = (row[i])[1:-1]
                        row[i] = row[i].split(',')
                        for j in range(0, len(row[i])):
                            row[i][j] = float(row[i][j])
                    if i == 5:
                        row[i] = (row[i])[1:-1]
                        row[i] = row[i].split(',')
                        for j in range(0, len(row[i])):
                            row[i][j] = int(row[i][j])
                    cargo_attr.append(row[i])
                cargo_queue[index] = cargo_attr
                if len(cargo_queue) == 10:
                    cargo_maxNum.append(index)
                    break
