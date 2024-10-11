# -*- coding: UTF-8 -*-

from typing import Union, Tuple, Literal
from tqdm import tqdm

import numpy as np
import umap as umap_
from anndata import AnnData
import pandas as pd
from pandas import DataFrame

from ykenan_log import Logger

from sklearn.manifold import TSNE, SpectralEmbedding
from sklearn.cluster import KMeans, SpectralClustering
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import (
    calinski_harabasz_score,
    adjusted_mutual_info_score,
    silhouette_score,
    davies_bouldin_score,
    adjusted_rand_score,
    accuracy_score,
    recall_score,
    f1_score,
    roc_curve,
    auc
)

from scipy import special, stats

from scLift.util import (
    matrix_data,
    to_sparse,
    to_dense,
    sparse_matrix,
    dense_data,
    number,
    collection,
    get_index,
    check_adata_get,
    project_name
)

log = Logger(f"{project_name}_tool_algorithm")


def sigmoid(data: matrix_data):
    return 1 / (1 + np.exp(-data))


def tf_idf(data: matrix_data, ri_sparse: bool = True) -> matrix_data:
    """
    TF-IDF transformer
    :param data: Matrix data that needs to be converted;
    :param ri_sparse: (return_is_sparse) Whether to return sparse matrix.
    :return: Matrix processed by TF-IDF.
    """
    log.info("TF-IDF transformer")
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(to_dense(data, is_array=True))
    return to_sparse(tfidf) if ri_sparse else to_dense(tfidf)


def adjustment_tf_idf(data: matrix_data, ri_sparse: bool = True) -> matrix_data:
    """
    adjustment TF-IDF transformer
    :param data: Matrix data that needs to be converted;
    :param ri_sparse: (return_is_sparse) Whether to return sparse matrix.
    :return: Matrix processed by adjustment TF-IDF.
    """
    log.info("Start adjustment TF-IDF transformer")
    data = to_dense(data, is_array=True)
    data_abs = np.abs(data)

    # TF
    row_sum = data_abs.sum(axis=1)
    row_sum[row_sum == 0] = 1
    tf = data / np.array(row_sum).flatten()[:, np.newaxis]

    # DF
    col_sum = data_abs.sum(axis=0)
    col_sum[col_sum == 0] = 1
    df = data_abs / np.array(col_sum).flatten()

    # IDF
    idf = np.log(data.shape[0] / (df + 1))

    # TF_IDF
    tfidf = np.multiply(tf, idf)
    log.info("End adjustment TF-IDF transformer")
    return to_sparse(tfidf) if ri_sparse else to_dense(tfidf)


def z_score_normalize(
    data: matrix_data,
    with_mean: bool = True,
    ri_sparse: bool = True
) -> Union[dense_data, sparse_matrix]:
    """
    Matrix standardization (z-score)
    :param data: Standardized data matrix required.
    :param with_mean: If True, center the data before scaling.
    :param ri_sparse: (return_is_sparse) Whether to return sparse matrix.
    :return: Standardized matrix.
    """
    log.info("Matrix z-score standardization")
    scaler = StandardScaler(with_mean=with_mean)

    if with_mean:
        dense_data_ = to_dense(data, is_array=True)
    else:
        dense_data_ = data

    transform_data = scaler.fit_transform(np.array(dense_data_))
    return to_sparse(transform_data) if ri_sparse else to_dense(transform_data)


def z_score_marginal(matrix: matrix_data, axis: Literal[0, 1] = 0) -> Tuple[matrix_data, matrix_data]:
    """
    Matrix standardization (z-score, marginal)
    :param matrix: Standardized data matrix required.
    :param axis: Standardize according to which dimension.
    :return: Standardized matrix.
    """
    log.info("Start marginal z-score")
    matrix = np.matrix(to_dense(matrix))
    # Separate z-score for each element
    __mean__ = np.mean(matrix, axis=axis)
    __std__ = np.std(matrix, axis=axis)
    # Control denominator is not zero
    __std__[__std__ == 0] = 1
    z_score = (matrix - __mean__) / __std__
    log.info("End marginal z-score")
    return z_score, __mean__


def marginal_normalize(matrix: matrix_data, axis: Literal[0, 1] = 0, default: float = 1e-50) -> matrix_data:
    """
    Marginal standardization
    :param matrix: Standardized data matrix required;
    :param axis: Standardize according to which dimension;
    :param default: To prevent division by 0, this value needs to be added to the denominator.
    :return: Standardized data.
    """
    matrix = np.matrix(to_dense(matrix))
    __sum__ = np.sum(matrix, axis=axis)
    return matrix / (__sum__ + default)


def min_max_norm(data: matrix_data, axis: Literal[0, 1, -1] = -1) -> matrix_data:
    """
    Calculate min max standardized data
    :param data: input data;
    :param axis: Standardize according to which dimension.
    :return: Standardized data.
    """
    data = to_dense(data, is_array=True)

    # Judgment dimension
    if axis == -1:
        data_extremum = data.max() - data.min()
        if data_extremum == 0:
            data_extremum = 1
        new_data = (data - data.min()) / data_extremum
    elif axis == 0:
        data_extremum = np.array(data.max(axis=axis) - data.min(axis=axis)).flatten()
        data_extremum[data_extremum == 0] = 1
        new_data = (data - data.min(axis=axis).flatten()) / data_extremum
    elif axis == 1:
        data_extremum = np.array(data.max(axis=axis) - data.min(axis=axis)).flatten()
        data_extremum[data_extremum == 0] = 1
        new_data = (data - data.min(axis=axis).flatten()[:, np.newaxis]) / data_extremum[:, np.newaxis]
    else:
        log.error(
            "The `axis` parameter supports only -1, 0, and 1, while other values will make the `scale` parameter value "
            "equal to 1."
        )
        raise ValueError("The `axis` parameter supports only -1, 0, and 1")

    return new_data


