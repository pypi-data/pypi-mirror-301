import numpy as np
import pandas as pd
from numba import typed
from simba.utils.read_write import find_files_of_filetypes_in_directory, read_df, get_fn_ext
from simba.mixins.circular_statistics import CircularStatisticsMixin
from simba.mixins.feature_extraction_mixin import FeatureExtractionMixin
from simba.mixins.timeseries_features_mixin import TimeseriesFeatureMixin
import seaborn as sns

data_dir = r'C:\troubleshooting\mitra\project_folder\csv\features_extracted'
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
    nose_arr = df[['Nose_x', 'Nose_y']].values.astype(np.float32)
    left_ear_arr = df[['Left_ear_x', 'Left_ear_y']].values.astype(np.float32)
    right_ear_arr = df[['Right_ear_x', 'Right_ear_y']].values.astype(np.float32)
    center_shifted = FeatureExtractionMixin.create_shifted_df(df[['Center_x', 'Center_y']])
    center_1 = center_shifted.iloc[:, 0:2].values
    center_2 = center_shifted.iloc[:, 2:4].values
    df['angle_degrees'] = CircularStatisticsMixin().direction_three_bps(nose_loc=nose_arr, left_ear_loc=left_ear_arr, right_ear_loc=right_ear_arr).astype(np.int32)
    sliding_circular_range = CircularStatisticsMixin().sliding_circular_range(data=df['angle_degrees'].values.astype(np.float32), time_windows=np.array([5, 10, 15, 20], dtype=np.float64), fps=30)
    movement = FeatureExtractionMixin.euclidean_distance(bp_1_x=center_1[:, 0].flatten(), bp_2_x=center_2[:, 0].flatten(), bp_1_y=center_1[:, 1].flatten(), bp_2_y=center_2[:, 1].flatten(), px_per_mm=2.15)
    movement_sum = TimeseriesFeatureMixin.sliding_descriptive_statistics(data=movement.astype(np.float32), window_sizes=np.array([5, 10, 15, 20], dtype=np.float64), sample_rate=30, statistics=typed.List(["sum"])).astype(np.int32)[0]
    movement_df = pd.DataFrame(movement_sum, columns=['Movement_5s', 'Movement_10s', 'Movement_15s', 'Movement_20s'])
    sliding_circular_range_df = pd.DataFrame(sliding_circular_range, columns=['Circular_range_5s', 'Circular_range_10s', 'Circular_range_15s', 'Circular_range_20s'])
    out = pd.concat([movement_df, sliding_circular_range_df], axis=1)
    out['video'] = get_fn_ext(filepath=file_path)[1]
    out['drug'] = drug
    out['group'] = group
    out['condition'] = f'{group}_{drug}'.upper()
    results.append(out)

out = pd.concat(results, axis=0)
results = pd.DataFrame(columns=['DRUG', 'GROUP', 'CONDITION', 'TIME'])
for video in out['video'].unique():
    video_df = out[out['video'] == video].reset_index(drop=True)
    drug, group, condition = video_df['drug'].iloc[0], video_df['group'].iloc[0], video_df['condition'].iloc[0]
    print(video_df['Circular_range_20s'].max())
    video_df = video_df[video_df['Circular_range_20s'] >= 350]
    if len(video_df) == 0:
        time = 0
    else:
        time = len(video_df) / 30
    results.loc[len(results)] = [drug, group, condition, time]



plot = sns.stripplot(data=results, x='CONDITION', y='TIME')

#plot = sns.histplot(data=results, x="CONDITION", hue="TIME", element="bars")






#
#
#
#
#
#
# data_dir = r'C:\troubleshooting\mitra\project_folder\csv\targets_inserted'
# data_files = find_files_of_filetypes_in_directory(directory=data_dir, extensions=['.csv'])
#
# results = []
#
# for file_cnt, file_path in enumerate(data_files):
#     df = read_df(file_path=file_path, file_type='csv')
#     nose_arr = df[['Nose_x', 'Nose_y']].values.astype(np.float32)
#     left_ear_arr = df[['Left_ear_x', 'Left_ear_y']].values.astype(np.float32)
#     right_ear_arr = df[['Right_ear_x', 'Right_ear_y']].values.astype(np.float32)
#     center_shifted = FeatureExtractionMixin.create_shifted_df(df[['Center_x', 'Center_y']])
#     center_1 = center_shifted.iloc[:, 0:2].values
#     center_2 = center_shifted.iloc[:, 2:4].values
#     df['angle_degrees'] = CircularStatisticsMixin().direction_three_bps(nose_loc=nose_arr, left_ear_loc=left_ear_arr, right_ear_loc=right_ear_arr).astype(np.int32)
#     sliding_circular_range = CircularStatisticsMixin().sliding_circular_range(data=df['angle_degrees'].values.astype(np.float32), time_windows=np.array([5, 10, 15, 20], dtype=np.float64), fps=30)
#     movement = FeatureExtractionMixin.euclidean_distance(bp_1_x=center_1[:, 0].flatten(), bp_2_x=center_2[:, 0].flatten(), bp_1_y=center_1[:, 1].flatten(), bp_2_y=center_2[:, 1].flatten(), px_per_mm=2.15)
#     movement_sum = TimeseriesFeatureMixin.sliding_descriptive_statistics(data=movement.astype(np.float32), window_sizes=np.array([5, 10, 15, 20], dtype=np.float64), sample_rate=30, statistics=typed.List(["sum"])).astype(np.int32)[0]
#     movement_df = pd.DataFrame(movement_sum, columns=['Movement_5s', 'Movement_10s', 'Movement_15s', 'Movement_20s'])
#     sliding_circular_range_df = pd.DataFrame(sliding_circular_range, columns=['Circular_range_5s', 'Circular_range_10s', 'Circular_range_15s', 'Circular_range_20s'])
#     out = pd.concat([df['circling'], movement_df, sliding_circular_range_df], axis=1)
#
#     out['video'] = get_fn_ext(filepath=file_path)[1]
#     results.append(out)
#     print(file_cnt)
#
#
# out = pd.concat(results, axis=0).reset_index(drop=True)
# non_circle_df = out[out['circling'] == 0]
# circle_df = out[out['circling'] == 1]
# non_circle_df = non_circle_df.sample(n=int(len(circle_df) * 2))
# new_out = pd.concat([circle_df, non_circle_df], axis=0)
#
#
# plot = sns.histplot(data=new_out, x="Circular_range_10s", hue="circling", element="step")

    # circling_df = df[df['circling'] == 1]
    # print(circling_df, file_cnt)




