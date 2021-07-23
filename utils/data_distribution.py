import numpy as np


class DataDistribution:
    """class for representing data distribution"""

    ordered_data_points = []

    def __init__(self, data_points: list):
        self.ordered_data_points = data_points.copy()
        self.ordered_data_points.sort()

    def get_percentile(self, data_point: float):
        for i in range(len(self.ordered_data_points)):
            if self.ordered_data_points[i] >= data_point:
                return i / len(self.ordered_data_points)
        return 1

    def get_point(self, percentile: float):
        ix = round(percentile * len(self.ordered_data_points))
        return self.ordered_data_points[min(ix, len(self.ordered_data_points) - 1)]


def convert_data_points_into_percentile_list(data_points, dist=None):
    if not dist:
        dist = DataDistribution(data_points)
    final_lst = []
    for point in data_points:
        final_lst.append(dist.get_percentile(point))
    return np.array([final_lst]), dist


def convert_data_points_2D_into_percentile_2D(data_points):
    dist = []
    new_arr = []
    for i in range(len(data_points)):
        lst, dt = convert_data_points_into_percentile_list(data_points[i])
        dist.append(dt)
        new_arr.append(lst)
    return np.concatenate(new_arr), dist