def symmetric_scale(
    data: matrix_data,
    scale: Union[number, collection] = 2.0,
    axis: Literal[0, 1, -1] = -1,
    is_verbose: bool = True
) -> matrix_data:
    """
    Symmetric scale Function
    :param data: input data;
    :param axis: Standardize according to which dimension;
    :param scale: scaling factor.
    :param is_verbose: log information.
    :return: Standardized data
    """

    if is_verbose:
        log.info("Start symmetric scale function")

    # Judgment dimension
    if axis == -1:
        scale = 1 if scale == 0 else scale
        x_data = to_dense(data) / scale
    elif axis == 0:
        scale = to_dense(scale, is_array=True).flatten()
        scale[scale == 0] = 1
        x_data = to_dense(data) / scale
    elif axis == 1:
        scale = to_dense(scale, is_array=True).flatten()
        scale[scale == 0] = 1
        x_data = to_dense(data) / scale[:, np.newaxis]
    else:
        log.warn(
            "The `axis` parameter supports only -1, 0, and 1, while other values will make the `scale` parameter value "
            "equal to 1."
        )
        x_data = to_dense(data)

    # Record symbol information
    symbol = to_dense(x_data).copy()
    symbol[symbol > 0] = 1
    symbol[symbol < 0] = -1

    # Log1p standardized data
    y_data = np.multiply(x_data, symbol)
    y_data = special.log1p(y_data)
    # Return symbols and make changes and sigmoid mapped data
    z_data = np.multiply(y_data, symbol)

    if is_verbose:
        log.info("End symmetric scale function")
    return z_data


def mean_symmetric_scale(data: matrix_data, axis: Literal[0, 1, -1] = -1, is_verbose: bool = True) -> matrix_data:
    """
    Calculate the mean symmetric
    :param data: input data;
    :param axis: Standardize according to which dimension.
    :param is_verbose: log information.
    :return: Standardized data after average symmetry.
    """

    # Judgment dimension
    if axis == -1:
        return symmetric_scale(data, np.abs(data).mean(), axis=-1, is_verbose=is_verbose)
    elif axis == 0:
        return symmetric_scale(data, np.abs(data).mean(axis=0), axis=0, is_verbose=is_verbose)
    elif axis == 1:
        return symmetric_scale(data, np.abs(data).mean(axis=1), axis=1, is_verbose=is_verbose)
    else:
        log.warn("The `axis` parameter supports only -1, 0, and 1")
        raise ValueError("The `axis` parameter supports only -1, 0, and 1")


def is_asc_sort(positions_list: list) -> bool:
    """
    Judge whether the site is in ascending order
    :param positions_list: positions list.
    :return: True for ascending order, otherwise False.
    """
    length: int = len(positions_list)

    if length <= 1:
        return True

    tmp = positions_list[0]

    for i in range(1, length):
        if positions_list[i] < tmp:
            return False
        tmp = positions_list[i]

    return True


def lsi(data: matrix_data, n_components: int = 50) -> dense_data:
    """
    SVD LSI
    :param data: input cell feature data;
    :param n_components: Dimensions that need to be reduced to.
    :return: Reduced dimensional data (SVD LSI model).
    """

    if data.shape[1] <= n_components:
        log.info("The features of the data are less than or equal to the `n_components` parameter, ignoring LSI")
        return to_dense(data, is_array=True)
    else:
        log.info("Start LSI")
        svd = TruncatedSVD(n_components=n_components)
        svd_data = svd.fit_transform(to_dense(data, is_array=True))
        log.info("End LSI")
        return svd_data


def pca(data: matrix_data, n_components: int = 50) -> dense_data:
    """
    PCA
    :param data: input cell feature data;
    :param n_components: Dimensions that need to be reduced to.
    :return: Reduced dimensional data.
    """
    if data.shape[1] <= n_components:
        log.info("The features of the data are less than or equal to the `n_components` parameter, ignoring PCA")
        return to_dense(data, is_array=True)
    else:
        log.info("Start PCA")
        data = to_dense(data, is_array=True)
        pca_n = PCA(n_components=n_components)
        pca_n.fit_transform(data)
        pca_data = pca_n.transform(data)
        log.info("End PCA")
        return pca_data


# noinspection SpellCheckingInspection
def laplacian_eigenmaps(data: matrix_data, n_components: int = 2) -> dense_data:
    """
    Laplacian Eigenmaps
    :param data: input cell feature data;
    :param n_components: Dimensions that need to be reduced to.
    :return: Reduced dimensional data.
    """
    if data.shape[1] <= n_components:
        log.info(
            "The features of the data are less than or equal to the `n_components` parameter, ignoring Laplacian "
            "Eigenmaps"
        )
        return to_dense(data, is_array=True)
    else:
        log.info("Start Laplacian Eigenmaps")
        data = to_dense(data, is_array=True)
        se = SpectralEmbedding(n_components=n_components)
        se_data = se.fit_transform(data)
        log.info("End Laplacian Eigenmaps")
        return se_data


def semi_mutual_knn_weight(
    data: matrix_data,
    neighbors: int = 30,
    or_neighbors: int = 3,
    weight: float = 0.01
) -> Tuple[matrix_data, matrix_data]:
    """
    Mutual KNN with weight
    :param data: Input data matrix;
    :param neighbors: The number of nearest neighbors;
    :param or_neighbors: The number of or nearest neighbors;
    :param weight: The weight of interactions or operations;
    :return: Adjacency weight matrix
    """
    log.info("Start semi-mutual KNN")

    if weight < 0 or weight > 1:
        log.error("The `and_weight` parameter must be between 0 and 1.")
        raise ValueError("The `and_weight` parameter must be between 0 and 1.")

    new_data: matrix_data = to_dense(data).copy()

    for j in range(new_data.shape[0]):
        new_data[j, j] = 0

    def _knn_(_data_: matrix_data, _neighbors_: int) -> matrix_data:
        _cell_cell_knn_: matrix_data = _data_.copy()
        _cell_cell_knn_copy_: matrix_data = _data_.copy()

        # Obtain numerical values for constructing a k-neighbor network
        cell_cell_affinity_sort = np.sort(_cell_cell_knn_, axis=1)
        cell_cell_value = cell_cell_affinity_sort[:, -(_neighbors_ + 1)]
        _cell_cell_knn_[_cell_cell_knn_copy_ >= np.array(cell_cell_value).flatten()[:, np.newaxis]] = 1
        _cell_cell_knn_[_cell_cell_knn_copy_ < np.array(cell_cell_value).flatten()[:, np.newaxis]] = 0
        return _cell_cell_knn_

    cell_cell_knn = _knn_(new_data, neighbors)

    if neighbors == or_neighbors:
        cell_cell_knn_or = cell_cell_knn.copy()
    else:
        cell_cell_knn_or = _knn_(new_data, or_neighbors)

    # Obtain symmetric adjacency matrix, using mutual kNN algorithm
    adjacency_and_matrix = np.minimum(cell_cell_knn, cell_cell_knn.T)
    adjacency_or_matrix = np.maximum(cell_cell_knn_or, cell_cell_knn_or.T)
    adjacency_weight_matrix = (1 - weight) * adjacency_and_matrix + weight * adjacency_or_matrix
    log.info("End semi-mutual KNN")
    return adjacency_weight_matrix, adjacency_and_matrix


