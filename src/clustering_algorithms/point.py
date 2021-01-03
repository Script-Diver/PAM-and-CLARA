import numpy as np

from clustering_algorithms.utils import compute_distance


class Point:
    def __init__(self, idx, coordinates):
        self.idx = idx
        self.coordinates = coordinates
        # Point's cluster (nearest medoid)
        self.nearest_medoid = None
        self.nearest_medoid_distance = None
        # Point's second nearest medoid
        self.second_nearest_medoid = None
        self.second_nearest_medoid_distance = None

    def update_cluster_assignment(self, medoids):
        """
        Pick nearest and second nearest medois from given medoids list.
        Update Point's assignment.
        """
        if self in medoids:
            self.nearest_medoid = self
            return

        self.nearest_medoid = np.nan
        self.nearest_medoid_distance = np.nan
        self.second_nearest_medoid = np.nan
        self.second_nearest_medoid_distance = np.nan

        for medoid in medoids:
            distance = compute_distance(self.coordinates, medoid.coordinates)

            # first assignment or better cluster found
            if self.nearest_medoid is np.nan or distance < self.nearest_medoid_distance:
                # update values connected to the second nearest medoid
                self.second_nearest_medoid = self.nearest_medoid
                self.second_nearest_medoid_distance = self.nearest_medoid_distance
                # update values connected to the nearest medoid
                self.nearest_medoid = medoid
                self.nearest_medoid_distance = distance

            # first assignment or better cluster found
            elif (
                self.second_nearest_medoid is np.nan
                or distance < self.second_nearest_medoid_distance
            ):
                self.second_nearest_medoid = medoid
                self.second_nearest_medoid_distance = distance

    def compute_medoid_replacement_cost(self, medoid_to_change, new_medoid, medoids):
        """
        Compute partial cost of replacing medoid `medoid_to_change` by object
        `new_medoid`.

        Arguments:
            medoid_to_change: medoid that we want to replace by another object
            new_medoid:

        """
        # medoid's cluster will not change, do not compute cost for medoid
        if self in medoids:
            return 0

        # distance to the new medoid
        new_medoid_distance = compute_distance(self.coordinates, new_medoid.coordinates)

        # we want to replace medoid that represents Point's cluster
        if self.nearest_medoid == medoid_to_change:
            if new_medoid_distance >= self.second_nearest_medoid_distance:
                # second_nearest_medoid will be Point's nearest_medoid
                return (
                    self.second_nearest_medoid_distance - self.nearest_medoid_distance
                )
            else:
                # new_medoid will be Point's nearest_medoid
                return new_medoid_distance - self.nearest_medoid_distance
        # we want to replace medoid that does not represent Point's cluster
        else:
            if new_medoid_distance >= self.nearest_medoid_distance:
                # Point's cluster will be the same as before
                return 0
            else:
                # new_medoid will be Point's nearest_medoid
                return new_medoid_distance - self.nearest_medoid_distance