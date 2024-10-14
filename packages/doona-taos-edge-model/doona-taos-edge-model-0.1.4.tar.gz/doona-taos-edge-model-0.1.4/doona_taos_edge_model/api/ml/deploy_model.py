import pandas as pd
from sklearn.model_selection import GridSearchCV
from api.pipeline.deploy_pipeline import DeployPipeline
from schema.ml import MlScalerType, MlModelType, MlModelTrainResult
from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler, RobustScaler

ml_scalers_ref = {
    MlScalerType.standard_scaler: StandardScaler,
    MlScalerType.min_max_scaler: MinMaxScaler,
    MlScalerType.max_abs_scaler: MaxAbsScaler,
    MlScalerType.robust_scaler: RobustScaler,
}


class DeployModel:
    def __init__(self,
                 version_name: str,
                 description: str,
                 target_column: str,
                 scaler_type: MlScalerType,
                 ml_type: MlModelType,
                 ml_class: str,
                 ml_usage: str,
                 pipeline_instance: DeployPipeline,
                 fitted_gs: GridSearchCV,
                 train_result: MlModelTrainResult):
        self.version_name = version_name
        self.description = description
        self.target_column = target_column
        self.scaler_type = scaler_type
        self.ml_type = ml_type
        self.ml_class = ml_class
        self.ml_usage = ml_usage
        self.pipeline = pipeline_instance
        self.gs = fitted_gs
        self.train_result = train_result
        self._verbose = True

    def set_verbose(self, value):
        self._verbose = value
        if hasattr(self, 'pipeline'):
            self.pipeline.set_verbose(value)

    def process_pipeline(self, df):
        return self.pipeline.process_pipeline(df)

    def compare_dataset(self, plc_dataframe: pd.DataFrame):
        raw_data_column_info = self.pipeline.get_raw_data_column_info()
        raw_data_column_info = sorted(raw_data_column_info)
        plc_data_column_info = sorted(
            (name, dtype.name) for name, dtype in zip(plc_dataframe.dtypes.index, plc_dataframe.dtypes.values))
        if self._verbose:
            print("학습 RAW 데이터 구조: ", raw_data_column_info, sep='\n')
            print("입력된 장비 데이터 구조:", plc_data_column_info, sep='\n')

        return raw_data_column_info == plc_data_column_info

    def predict(self, df: pd.DataFrame):
        if self._verbose:
            print('파이프라인 : 타겟컬럼제외')

        x = df.drop([self.target_column], axis=1)

        if self._verbose:
            print('ok')

        if self._verbose:
            print('파이프라인 : 스케일링적용')

        scaler_class = ml_scalers_ref.get(self.scaler_type)
        scaler = scaler_class()
        x_scaled = scaler.fit_transform(x)

        if self._verbose:
            print('ok')

        if self._verbose:
            print('모델예측 : 계산중...')

        result = self.gs.predict(x_scaled)

        if self._verbose:
            print('ok')
        return result

    def pipeline_and_predict(self, df: pd.DataFrame):
        pipeline_df = self.process_pipeline(df)
        return self.predict(pipeline_df)

    def get_report(self):
        score_result_dict = self.train_result.model_dump()
        score_result_dict.update({
            "version_name": self.version_name,
            "description": self.description,
            "target_column": self.target_column,
            "scaler_type": self.scaler_type.value,
            "ml_type": self.ml_type.value,
            "ml_class": self.ml_class,
            "ml_usage": self.ml_usage,
        })
        return score_result_dict