def k_means(data: matrix_data, n_clusters: int = 2):
    """
    Perform k-means clustering on data
    :param data: Input data matrix;
    :param n_clusters: The number of clusters to form as well as the number of centroids to generate.
    :return: Tags after k-means clustering.
    """
    log.info("Start K-means cluster")
    model = KMeans(n_clusters=n_clusters, n_init="auto")
    model.fit(to_dense(data, is_array=True))
    labels = model.labels_
    log.info("End K-means cluster")
    return labels


def spectral_clustering(data: matrix_data, n_clusters: int = 2) -> collection:
    """
    Spectral clustering
    :param data: Input data matrix;
    :param n_clusters: The dimension of the projection subspace.
    :return: Tags after spectral clustering.
    """
    log.info("Start spectral clustering")
    data = to_dense(data, is_array=True)
    model = SpectralClustering(n_clusters=n_clusters)
    clusters_types = model.fit_predict(data)
    log.info("End spectral clustering")
    return clusters_types


def tsne(data: matrix_data, n_components: int = 2) -> matrix_data:
    """
    T-SNE dimensionality reduction
    :param data: Data matrix that requires dimensionality reduction;
    :param n_components: Dimension of the embedded space.
    :return: Reduced dimensional data matrix
    """
    data = to_dense(data, is_array=True)
    tsne = TSNE(n_components=n_components)
    tsne.fit(data)
    data_tsne = tsne.fit_transform(data)
    return data_tsne


def umap(data: matrix_data, n_neighbors: float = 15, n_components: int = 2, min_dist: float = 0.15) -> matrix_data:
    """
    UMAP dimensionality reduction
    :param data: Data matrix that requires dimensionality reduction;
    :param n_neighbors: float (optional, default 15)
        The size of local neighborhood (in terms of number of neighboring
        sample points) used for manifold approximation. Larger values
        result in more global views of the manifold, while smaller
        values result in more local data being preserved. In general
        values should be in the range 2 to 100;
    :param n_components: The dimension of the space to embed into. This defaults to 2 to
        provide easy visualization, but can reasonably be set to any
        integer value in the range 2 to 100.
    :param min_dist: The effective minimum distance between embedded points. Smaller values
        will result in a more clustered/clumped embedding where nearby points
        on the manifold are drawn closer together, while larger values will
        result on a more even dispersal of points. The value should be set
        relative to the ``spread`` value, which determines the scale at which
        embedded points will be spread out.
    :return: Reduced dimensional data matrix
    """
    data = to_dense(data, is_array=True)
    embedding = umap_.UMAP(n_neighbors=n_neighbors, n_components=n_components, min_dist=min_dist).fit_transform(data)
    return embedding


def kl_divergence(data1: matrix_data, data2: matrix_data) -> float:
    """
    Calculate KL divergence for two data
    :param data1: First data;
    :param data2: Second data.
    :return: KL divergence score
    """
    data1 = to_dense(data1, is_array=True).flatten()
    data2 = to_dense(data2, is_array=True).flatten()
    return stats.entropy(data1, data2)


def calinski_harabasz(data: matrix_data, labels: collection) -> float:
    """
    The Calinski-Harabasz index is also one of the indicators used to evaluate the quality of clustering models.
    It measures the compactness within the cluster and the separation between clusters in the clustering results. The
    larger the value, the better the clustering effect
    :param data: First data;
    :param labels: Predicted labels for each sample.
    :return:
    """
    return calinski_harabasz_score(to_dense(data, is_array=True), labels)


def silhouette(data: matrix_data, labels: collection) -> float:
    """
    silhouette
    :param data: An array of pairwise distances between samples, or a feature array;
    :param labels: Predicted labels for each sample.
    :return: index
    """
    return silhouette_score(to_dense(data, is_array=True), labels)


def davies_bouldin(data: matrix_data, labels: collection) -> float:
    """
    Davies-Bouldin index (DBI)
    :param data: A list of ``n_features``-dimensional data points. Each row corresponds to a single data point;
    :param labels: Predicted labels for each sample.
    :return: index
    """
    return davies_bouldin_score(to_dense(data, is_array=True), labels)


def ari(labels_pred: collection, labels_true: collection) -> float:
    """
    ARI (-1, 1)
    :param labels_pred: Predictive labels for clustering;
    :param labels_true: Real labels for clustering.
    :return: index
    """
    return adjusted_rand_score(labels_true, labels_pred)


def ami(labels_pred: collection, labels_true: collection) -> float:
    """
    AMI (0, 1)
    :param labels_pred: Predictive labels for clustering;
    :param labels_true: Real labels for clustering.
    :return: index
    """
    return adjusted_mutual_info_score(labels_true, labels_pred)


def f1_auc(labels_pred: collection, labels_true: collection) -> Tuple[float, float, float, float, float, float]:
    """
    Accuracy, Recall, F1, FPR, TPR auc
    :param labels_pred: Predictive labels for clustering;
    :param labels_true: Real labels for clustering.
    :return: index
    """
    acc_s = accuracy_score(labels_true, labels_pred)
    rec_s = recall_score(labels_true, labels_pred)
    f1_s = f1_score(labels_true, labels_pred)
    fpr, tpr, thresholds = roc_curve(labels_true, labels_pred)
    auc_s = auc(fpr, tpr)
    return acc_s, rec_s, f1_s, fpr, tpr, auc_s


