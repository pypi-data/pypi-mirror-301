from typing import List
import numpy as np
from scipy.stats import logistic
from schema.pipeline import (RawData,
                             RowsCols,
                             MissingValues, CleaningModeEnum,
                             Outlier, OutlierClipModeEnum, OutlierThresholdMode, OutlierSubstitutionMode,
                             Normalization, NormalizeTransformMethod, PipeInfo)
from schema.stats import DataFrameStatsInfo, ColumnStatsInfo

import pandas as pd
import warnings
warnings.filterwarnings('ignore', category=pd.errors.SettingWithCopyWarning)


class DeployPipeline:
    def __init__(self,
                 pipeline_steps: List[PipeInfo],
                 df_stats: DataFrameStatsInfo,
                 col_stats: List[ColumnStatsInfo]
                 ):
        self.pipeline_steps = pipeline_steps
        self.df_stats = df_stats
        self.col_stats = col_stats
        self._verbose = True

        # col_stats 초기화 확인
        if not self.col_stats:
            raise ValueError("col_stats는 제공되어야 하며 None일 수 없습니다")

        self.col_stats_dict = {col_stat.colname: col_stat for col_stat in self.col_stats}

        raw_data_column_info = []
        if df_stats.column_name_list and df_stats.column_type_list:
            raw_data_column_info = [(name, type_) for name, type_ in
                                    zip(df_stats.column_name_list, df_stats.column_type_list)]

        self._raw_data_column_info = raw_data_column_info  # [(컬럼이름, 타입)] 튜플 리스트

    def set_verbose(self, value):
        self._verbose = value

    def _get_col_stat(self, column_name):
        col_stat = self.col_stats_dict.get(column_name)
        if not col_stat:
            raise ValueError(f'{column_name} 컬럼에 대한 통계 정보가 없습니다')
        return col_stat

    def pipe_raw_data(self, df, params: dict):
        if self._verbose:
            print('파이프라인 : 데이터 입력')
        params = RawData.model_validate(params)  # 타입캐스팅
        # print('pipe rawdata', params)
        return df

    def get_raw_data_column_info(self):
        return self._raw_data_column_info

    # 행/열 자르기
    def pipe_rows_cols(self, df, params: dict):
        if self._verbose:
            print('파이프라인 : 행/열 처리 중...')
        params = RowsCols.model_validate(params)
        # print('pipe rows cols', params)

        """ 행 자르기 """

        """ 열 자르기 """
        # toggles 가 True인 항목만 필터링
        select_cols = [item.key for item in params.toggles if item.value and item.key in df.columns]
        df = df[select_cols]

        return df

    # 결측치 처리
    def pipe_missing_values(self, df, params: dict):
        if self._verbose:
            print('파이프라인 : 결측치 처리 중...')
        params = MissingValues.model_validate(params)

        if not params.colname_list:
            raise ValueError('적용할 컬럼을 선택해야합니다')

        for col in params.colname_list:
            if col not in df.columns:
                raise ValueError(f'{col} 컬럼이 데이터프레임에 존재하지 않습니다')

            col_stat = self._get_col_stat(col)

            if params.cleaning_mode == CleaningModeEnum.subsitution_value:
                df[col] = df[col].fillna(params.replacement_value)
            elif params.cleaning_mode == CleaningModeEnum.replace_mean:
                if col_stat.mean is not None:
                    df[col] = df[col].fillna(col_stat.mean)
                else:
                    raise ValueError(f'{col} 컬럼에 대한 mean 통계 정보가 없습니다')
            elif params.cleaning_mode == CleaningModeEnum.replace_median:
                if col_stat.median is not None:
                    df[col] = df[col].fillna(col_stat.median)
                else:
                    raise ValueError(f'{col} 컬럼에 대한 median 통계 정보가 없습니다')
            elif params.cleaning_mode == CleaningModeEnum.replace_mode:
                if col_stat.mode is not None:
                    df[col] = df[col].fillna(col_stat.mode)
                else:
                    raise ValueError(f'{col} 컬럼에 대한 mode 통계 정보가 없습니다')
            elif params.cleaning_mode == CleaningModeEnum.remove_row:
                df = df.dropna(subset=[col], axis=0)
            elif params.cleaning_mode == CleaningModeEnum.remove_column:
                df = df.drop(labels=[col], axis=1)
            else:
                raise ValueError('cleaning_mode not found')

        return df

    # 이상치 처리
    def handle_threshold_operation(self, df, column_name, threshold, substitution_mode):
        col_stat = self._get_col_stat(column_name)

        if substitution_mode == OutlierSubstitutionMode.threshold:
            df.loc[df[column_name] >= threshold, column_name] = threshold
        elif substitution_mode == OutlierSubstitutionMode.mean:
            if col_stat.mean is not None:
                df.loc[df[column_name] >= threshold, column_name] = col_stat.mean
            else:
                raise ValueError(f'{column_name} 컬럼에 대한 mean 통계 정보가 없습니다')
        elif substitution_mode == OutlierSubstitutionMode.median:
            if col_stat.median is not None:
                df.loc[df[column_name] >= threshold, column_name] = col_stat.median
            else:
                raise ValueError(f'{column_name} 컬럼에 대한 median 통계 정보가 없습니다')
        elif substitution_mode == OutlierSubstitutionMode.missing:
            df.loc[df[column_name] >= threshold, column_name] = np.nan
        return df

    def pipe_outliers(self, df, params: dict):
        if self._verbose:
            print('파이프라인 : 이상치 처리 중...')
        params = Outlier.model_validate(params)

        for column_name in params.colname_list:
            if params.clip_mode in [OutlierClipModeEnum.clip_peaks, OutlierClipModeEnum.clip_peaks_and_subpeaks]:  # 상한
                if params.threshold_mode == OutlierThresholdMode.constant:
                    threshold = params.upperbound_value
                else:
                    threshold = df[column_name].quantile((params.upperbound_value - 1) / (100 - 1))
                df = self.handle_threshold_operation(df, column_name, threshold, params.sub_value_peaks)

            if params.clip_mode in [OutlierClipModeEnum.clip_subpeaks,
                                    OutlierClipModeEnum.clip_peaks_and_subpeaks]:  # 하한
                if params.threshold_mode == OutlierThresholdMode.constant:
                    threshold = params.lowerbound_value
                else:
                    threshold = df[column_name].quantile((params.lowerbound_value - 1) / (100 - 1))

                df = self.handle_threshold_operation(df, column_name, threshold, params.sub_value_subpeaks)

        return df

    # 정규화/표준화
    def pipe_normalization(self, df, params: dict):
        if self._verbose:
            print('파이프라인 : 정규화 처리 중...')
        params = Normalization.model_validate(params)
        # print('pipe normalization', params)
        method = params.transform_method
        column_list = params.colname_list
        use_0 = params.use_0

        for column in column_list:
            if column not in df.columns:
                raise ValueError(f'Column "{column}" does not exist in the DataFrame.')

            col_stat = self._get_col_stat(column)

            if method == NormalizeTransformMethod.z_score:
                if col_stat.mean is not None and col_stat.standard_deviation is not None:
                    df.loc[:, column] = (df[column] - col_stat.mean) / col_stat.standard_deviation
                else:
                    raise ValueError(f'{column} 컬럼에 대한 mean 또는 standard deviation 통계 정보가 없습니다')
            elif method == NormalizeTransformMethod.min_max:
                if col_stat.min is not None and col_stat.max is not None:
                    df.loc[:, column] = (df[column] - col_stat.min) / (col_stat.max - col_stat.min)
                else:
                    raise ValueError(f'{column} 컬럼에 대한 min 또는 max 통계 정보가 없습니다')
            elif method == NormalizeTransformMethod.logistic:
                df.loc[:, column] = logistic.cdf(df[column])
            elif method == NormalizeTransformMethod.log_normal:
                df.loc[:, column] = np.log(df[column] - col_stat.min + 1)
            elif method == NormalizeTransformMethod.tanh:
                df.loc[:, column] = np.tanh(df[column])
            else:
                raise ValueError("Unsupported normalization method")

            # If use_0 is True and the column is constant, change all its values to 0.
            if use_0 and df[column].nunique() == 1:
                df.loc[:, column] = 0

        return df

    def process_pipeline(self, df):
        pipeline_process_mapping = {
            "raw_data": self.pipe_raw_data,
            "rows_cols": self.pipe_rows_cols,
            "missing_values": self.pipe_missing_values,
            "outliers": self.pipe_outliers,
            "normalization": self.pipe_normalization,
        }

        for pipe_info in self.pipeline_steps:
            process_method = pipeline_process_mapping.get(pipe_info.type)

            if process_method:
                df = process_method(df, pipe_info.params.model_dump())
                if self._verbose:
                    print('ok')

        return df
