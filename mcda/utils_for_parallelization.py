from mcda.utility_functions.aggregation import Aggregation
import pandas as pd
import multiprocess as mp
import multiprocessing
from typing import List, Tuple

def initialize_and_call_aggregation(args: Tuple[list, dict]) -> pd.DataFrame:
    weights,data = args
    agg = Aggregation(weights)

    scores_one_run = aggregate_indicators_in_parallel(agg,data)

    return scores_one_run

def aggregate_indicators_in_parallel(agg: object, normalized_indicators: dict) -> pd.DataFrame():

        scores_weighted_sum_standardized = agg.weighted_sum(normalized_indicators["standardized"])
        scores_weighted_sum_minmax = agg.weighted_sum(normalized_indicators["minmax_01"])
        scores_weighted_sum_target = agg.weighted_sum(normalized_indicators["target_01"])
        scores_weighted_sum_rank = agg.weighted_sum(normalized_indicators["rank"])

        scores_geometric_standardized = agg.geometric(normalized_indicators["standardized"])
        scores_geometric_minmax = agg.geometric(normalized_indicators["minmax_no0"])
        scores_geometric_target = agg.geometric(normalized_indicators["target_no0"])
        scores_geometric_rank = agg.geometric(normalized_indicators["rank"])

        scores_harmonic_standardized = agg.harmonic(normalized_indicators["standardized"])
        scores_harmonic_minmax = agg.harmonic(normalized_indicators["minmax_no0"])
        scores_harmonic_target = agg.harmonic(normalized_indicators["target_no0"])
        scores_harmonic_rank = agg.harmonic(normalized_indicators["rank"])

        scores_minimum_standardized = agg.minimum(normalized_indicators["standardized"])

        scores = pd.concat([scores_weighted_sum_standardized,scores_weighted_sum_minmax,scores_weighted_sum_target,scores_weighted_sum_rank,
                            scores_geometric_standardized,scores_geometric_minmax,scores_geometric_target,scores_geometric_rank,
                            scores_harmonic_standardized,scores_harmonic_minmax,scores_harmonic_target,scores_harmonic_rank,
                            scores_minimum_standardized], axis=1)
        col_names = ['ws-stand', 'ws-minmax', 'ws-target', 'ws-rank',
                     'geom-stand', 'geom-minmax', 'geom-target', 'geom-rank',
                     'harm-stand', 'harm-minmax', 'harm-target', 'harm-rank',
                     'min-stand']

        scores.columns=col_names

        return scores

def parallelize_aggregation(args: List[tuple]) -> List[pd.DataFrame]:

    # processes = []
    #
    # for arg in args:
    #     process = mp.Process(target=initialize_and_call_aggregation, args=(arg,))
    #     process.start()
    #
    #     processes.append(process)
    #
    #     for process in processes:
    #         process.join()

    # create a synchronous multiprocessing pool with the desired number of processes
    pool = multiprocessing.Pool()
    res = pool.map(initialize_and_call_aggregation, args)
    pool.close()
    pool.join()

    return res