class RandomWalk:
    """
    Random walk
    """

    def __init__(
        self,
        cc_adata: AnnData,
        init_status: AnnData,
        epsilon: float = 1e-05,
        gamma: float = 0.01,
        p: int = 2,
        min_seed_cell_rate: float = 0.01,
        max_seed_cell_rate: float = 0.05,
        credible_threshold: float = 0,
        is_simple: bool = True
    ):
        """
        Perform random walk steps
        :param cc_adata: Cell features;
        :param init_status: For cell scores under each trait;
        :param epsilon: conditions for stopping in random walk;
        :param gamma: reset weight for random walk;
        :param p: Distance used for loss {1: Manhattan distance, 2: Euclidean distance};
        :param min_seed_cell_rate: The minimum percentage of seed cells in all cells;
        :param max_seed_cell_rate: The maximum percentage of seed cells in all cells.
        :param credible_threshold: The threshold for determining the credibility of enriched cells in the context of
            enrichment, i.e. the threshold for judging enriched cells;
        :return: Stable distribution score.
        """
        log.info("Random walk.")
        # judge length
        if cc_adata.shape[0] != init_status.shape[0]:
            log.error(
                f"The number of rows {cc_adata.shape[0]} in the data is not equal to the initialization state length "
                f"{np.array(init_status).size}"
            )
            raise ValueError(
                f"The number of rows {cc_adata.shape[0]} in the data is not equal to the initialization state length "
                f"{np.array(init_status).size}"
            )

        if p <= 0:
            log.error(
                "The value of `p` must be greater than zero. Distance used for loss {1: Manhattan distance, "
                "2: Euclidean distance}"
            )
            raise ValueError(
                "The value of `p` must be greater than zero. Distance used for loss {1: Manhattan distance, "
                "2: Euclidean distance}"
            )
        elif p > 3:
            log.warn("Suggested value for `p` is 1 or 2.")

        if epsilon > 0.1:
            log.warn(
                f"Excessive value of parameter `epsilon`=({epsilon}) can lead to incorrect iteration and poor "
                f"enrichment effect."
            )
        elif epsilon < 0:
            epsilon = 0
            log.warn(
                "The parameter value of `epsilon` is less than 0, which is equivalent to the effect of zero. "
                "Therefore, setting the value of epsilon will be set to zero."
            )

        init_status.obs["clusters"] = init_status.obs["clusters"].astype(str)

        self.cc_adata = cc_adata
        self.epsilon = epsilon
        self.gamma = gamma
        self.p = p
        self.min_seed_cell_rate = min_seed_cell_rate
        self.max_seed_cell_rate = max_seed_cell_rate
        self.credible_threshold = credible_threshold
        self.is_simple = is_simple

        # Enrichment judgment
        self.is_run_none = False
        self.is_run_none_nw = False
        self.is_run_core = False
        self.is_run_core_nw = False

        self.is_run_en_none = False
        self.is_run_en_none_nw = False
        self.is_run_en = False
        self.is_run_en_nw = False

        self.is_random = False

        self.cell_affinity = to_dense(cc_adata.layers["cell_affinity"])
        self.trs_data: AnnData = init_status.copy()
        self.trs_data.X = to_sparse(init_status.X)
        self.cell_size: int = self.trs_data.shape[0]

        self.trait_info: list = list(init_status.var["id"])

        # set seed cells
        self.run_core_score = np.zeros(init_status.shape)

        if not is_simple:
            self.run_none_score = np.zeros(init_status.shape)
            self.run_none_nw_score = np.zeros(init_status.shape)
            self.run_core_nw_score = np.zeros(init_status.shape)
            self.random_cell_matrix = np.zeros(init_status.shape)

        # trait
        self.trait_list: list = list(self.trs_data.var_names)
        self.trait_range = range(len(self.trait_list))

        # Transition Probability Matrix
        self.weight, self.cell_weight = self._get_weight_()
        # get seed value
        self.seed_cell_size = self._get_seed_cell_size_()
        (
            self.seed_cell_threshold,
            self.seed_cell_matrix,
            self.seed_cell_weight,
            self.seed_cell_en_matrix,
            self.seed_cell_en_weight
        ) = self._get_seed_cell_(init_status)

        if not is_simple:
            init_status_no_weight = check_adata_get(init_status, "init_score")
            (
                self.seed_cell_threshold_nw,
                self.seed_cell_matrix_nw,
                self.seed_cell_weight_nw,
                self.seed_cell_en_matrix_nw,
                self.seed_cell_en_weight_nw
            ) = self._get_seed_cell_(init_status_no_weight)

    def _random_walk_(self, seed_cell_vector: collection, weight: matrix_data = None, gamma: float = 0) -> matrix_data:
        """
        Perform a random walk
        :param seed_cell_vector: seed cells;
        :param weight: weight matrix;
        :param gamma: reset weight.
        :return: The value after random walk.
        """

        if weight is None:
            w = to_dense(self.weight).copy()
        else:
            w = to_dense(weight).copy()

        # Random walk
        p0 = seed_cell_vector.copy()[:, np.newaxis]
        pt: matrix_data = seed_cell_vector.copy()[:, np.newaxis]
        k = 0
        delta = 1

        # iteration
        while delta > self.epsilon:
            p1 = (1 - gamma) * np.dot(w, pt) + gamma * p0

            # 1 and 2, It would be faster alone
            if self.p == 1:
                delta = np.abs(pt - p1).sum()
            elif self.p == 2:
                delta = np.sqrt(np.square(np.abs(pt - p1)).sum())
            else:
                delta = np.float_power(np.float_power(np.abs(pt - p1), self.p).sum(), 1.0 / self.p)

            pt = p1
            k += 1

        return pt.flatten()

    def _random_walk_core_(self, seed_cell_vector: collection, weight: matrix_data = None) -> matrix_data:
        """
        Perform a random walk
        :param seed_cell_vector: seed cells;
        :param weight: weight matrix.
        :return: The value after random walk.
        """
        return self._random_walk_(seed_cell_vector, weight, self.gamma)

    def _get_weight_(self) -> Tuple[matrix_data, matrix_data]:
        """
        Obtain weights in random walks
        :return: weight matrix
            1. The weights used in the iteration of random walks.
            2. Assign different weight matrices to seed cells.
        """
        data_weight = to_dense(self.cc_adata.X, is_array=True)
        cell_sum_weight = data_weight.sum(axis=1)[:, np.newaxis]
        cell_sum_weight[cell_sum_weight == 0] = 1

        cell_weight = np.multiply(data_weight, self.cell_affinity)
        return data_weight / cell_sum_weight, cell_weight

    def _get_seed_cell_size_(self) -> int:
        # cluster size/count
        cluster_types = list(set(self.trs_data.obs["clusters"]))
        cluster_types.sort()

        clusters = list(self.trs_data.obs["clusters"])
        cluster_size: dict = {}

        for cluster in cluster_types:
            count = clusters.count(cluster)
            cluster_size.update(
                {cluster: {
                    "size": clusters.count(cluster),
                    "rate": count / self.cell_size
                }}
            )

        seed_cell_size: int = np.ceil(self.cell_size / len(cluster_types)).astype(int)

        # Control the number of seeds
        if (seed_cell_size / self.cell_size) < self.min_seed_cell_rate:
            seed_cell_size = np.ceil(self.min_seed_cell_rate * self.cell_size).astype(int)
        elif (seed_cell_size / self.cell_size) > self.max_seed_cell_rate:
            seed_cell_size = np.ceil(self.max_seed_cell_rate * self.cell_size).astype(int)

        if seed_cell_size == 0:
            seed_cell_size = 1

        self.trs_data.uns["cluster_info"] = {
            "cluster_size": cluster_size,
            "seed_cell_size": seed_cell_size,
            "min_seed_cell_rate": self.min_seed_cell_rate,
            "max_seed_cell_rate": self.max_seed_cell_rate
        }
        return seed_cell_size

    def _get_cell_seed_weight_(self, seed_cell_index: collection) -> collection:
        seed_cell_mutual_knn = np.array(self.cell_weight[seed_cell_index, :][:, seed_cell_index])
        seed_weight_threshold: collection = seed_cell_mutual_knn.sum(axis=0)
        seed_weight_threshold /= (1 if seed_weight_threshold.sum() == 0 else seed_weight_threshold.sum())
        return seed_weight_threshold

    def _get_seed_cell_(self, init_data: AnnData) -> Tuple[collection, matrix_data, matrix_data, matrix_data, matrix_data]:
        """
        Obtain information related to seed cells
        :param init_data: Initial TRS data
        :return:
            1. Number of seed cells.
            2. The threshold for seedless cells for each trait or disease.
            3. Average weight of seed cells.
            4. Seed cells with different weights.
        """

        # seed cell threshold
        seed_cell_threshold: collection = np.zeros(len(self.trait_list))
        seed_cell_weight: matrix_data = np.zeros(self.trs_data.shape)
        seed_cell_en_weight: matrix_data = np.zeros(self.trs_data.shape)

        if not self.is_simple:
            seed_cell_matrix: matrix_data = np.zeros(self.trs_data.shape)
            seed_cell_en_matrix: matrix_data = np.zeros(self.trs_data.shape)
        else:
            seed_cell_matrix: matrix_data = np.zeros((1, 1))
            seed_cell_en_matrix: matrix_data = np.zeros((1, 1))

        log.info(f"Calculate {len(self.trait_list)} traits/diseases for seed cells information.")
        for i in tqdm(self.trait_range):

            # Obtain all cell score values in a trait
            trait_adata = init_data[:, i]
            trait_value = to_dense(trait_adata.X, is_array=True).flatten()

            # Obtain the maximum initial score
            trait_value_max = np.max(trait_value)

            if trait_value_max > 0:
                trait_value_sort_index = np.argsort(trait_value).astype(int)
                trait_value_sort_index = trait_value_sort_index[::-1]

                seed_cell_threshold[i] = trait_value[trait_value_sort_index[self.seed_cell_size]]

                # Set seed cell weights (reduce noise seed cell weights)
                seed_cell_index = trait_value_sort_index[0:self.seed_cell_size]
                seed_cell_weight[:, i][seed_cell_index] = self._get_cell_seed_weight_(seed_cell_index)

                seed_cell_en_index = trait_value_sort_index[
                                     self.seed_cell_size:2 * self.seed_cell_size
                                     if self.cell_size > 2 * self.seed_cell_size else self.seed_cell_size - 1]
                _seed_cell_en_weight_ = self._get_cell_seed_weight_(seed_cell_en_index)
                seed_cell_en_weight[:, i][seed_cell_en_index] = _seed_cell_en_weight_[::-1]

                if not self.is_simple:
                    # Without weight
                    seed_cell_value = np.zeros(self.cell_size)
                    seed_cell_value[seed_cell_index] = 1
                    seed_cell_matrix[:, i] = seed_cell_value / (1 if seed_cell_value.sum() == 0 else seed_cell_value.sum())
                    seed_cell_en_value = np.zeros(self.cell_size)
                    seed_cell_en_value[seed_cell_en_index] = 1
                    seed_cell_en_matrix[:, i] = seed_cell_en_value / (1 if seed_cell_en_value.sum() == 0 else seed_cell_en_value.sum())

        return seed_cell_threshold, seed_cell_matrix, seed_cell_weight, seed_cell_en_matrix, seed_cell_en_weight

    @staticmethod
    def _scale_norm_(score: matrix_data) -> matrix_data:
        cell_value = mean_symmetric_scale(score, axis=0)
        cell_value = np.log1p(min_max_norm(cell_value, axis=0))
        return cell_value

    def _simple_error_(self) -> None:

        if self.is_simple and "is_simple" in self.trs_data.uns.keys() and self.trs_data.uns["is_simple"]:
            log.error("The parameter `is_simple` is True, so running this method is not supported.")
            raise RuntimeError("The parameter `is_simple` is True, so running this method is not supported.")

    def run_random(self) -> None:
        """
        Perform random walks of random seeds on all traits.
        """
        self._simple_error_()

        for i in tqdm(self.trait_range):
            # Set random seed information
            random_seed_cell = np.zeros(self.cell_weight.shape[0])
            random_seed_index = np.random.choice(
                np.arange(0, self.cell_weight.shape[0]), size=self.seed_cell_size, replace=False
            )
            random_seed_cell[random_seed_index] = 1

            # seed cell weight
            seed_weight_threshold: collection = (
                np.array(self.cell_weight[random_seed_index, :][:, random_seed_index]).sum(axis=0)
            )
            seed_weight_threshold /= (1 if seed_weight_threshold.sum() == 0 else seed_weight_threshold.sum())
            random_seed_cell[random_seed_index] = seed_weight_threshold

            # Random walk
            cell_value = self._random_walk_core_(random_seed_cell)

            # Remove the influence of background
            self.random_cell_matrix[:, i] = cell_value

        cell_value = self._scale_norm_(self.random_cell_matrix)
        self.trs_data.layers["trait_cell_random"] = to_sparse(cell_value)
        self.is_random = True

    @staticmethod
    def _get_label_description_(label: str) -> str:
        if label == "run_core":
            return "Calculate weighted random walks."
        elif label == "run_none_nw":
            return "Removed cell weights in random walks and cluster type weights in initial scores."
        elif label == "run_none":
            return "Removed cell weights from random walks."
        elif label == "run_core_nw":
            return "Removed cell cluster type weights in initial scores."
        else:
            raise ValueError(f"{label} is not a valid information.")

    def _run_(self, seed_cell_data: matrix_data, label: str) -> matrix_data:
        """
        Calculate random walks
        :param seed_cell_data: Seed cell data
        :return: Return values without `scale` normalization
        """

        score = np.zeros(self.trs_data.shape)

        log.info(f"Calculate {len(self.trait_list)} traits/diseases for process `{label}`. ({self._get_label_description_(label)})")

        for i in tqdm(self.trait_range):
            score[:, i] = self._random_walk_core_(seed_cell_data[:, i])

        cell_value = self._scale_norm_(score)
        self.trs_data.layers[f"{label}_trs"] = to_sparse(score)
        self.trs_data.layers[f"{label}_trs_scale"] = to_sparse(cell_value)
        return score

    def run_none(self) -> None:
        """
        Removed cell weights from random walks
        """
        self._simple_error_()
        self.trs_data.layers["seed_cell_matrix"] = self.seed_cell_matrix
        self.trs_data.var["seed_cell_threshold"] = self.seed_cell_threshold
        self.run_none_score = self._run_(self.seed_cell_matrix, "run_none")
        self.is_run_none = True

    def run_none_nw(self) -> None:
        """
        Removed cell weights in random walks and cluster type weights in initial scores
        """
        self._simple_error_()
        self.trs_data.layers["seed_cell_matrix_nw"] = self.seed_cell_matrix_nw
        self.trs_data.var["seed_cell_threshold_nw"] = self.seed_cell_threshold_nw
        self.run_none_nw_score = self._run_(self.seed_cell_matrix_nw, "run_none_nw")
        self.is_run_none_nw = True

    def run_core(self) -> None:
        """
        Calculate weighted random walks
        """
        if not self.is_simple:
            self.trs_data.layers["seed_cell_weight"] = self.seed_cell_weight

        self.trs_data.var["seed_cell_threshold"] = self.seed_cell_threshold
        self.run_core_score = self._run_(self.seed_cell_weight, "run_core")

        if not self.is_simple:
            self.trs_data.layers[f"run_core_trs_source"] = to_sparse(self.run_core_score)

        self.is_run_core = True

    def run_core_nw(self) -> None:
        """
        Removed cell cluster type weights in initial scores
        """
        self._simple_error_()
        self.trs_data.layers["seed_cell_weight_nw"] = self.seed_cell_weight_nw
        self.trs_data.var["seed_cell_threshold_nw"] = self.seed_cell_threshold_nw
        self.run_core_nw_score = self._run_(self.seed_cell_weight_nw, "run_core_nw")
        self.is_run_core_nw = True

    def _run_enrichment_(self, seed_cell_en_weight: matrix_data, label: str) -> None:
        """
        Enrichment analysis of traits/cells
        :param seed_cell_en_weight: Seed cell data
        """

        if label == "run_en_none":
            if not self.is_run_none:
                log.warn("Need to run the `run_none` method first in order to run this method.")
                self.run_none()
            score = self.run_none_score
        elif label == "run_en_none_nw":
            if not self.is_run_none_nw:
                log.warn("Need to run the `run_none_nw` method first in order to run this method.")
                self.run_none_nw()
            score = self.run_none_nw_score
        elif label == "run_enrichment":
            if not self.is_run_core:
                log.warn("Need to run the `run_core` method first in order to run this method.")
                self.run_core()
            score = self.run_core_score
        elif label == "run_enrichment_nw":
            if not self.is_run_core_nw:
                log.warn("Need to run the `run_core_nw` method first in order to run this method.")
                self.run_core_nw()
            score = self.run_core_nw_score
        else:
            raise ValueError(f"{label} error. `run_en_none`, `run_en_none_nw`, `run_enrichment` or `run_enrichment_nw`")

        # Initialize enriched container
        trait_cell_enrichment = np.zeros(self.trs_data.shape)
        trait_cell_credible = np.zeros(self.trs_data.shape)

        log.info(f"Calculate {len(self.trait_list)} traits/diseases for process `{label}`. (Enrichment)")
        for i in tqdm(self.trait_range):
            # Random walk
            cell_value = self._random_walk_(seed_cell_en_weight[:, i], weight=self.weight)
            cell_value = np.array(cell_value).flatten()
            # concat
            cell_value_source = np.array(score[:, i]).flatten()
            concat_value = np.row_stack((cell_value, cell_value_source))
            concat_value_scale = mean_symmetric_scale(concat_value, axis=-1, is_verbose=False)

            # separate
            cell_value_credible = concat_value_scale[1, :] - concat_value_scale[0, :]
            trait_cell_enrichment[:, i][cell_value_credible > self.credible_threshold] = 1
            trait_cell_credible[:, i] = cell_value_credible

        self.trs_data.layers[f"{label}_tre"] = to_sparse(trait_cell_enrichment.astype(int))

        if not self.is_simple:
            self.trs_data.layers[f"credible_{label}_tre"] = to_sparse(trait_cell_credible)

    def run_en_none(self) -> None:
        """
        Removed cell weights from random walks
        """
        self._simple_error_()
        self._run_enrichment_(self.seed_cell_en_matrix, "run_en_none")
        self.is_run_en_none = True

    def run_en_none_nw(self) -> None:
        """
        Removed cell weights in random walks and cluster type weights in initial scores
        """
        self._simple_error_()
        self._run_enrichment_(self.seed_cell_en_matrix_nw, "run_en_none_nw")
        self.is_run_en_none_nw = True

    def run_enrichment(self) -> None:
        """
        Enrichment analysis
        """
        self._run_enrichment_(self.seed_cell_en_weight, "run_enrichment")
        self.is_run_en = True

    def run_enrichment_nw(self) -> None:
        """
        Removed cell cluster type weights in initial scores
        """
        self._simple_error_()
        self._run_enrichment_(self.seed_cell_en_weight_nw, "run_enrichment_nw")
        self.is_run_en_nw = True


