import numpy as np
import pandas as pd
import geopandas as gpd
import sklearn
import shapely

from shapely.geometry import Point, MultiPoint
from sklearn.cluster import DBSCAN


def cluster_staypoints(staypoints, method='dbscan',
                       epsilon=100, num_samples=3):
    """Clusters staypoints to get places.

    Parameters
    ----------
    staypoints : GeoDataFrame
        The staypoints have to follow the standard definition for staypoints DataFrames.

    method : {'dbscan'}
        The following methods are available to cluster staypoints into places:

        'dbscan' : Uses the DBSCAN algorithm to cluster staypoints.

    epsilon : float
        The epsilon for the 'dbscan' method.

    num_samples : int
        The minimal number of samples in a cluster.

    Returns
    -------
    GeoDataFrame
        A new GeoDataFrame containing places that a person visited multiple times.

    Examples
    --------
    >>> cluster_staypoints(...)    
    """
    ret_places = pd.DataFrame(columns=['user_id', 'place_id','geom'])


    db = DBSCAN(eps=epsilon, min_samples=num_samples)
    for user_id_this in staypoints["user_id"].unique():

        user_staypoints = staypoints[staypoints["user_id"] == user_id_this] #this is not a copy!

        # todo: enable transformations to temporary (metric) system
        transform_crs = None
        if transform_crs is not None:
            pass

        # todo: allow to pass a distance metric. This is important to cluster points in meters
        # even if they are distributed over a large geographic area

        # get place matching
        coordinates = np.array([[g.x, g.y] for g in user_staypoints['geom']])
        labels = db.fit_predict(coordinates)

        # add staypoint - place matching to original staypoints
        staypoints.loc[user_staypoints.index,'place_id'] = labels

    # create places as grouped staypoints
    grouped_df = staypoints.groupby(['user_id','place_id'])
    for combined_id, group in grouped_df:
        user_id, place_id = combined_id

        if int(place_id) != -1:
            ret_place = {}
            ret_place['user_id'] = user_id
            ret_place['place_id'] = place_id
            
            # point geometry of place
            ret_place['center'] = Point(group.geometry.x.mean(),
                 group.geometry.y.mean())
            # polygon geometry of place
            ret_place['extent'] = MultiPoint(points=list(group.geometry)).convex_hull

            ret_places = ret_places.append(ret_place, ignore_index=True)

    ret_places = gpd.GeoDataFrame(ret_places, geometry='center')
    ret_places['place_id'] = ret_places['place_id'].astype('int')
    return ret_places

