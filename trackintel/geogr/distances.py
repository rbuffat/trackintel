from math import radians, cos, sin, asin, sqrt, pi


# todo: calculate distance matrix
#def distance_matrix():
#   pass
# for all that is euclidean (or minkowski) we can use scipy.spatial.distance_matrix
#
# There is a sklearn function that supports many different metrics:
# sklearn.metrics.pairwise_distances(X, Y=None, metric=’euclidean’, n_jobs=None, **kwds)
#

# todo: check the sklearn format for distances matrices and try to use it
def calculate_distance_matrix(points, dist_metric='haversine', *args, **kwds)

    x = points.geometry.x
    y = points.geometry.x

    n = len(x)

    for i in range(n):
        for j in range(n - i):
            x_1.append(x[i])
            y_1.append(y[i])
            x_2.append(x[j])
            y_2.append(y[j])

    if dist_metric == 'haversine':
        d = haversine_dist(x1, y1, x2, y2)


    # rebuild matrix from vector
    D = np.zeros(n,n)
    for i in range(n):
        for j in range(n - i):
            D[i,j] = d[i+j]

    return D
    


def haversine_dist(lon_1, lat_1, lon_2, lat_2, r=6371000):
    """Computes the great circle or haversine distance between two coordinates in WGS84.

    # todo: test different input formats, especially different vector
    shapes
    # define output format. 

    Parameters
    ----------
    lon_1 : float or numpy.array of shape (-1,)
        The longitude of the first point.
    
    lat_1 : float or numpy.array of shape (-1,)
        The latitude of the first point.
        
    lon_2 : float or numpy.array of shape (-1,)
        The longitude of the second point.
    
    lat_2 : float or numpy.array of shape (-1,)
        The latitude of the second point.

    r     : float
        Radius of the reference sphere for the calculation. 
        The average Earth radius is 6'371'000 m. 

    Returns
    -------
    float
        An approximation of the distance between two points in WGS84 given in meters.

    Examples
    --------
    >>> haversine_dist(8.5, 47.3, 8.7, 47.2)
    18749.056277719905

    References
    ----------
    https://en.wikipedia.org/wiki/Haversine_formula
    https://stackoverflow.com/questions/19413259/efficient-way-to-calculate-distance-matrix-given-latitude-and-longitude-data-in
    """ 
    
    lon_1 = lon_1.ravel() * np.pi / 180
    lat_1 = lat_1.ravel() * np.pi / 180
    lon_2 = lon_2.ravel() * np.pi / 180
    lat_2 = lat_2.ravel() * np.pi / 180
    
    cos_lat1 = np.cos(lat_1)
    cos_lat2 = np.cos(lat_2)
    cos_lat_d = np.cos(lat_1 - lat_2)
    cos_lon_d = np.cos(lon_1 - lon_2)

    return r * np.arccos(cos_lat_d - cos_lat1 * cos_lat2 * (1 - cos_lon_d))


def meters_to_decimal_degrees(meters, latitude):
    """Converts meters to decimal degrees (approximately).

    Parameters
    ----------
    meters : float
        The meters to convert to degrees.

    latitude : float
        As the conversion is dependent (approximatively) on the latitude where 
        the conversion happens, this needs to be specified. Use 0 for the equator.

    Returns
    -------
    float
        An approximation of a distance (given in meters) in degrees.
    """
    return meters / (111.32 * 1000.0 * cos(latitude * (pi / 180.0)))