def euclidean_distances(data1: matrix_data, data2: matrix_data = None) -> matrix_data:
    """
    Calculate the Euclidean distance between two matrices
    :param data1: First data;
    :param data2: Second data (If the second data is empty, it will default to the first data.)
    :return: Data of Euclidean distance.
    """
    log.info("Start euclidean distances")

    if data2 is None:
        data2 = data1.copy()

    data1 = to_dense(data1)
    data2 = to_dense(data2)
    __data1_sum_sq__ = np.power(data1, 2).sum(axis=1)
    data1_sum_sq = __data1_sum_sq__.reshape((-1, 1))
    data2_sum_sq = __data1_sum_sq__ if data2 is None else np.power(data2, 2).sum(axis=1)

    distances = data1_sum_sq + data2_sum_sq - 2 * data1.dot(data2.transpose())
    distances[distances < 0] = 0.0
    distances = np.sqrt(distances)
    return distances


def overlap(regions: DataFrame, variants: DataFrame) -> DataFrame:
    """
    Relate the peak region and variant site
    :param regions: peaks information
    :param variants: variants information
    :return: The variant maps data in the peak region
    """
    regions_columns: list = list(regions.columns)

    if "chr" not in regions_columns or "start" not in regions_columns or "end" not in regions_columns:
        log.error(
            f"The peaks information {regions_columns} in data `adata` must include three columns: `chr`, `start` and "
            f"`end`. (It is recommended to use the `read_sc_atac` method.)"
        )
        raise ValueError(
            f"The peaks information {regions_columns} in data `adata` must include three columns: `chr`, `start` and "
            f"`end`. (It is recommended to use the `read_sc_atac` method.)"
        )

    columns = ['variant_id', 'index', 'chr', 'position', 'rsId', 'chr_a', 'start', 'end']

    if regions.shape[0] == 0 or variants.shape[0] == 0:
        log.warn("Data is empty.")
        return pd.DataFrame(columns=columns)

    regions = regions.rename_axis("index")
    regions = regions.reset_index()
    # sort
    regions_sort = regions.sort_values(["chr", "start", "end"])[["index", "chr", "start", "end"]]
    variants_sort = variants.sort_values(["chr", "position"])[["variant_id", "chr", "position", "rsId"]]

    # Intersect and Sort
    chr_keys: list = list(set(regions_sort["chr"]).intersection(set(variants_sort["chr"])))
    chr_keys.sort()

    variants_chr_type: dict = {}
    variants_position_list: dict = {}

    # Cyclic region chromatin
    for chr_key in chr_keys:
        # variant chr information
        sort_chr_regions_chr = variants_sort[variants_sort["chr"] == chr_key]
        variants_chr_type.update({chr_key: sort_chr_regions_chr})
        variants_position_list.update({chr_key: list(sort_chr_regions_chr["position"])})

    variants_overlap_info_list: list = []

    for index, chr_a, start, end in zip(regions_sort["index"], regions_sort["chr"], regions_sort["start"], regions_sort["end"]):

        # judge chr
        if chr_a in chr_keys:
            # get chr variant
            variants_chr_type_position_list = variants_position_list[chr_a]
            # judge start and end position
            if start <= variants_chr_type_position_list[-1] and end >= variants_chr_type_position_list[0]:
                # get index
                start_index = get_index(start, variants_chr_type_position_list)
                end_index = get_index(end, variants_chr_type_position_list)

                # Determine whether it is equal, Equality means there is no overlap
                if start_index != end_index:
                    start_index = start_index if isinstance(start_index, number) else start_index[1]
                    end_index = end_index + 1 if isinstance(end_index, number) else end_index[1]

                    if start_index > end_index:
                        log.error("The end index in the region is greater than the start index.")
                        raise IndexError("The end index in the region is greater than the start index.")

                    variants_chr_type_chr_a = variants_chr_type[chr_a]
                    # get data
                    variants_overlap_info: DataFrame = variants_chr_type_chr_a[start_index:end_index].copy()
                    variants_overlap_info["index"] = index
                    variants_overlap_info["chr_a"] = chr_a
                    variants_overlap_info["start"] = start
                    variants_overlap_info["end"] = end
                    variants_overlap_info.index = (variants_overlap_info["variant_id"].astype(str) + "_" + variants_overlap_info["index"].astype(str))
                    variants_overlap_info_list.append(variants_overlap_info)

    # merge result
    if len(variants_overlap_info_list) > 0:
        overlap_data: DataFrame = pd.concat(variants_overlap_info_list, axis=0)
    else:
        return pd.DataFrame(columns=columns)

    return overlap_data


