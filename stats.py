import pandas as pd
import numpy as np
import scipy.stats as st
import setting
from simulator import Simulation
from tracker import PerformanceTracker
from typing import Optional

class Statistics: 
    def __init__(self):
        self.name = setting.NAME
        pass

    def metrics_type(self, value: any) -> str:
        """
        Determine the metric type based on the value.

        Returns:
            "array" if the value is array-like (list, tuple, or np.ndarray),
            "scalar" if the value is numeric (int or float),
            None if the value does not match these types.
        """
        if isinstance(value, (list, tuple, np.ndarray)):
            return "array"
        elif isinstance(value, (int, float)):
            return "scalar"
        return None
    
    def evaluate_on_observation(self, obs: list[PerformanceTracker]) -> list[pd.DataFrame]:
        """
        Evaluate statistics for each metric (attribute) in the observation.

        Arguments:
            obs: A list of tracker objects with attributes to be analyzed.

        Returns:
            A list of DataFrames, each containing statistics for one metric.
        """

        data_frame_for_obs = []
        # Get the list of keys from the first object
        for key, _ in obs[0].metrics_for_stats.items():

            values = []
            # Aggregate values from all objects for the given key
            for obj in obs:
                value = obj.metrics_for_stats[key]
                current_type = self.metrics_type(value)
                if current_type == "array":
                    values.append(np.mean(value))
                elif current_type == "scalar":
                    values.append(value)

            sample_mean = np.mean(values)
            sample_variance = np.var(values, ddof=1)
            var_mean = sample_variance / len(values)

            # Calculate the t-critical value for the confidence interval
            dof = len(values) - 1
            t_critical = st.t.ppf(1 - setting.ALPHA / 2, dof)
            margin_error = t_critical * np.sqrt(var_mean)

            # Create a DataFrame for the metric
            df = pd.DataFrame({
                'mean': [sample_mean],
                'var': [sample_variance],
                'var_mean': [var_mean],
                'ci_lower': [sample_mean - margin_error],
                'ci_upper': [sample_mean + margin_error]
            })
            df.attrs['name'] = key
            data_frame_for_obs.append(df)

        return data_frame_for_obs

    def evaluate_metrics(self, config: list[list[PerformanceTracker]], sim : Optional[Simulation]) -> list[pd.DataFrame]:
        """
        Evaluate metrics for multiple configurations and optionally update DataFrame indices using simulation parameters.
        This method takes a list of configurations, where each configuration is a list of PerformanceTracker objects.
        It computes metrics for every observation in each configuration, then concatenates the metrics across configurations
        observation-wise. If a Simulation instance is provided, the indices of the resulting DataFrames are reset based on the
        simulation's 'configuration' and 'configuration_step' attributes, formatted as "config_<number>".
        
        Parameters:
            config (list[list[PerformanceTracker]]): A list where each element is a list of PerformanceTracker objects.
            sim (Optional[Simulation], optional): A Simulation instance used to adjust DataFrame indices. Defaults to None.
        
        Returns:
            list[pd.DataFrame]: A list of DataFrames, each containing the concatenated metrics for corresponding observations
                    across all configurations.
        """
        config_stats = [] # it will store statics for each configuration
        for obs in config:
            config_stats.append(self.evaluate_on_observation(obs))

        # Concatenate all DataFrames in the list into a single DataFrame
        combined_df = []
        for metrics in range(len(config_stats[0])):
            concat_metrics = pd.DataFrame()
            
            for set_of_obs in range(len(config_stats)):
                concat_metrics = pd.concat([concat_metrics, config_stats[set_of_obs][metrics]], ignore_index=True)
            
            if sim is not None:
                idx = [f"config_{str(i)}" for i in range(0, sim.configuration, sim.configuration_step)]
                concat_metrics.index = idx

            combined_df.append(concat_metrics)

        return combined_df

    def save_stats(self, combined_df : list[pd.DataFrame], index=False):
        for i in combined_df:
            i.to_csv(f"{self.name}_{i.attrs['name']}.csv", index=index)  # Set index=False to avoid saving the index column


if __name__ == "__main__":
    stats = Statistics()
    # class SampleSim:
    #     def __init__(self, configuration, permutations):
    #         self.configuration = configuration
    #         self.permutations = permutations
    #         self.configuration_step = 1
    # sim = SampleSim(configuration=2, permutations=1)
    # stats.save_stats(stats.evaluate_metrics([[[1, 2],[1, 2]], [[4, 5],[5, 6]]], sim), index=True)


