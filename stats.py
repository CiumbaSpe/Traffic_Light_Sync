import pandas as pd
import numpy as np
import scipy.stats as st
import setting

class Statistics: 
    def __init__(self):
        self.name = setting.NAME
        pass

    def metrics_type(self, value):
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
    
    def evaluate_on_observation(self, obs):
        """
        Evaluate statistics for each metric (attribute) in the observation.

        Arguments:
            obs: A list of objects with attributes to be analyzed.

        Returns:
            A list of DataFrames, each containing statistics for one metric.
        """
        if not obs:
            return []

        data_frame_for_obs = []
        # Get the list of keys from the first object
        for key in obs[0].__dict__.keys():
            # Determine the type based on the first object's value for the key
            metric_type = self.metrics_type(getattr(obs[0], key, None))
            if metric_type is None:
                continue

            values = []
            # Aggregate values from all objects for the given key
            for obj in obs:
                value = getattr(obj, key, None)
                current_type = self.metrics_type(value)
                if current_type == "array":
                    values.append(np.mean(value))
                elif current_type == "scalar":
                    values.append(value)

            if values:
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

    def evaluate_metrics(self, config, sim = None):
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
                idx = [f"perm_{str(i)}_config_{str(j)}" for i in range(sim.permutations) for j in range(0, sim.configuration, sim.configuration_step)]
                concat_metrics.index = idx

            combined_df.append(concat_metrics)

        return combined_df

    def save_stats(self, combined_df, index=False):
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