def overlap_sum(regions: AnnData, variants: dict, trait_info: DataFrame) -> AnnData:
    """
    Overlap regional data and mutation data and sum the PP values of all mutations in a region as the values for that
    region.
    :param regions: peaks data
    :param variants: variants data
    :param trait_info: traits information
    :return: overlap data
    """

    # Unique feature set
    label_all = list(regions.var.index)
    # Peak number
    label_all_size: int = len(label_all)

    # trait/disease information
    trait_names: list = list(trait_info["id"])

    matrix = np.zeros((label_all_size, len(trait_names)))

    log.info(f"Obtain peak-trait/disease matrix. (overlap variant information)")
    for trait_name in tqdm(trait_names):

        variant: AnnData = variants[trait_name]
        index: int = trait_names.index(trait_name)

        # handle overlap data
        overlap_info: DataFrame = overlap(regions.var, variant.obs)

        if overlap_info.shape[0] == 0:
            continue

        overlap_info.rename({"index": "label"}, axis="columns", inplace=True)
        overlap_info.reset_index(inplace=True)
        overlap_info["region_id"] = (
            overlap_info["chr"].astype(str)
            + ":" + overlap_info["start"].astype(str) + "-" + overlap_info["end"].astype(str)
        )

        # get region
        region_info = overlap_info.groupby("region_id", as_index=False)["label"].first()
        region_info.index = region_info["label"].astype(str)
        label: list = list(region_info["label"])

        # Mutation information with repetitive features
        label_size: int = len(label)

        for j in range(label_size):

            # Determine whether the features after overlap exist, In other words, whether there is overlap in this feature
            if label[j] in label_all:
                # get the index of label
                label_index = label_all.index(label[j])
                overlap_info_region = overlap_info[overlap_info["label"] == label[j]]
                # sum value
                overlap_variant = variant[list(overlap_info_region["variant_id"]), :]
                matrix[label_index, index] = overlap_variant.X.sum(axis=0)

    overlap_adata = AnnData(to_sparse(matrix), var=trait_info, obs=regions.var)
    overlap_adata.uns["trait_info"] = trait_info
    return overlap_adata


