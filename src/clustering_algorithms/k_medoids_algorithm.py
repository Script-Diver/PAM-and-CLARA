import random
from typing import List

import pandas as pd

from clustering_algorithms.point import Point


class KMedoidsAlgorithm:
    def __init__(
        self, points: List[Point], clusters_num: int = 2, labels: List["str"] = None
    ):
        if labels and not len(labels) == clusters_num:
            raise ValueError(
                "Number of labels needs to be the same as the number of clusters."
            )

        self.points = points
        self.clusters_num = clusters_num
        self.labels = labels

        self.medoids_indices = self.get_initial_medoids_indices(
            self.points, clusters_num
        )

    @staticmethod
    def get_initial_medoids_indices(
        source_points: List[Point], clusters_num: int
    ) -> List[int]:
        """
        Random selection of `cluster_num` points.

        Arguments:
            source_points: list of points
            clusters_num: number of medoids that will be randomly sampled from
                source_points

        Return:
            List of points' indices.

        """
        points_indices = [point.idx for point in source_points]
        return random.sample(points_indices, clusters_num)

    def prepare_medoids(self) -> List[Point]:
        """
        Prepare list of points that have been marked as medoids.

        Returns:
            List of medoids as Points.

        """
        return [point for point in self.points if point.idx in self.medoids_indices]

    def update_clusters_assignment(self) -> None:
        """
        Assign points to the medoids, which indices are stored in self.medoids_indices.

        """
        medoids = self.prepare_medoids()
        for point in self.points:
            point.update_cluster_assignment(medoids)

    def get_labels_mapper(self) -> dict:
        """
        Prepare dictionary that will be used to map points' nearest medoids into real
        labels.

        Return:
            mapper: medoid indices -> labels
            Ex. {114: "label_1", 10: "label_2", 999: "label_3"}

        """
        if self.labels and len(self.labels) == self.clusters_num:
            return {
                medoid_idx: label
                for label, medoid_idx in zip(self.labels, self.medoids_indices)
            }
        return {medoid_idx: idx for idx, medoid_idx in enumerate(self.medoids_indices)}

    def get_result_df(self) -> pd.DataFrame:
        """
        Convert Points from self.points into DataFrame.

        Return:
            DataFrame with info about points and their assignment to clusters.
            DataFrame columns:
                * idx
                * nearest_medoid
                * nearest_medoid_distance
                * second_nearest_medoid
                * second_nearest_medoid_distance
                * all coordinates with their names as keys
                * cluster
        """
        rows = {column: [] for column in self.points[0].get_data().keys()}
        for point in self.points:
            for key, value in point.get_data().items():
                rows[key].append(value)

        result = pd.DataFrame(rows)
        result["cluster"] = result["nearest_medoid"]
        result["cluster"].replace(self.get_labels_mapper(), inplace=True)

        return result

    def swap_medoids(self, old_medoid: Point, new_medoid: Point) -> None:
        """
        Delete `old_medoid` from medoids list. Add `new_medoid` to medoids list.

        """
        self.medoids_indices.remove(old_medoid.idx)
        self.medoids_indices.append(new_medoid.idx)
