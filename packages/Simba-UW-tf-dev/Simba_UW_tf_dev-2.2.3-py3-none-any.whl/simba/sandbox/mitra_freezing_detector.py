import numpy as np
import pandas as pd
from numba import typed
from simba.utils.read_write import find_files_of_filetypes_in_directory, read_df, get_fn_ext
from simba.mixins.circular_statistics import CircularStatisticsMixin
from simba.mixins.feature_extraction_mixin import FeatureExtractionMixin
from simba.mixins.timeseries_features_mixin import TimeseriesFeatureMixin
import seaborn as sns
from scipy.stats import ttest_ind


data_dir = r"C:\troubleshooting\mitra\project_folder\csv\outlier_corrected_movement_location\Pre_savitzky-golay_500_smoothing_20240722162601"
data_files = find_files_of_filetypes_in_directory(directory=data_dir, extensions=['.csv'])

results = []

for file_cnt, file_path in enumerate(data_files):
    print(file_cnt)
    video_name = get_fn_ext(filepath=file_path)[1].lower()
    if '_cno_' in video_name:
        drug = 'cno'
    elif '_saline_' in video_name:
        drug = 'saline'
    else:
        drug = 'dzo'

    if '_gi_' in video_name:
        group = 'gi'
    elif '_gq_' in video_name:
        group = 'gq'
    else:
        group = 'dzo'
    df = read_df(file_path=file_path, file_type='csv')
    nose_shifted = FeatureExtractionMixin.create_shifted_df(df[['Nose_x', 'Nose_y']])
    nose_1 = nose_shifted.iloc[:, 0:2].values
    nose_2 = nose_shifted.iloc[:, 2:4].values
    nose_movement = FeatureExtractionMixin.euclidean_distance(bp_1_x=nose_1[:, 0].flatten(),
                                                              bp_2_x=nose_2[:, 0].flatten(),
                                                              bp_1_y=nose_1[:, 1].flatten(),
                                                              bp_2_y=nose_2[:, 1].flatten(), px_per_mm=2.15)


    tail_base_shifted = FeatureExtractionMixin.create_shifted_df(df[['Tail_base_x', 'Tail_base_y']])
    tail_base_shifted_1 = tail_base_shifted.iloc[:, 0:2].values
    tail_base_shifted_2 = tail_base_shifted.iloc[:, 2:4].values
    tail_base_movement = FeatureExtractionMixin.euclidean_distance(bp_1_x=tail_base_shifted_1[:, 0].flatten(),
                                                                          bp_2_x=tail_base_shifted_2[:, 0].flatten(),
                                                                          bp_1_y=tail_base_shifted_1[:, 1].flatten(),
                                                                          bp_2_y=tail_base_shifted_2[:, 1].flatten(), px_per_mm=2.15)


    left_ear_arr = df[['Left_ear_x', 'Left_ear_y']].values.astype(np.int64)
    right_ear_arr = df[['Right_ear_x', 'Right_ear_y']].values.astype(np.int64)
    nape_arr = pd.DataFrame(FeatureExtractionMixin.find_midpoints(bp_1=left_ear_arr, bp_2=right_ear_arr, percentile=np.float64(0.5)), columns=['Nape_x', 'Nape_y'])
    nape_shifted = FeatureExtractionMixin.create_shifted_df(nape_arr[['Nape_x', 'Nape_y']])

    nape_shifted_1 = nape_shifted.iloc[:, 0:2].values
    nape_shifted_2 = nape_shifted.iloc[:, 2:4].values
    nape_movement = FeatureExtractionMixin.euclidean_distance(bp_1_x=nape_shifted_1[:, 0].flatten(),
                                                              bp_2_x=nape_shifted_2[:, 0].flatten(),
                                                              bp_1_y=nape_shifted_1[:, 1].flatten(),
                                                              bp_2_y=nape_shifted_2[:, 1].flatten(), px_per_mm=2.15)

    movement = np.hstack([nose_movement.reshape(-1, 1), nape_movement.reshape(-1, 1), tail_base_movement.reshape(-1, 1)])
    mean_movement = np.mean(movement, axis=1)

    movement_mean = TimeseriesFeatureMixin.sliding_descriptive_statistics(data=nose_movement.astype(np.float32), window_sizes=np.array([2, 3, 4, 6], dtype=np.float64), sample_rate=30, statistics=typed.List(["sum"]))[0]
    movement_df = pd.DataFrame(movement_mean, columns=['Movement_2s', 'Movement_3s', 'Movement_4s', 'Movement_6s'])
    out = pd.concat([movement_df], axis=1)
    out['video'] = get_fn_ext(filepath=file_path)[1]
    out['drug'] = drug
    out['group'] = group
    out['condition'] = f'{group}_{drug}'.upper()
    results.append(out)

out = pd.concat(results, axis=0)
final_results = pd.DataFrame(columns=['DRUG', 'GROUP', 'CONDITION', '% SESSION'])
for video_cnt, video in enumerate(out['video'].unique()):
    print(video_cnt)
    video_df = out[out['video'] == video].reset_index(drop=True)
    drug, group, condition = video_df['drug'].iloc[0], video_df['group'].iloc[0], video_df['condition'].iloc[0]
    if condition == 'GQ_CNO' or condition == 'GQ_SALINE':
        freezing_df = video_df[video_df['Movement_2s'] <= 66]
        if len(freezing_df) == 0:
            time = 0
        else:
            time = (len(freezing_df) / len(video_df))
        final_results.loc[len(final_results)] = [drug, group, condition, time]



cno = final_results[final_results['CONDITION'] == 'GQ_CNO']['% SESSION'].values
saline = final_results[final_results['CONDITION'] == 'GQ_SALINE']['% SESSION'].values

ttest_ind(cno, saline, equal_var=True)


plot = sns.stripplot(data=final_results, x='CONDITION', y='% SESSION', linewidth=2)
plot = sns.barplot(data=final_results, x='CONDITION', y='% SESSION')