def calculate_init_score(
    data: matrix_data,
    overlap_data: matrix_data
) -> matrix_data:
    """
    Calculate the initial trait or disease-related cell score
    :param data: Convert the `counts` matrix to the `fragments` matrix using the `scvi.data.reads_to_fragments`
    :param overlap_data: Peaks-traits/diseases data
    :return: Initial TRS
    """
    # Processing data
    matrix = to_sparse(data)
    matrix[matrix < 0] = 0

    # Summation information
    log.info("Calculate summation information")
    row_col_multiply = np.array(matrix.sum(axis=1)).flatten()[:, np.newaxis] * np.array(matrix.sum(axis=0)).flatten()

    all_sum = matrix.sum()

    # init_score
    log.info("Calculate initial trait-cell score")
    overlap_matrix = to_dense(overlap_data)
    overlap_matrix[overlap_matrix < 0] = 0
    global_scale_data = (row_col_multiply / all_sum) @ overlap_matrix
    del row_col_multiply
    global_scale_data[global_scale_data == 0] = global_scale_data[global_scale_data != 0].min() / 2
    init_score: matrix_data = (matrix @ overlap_matrix) / global_scale_data

    return init_score


def calculate_init_score_weight(
    adata: AnnData,
    da_peaks_adata: AnnData,
    overlap_adata: AnnData,
    is_simple: bool = True
) -> AnnData:
    """
    Calculate the initial trait or disease-related cell score with weight
    :param adata: scATAC-seq data
    :param da_peaks_adata: Differential peak data
    :param overlap_adata: Peaks-traits/diseases data
    :param is_simple: True represents not adding unnecessary intermediate variables, only adding the final result. It
    is worth noting that when set to `True`, the `is_ablation` parameter will become invalid, and when set to `False`,
    `is_ablation` will only take effect;
    :return: Initial TRS with weight
    """
    if "trait_info" not in list(overlap_adata.uns.keys()):
        log.error("The description of traits/diseases `trait_info` is not in `overlap_data.uns.keys()`")
        raise ValueError("The description of traits/diseases `trait_info` is not in `overlap_data.uns.keys()`")

    # Processing data
    fragments = to_dense(adata.layers["fragments"])
    overlap_matrix = to_dense(overlap_adata.X)
    _weight_bf_ = to_dense(da_peaks_adata.X)

    # handler
    _weight_bf_tf_idf_ = to_dense(adjustment_tf_idf(_weight_bf_))
    del _weight_bf_
    weight_bf_normalize = z_score_normalize(_weight_bf_tf_idf_)
    del _weight_bf_tf_idf_
    da_peaks_adata.layers["bf_normalize"] = to_sparse(weight_bf_normalize)

    log.info("Start calculate leiden cluster init_score")
    _cluster_weight_: matrix_data = weight_bf_normalize @ overlap_matrix
    _cluster_weight_ = mean_symmetric_scale(_cluster_weight_, axis=0)
    da_peaks_adata.obsm["cluster_weight"] = to_sparse(_cluster_weight_)

    log.info("Start set weight")
    anno_info = adata.obs
    _cell_type_weight_ = np.zeros((adata.shape[0], _cluster_weight_.shape[1]))
    del _cluster_weight_

    for cluster in da_peaks_adata.obs_names:
        _cell_type_weight_[anno_info["clusters"] == cluster, :] = to_dense(
            da_peaks_adata[cluster, :].obsm["cluster_weight"], is_array=True
        ).flatten()

    _cell_type_weight_ = sigmoid(_cell_type_weight_)

    # calculate
    _init_score_ = calculate_init_score(fragments, overlap_matrix)
    log.info("Calculate initial trait-cell score with cell weight")
    _init_score_weight_ = np.multiply(_init_score_, _cell_type_weight_)

    init_score_weight_adata = AnnData(
        to_sparse(_init_score_weight_), obs=adata.obs, var=overlap_adata.uns["trait_info"]
    )

    del _init_score_weight_

    if not is_simple:
        init_score_weight_adata.layers["init_score"] = to_sparse(_init_score_)
        init_score_weight_adata.layers["cell_type_weight"] = to_sparse(_cell_type_weight_)

    del _init_score_
    del _cell_type_weight_
    init_score_weight_adata.uns["is_sample"] = is_simple
    return init_score_weight_adata


