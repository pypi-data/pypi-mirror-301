import dill
import pandas as pd
from .api.ml.deploy_model import DeployModel
from sklearn import __version__ as sklearn_version

class ModelPredictor:
    def __init__(self, model_file):
        self.model_file = model_file
        self.model = self._load_model()
        self.report = None
        self._verbose = True
        self._set_verbose_to_subclasses(self._verbose)

    def _load_model(self) -> DeployModel:
        """
        dill을 사용하여 모델 파일을 로드합니다.
        반환되는 객체는 api.ml.deploy_model.DeployModel의 인스턴스입니다.
        """
        with open(self.model_file, 'rb') as f:
            return dill.load(f)

    def load_test_csv(self, file_path):
        return pd.read_csv(file_path)

    def get_sample(self, df, n=1):
        return df.sample(n=n)

    def compare_dataset(self, input_data):
        return self.model.compare_dataset(input_data)

    def process_pipeline(self, input_data):
        return self.model.process_pipeline(input_data)

    def predict(self, pipeline_data):
        return self.model.predict(pipeline_data)

    def pipeline_and_predict(self, input_data):
        return self.model.pipeline_and_predict(input_data)

    def get_report(self):
        self.report = self.model.get_report()
        return self.report

    def print_report(self):
        if self.report is None:
            self.get_report()

        # if self.verbose:
        print(f"회귀분류구분: {self.report['ml_type']}")
        print(f"사용목적: {self.report['ml_usage']}")

        print(f"모델 알고리즘: {self.report['model']}")
        print(f"최고 점수: {self.report['best_score']}")
        print(f"테스트 점수: {self.report['score_test']}")
        print(f"훈련 점수: {self.report['score_train']}")
        print(f"R2 점수: {self.report['r2_score']}")
        print(f"MSE 점수: {self.report['mse']}")
        print(f"RMSE 점수: {self.report['rmse']}")
        
        if 'accuracy_score' in self.report:
            print(f"정확도: {self.report['accuracy_score']}")
            print(f"혼동 행렬: {self.report['confusion_matrix']}")
            print(f"분류 결과: {self.report['classification_report']}")

    @staticmethod
    def check_sklearn_version():
        print(f"scikit-learn 버전: {sklearn_version}")

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, value):
        if not isinstance(value, bool):
            raise ValueError("verbose는 반드시 불리언 값이어야 합니다.")
        self._verbose = value
        self._set_verbose_to_subclasses(value)

    def _set_verbose_to_subclasses(self, value):
        if hasattr(self.model, 'set_verbose'):
            self.model.set_verbose(value)
        if hasattr(self.model, 'pipeline') and hasattr(self.model.pipeline, 'set_verbose'):
            self.model.pipeline.set_verbose(value)