def obtain_cell_cell_network(
    adata: AnnData,
    k: int = 30,
    or_k: int = 3,
    weight: float = 0.01,
    is_simple: bool = True
) -> AnnData:
    """
    Calculate cell-cell correlation
    :param adata: scATAC-seq data;
    :param k: When building an mKNN network, the number of nodes connected by each node (and);
    :param or_k: When building an mKNN network, the number of nodes connected by each node (or);
    :param weight: The weight of interactions or operations;
    :param is_simple: True represents not adding unnecessary intermediate variables, only adding the final result.
        It is worth noting that when set to `True`, the `is_ablation` parameter will become invalid, and when set to
        `False`, `is_ablation` will only take effect;
    :return: Cell similarity data.
    """
    # data
    if "poisson_vi" not in adata.uns.keys():
        log.error(
            "`poisson_vi` is not in the `adata.uns` dictionary, and the scATAC-seq data needs to be processed through "
            "the `poisson_vi` function."
        )
        raise ValueError(
            "`poisson_vi` is not in the `adata.uns` dictionary, and the scATAC-seq data needs to be processed through "
            "the `poisson_vi` function."
        )

    _latent_name_ = "latent" if adata.uns["poisson_vi"]["latent_name"] is None else adata.uns["poisson_vi"]["latent_name"]
    latent = adata.obsm[_latent_name_]
    del _latent_name_
    cell_anno = adata.obs

    # euclidean distances
    _ed_data_ = euclidean_distances(latent)
    _ed_scale_data_ = mean_symmetric_scale(_ed_data_, axis=1)
    del _ed_data_

    log.info("Start affinity matrix")
    _distances_ = to_dense(_ed_scale_data_, is_array=True)
    del _ed_scale_data_
    _affinity_data_ = stats.gamma.pdf(_distances_, a=1, scale=1)
    del _distances_
    cell_affinity = mean_symmetric_scale(_affinity_data_, axis=1)
    del _affinity_data_

    # Define KNN network
    cell_mutual_knn_weight, cell_mutual_knn = semi_mutual_knn_weight(
        cell_affinity, neighbors=k, or_neighbors=or_k, weight=weight
    )

    # cell-cell graph
    cc_data: AnnData = AnnData(to_sparse(cell_mutual_knn_weight), var=cell_anno, obs=cell_anno)
    cc_data.layers["cell_affinity"] = to_sparse(cell_affinity)

    if not is_simple:
        cc_data.layers["cell_mutual_knn"] = to_sparse(cell_mutual_knn)

    return cc_data
