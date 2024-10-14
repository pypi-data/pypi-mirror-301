from pydantic import BaseModel, Field, BaseConfig
from typing import Optional, Any, List, Union, Dict
from enum import Enum
from datetime import datetime


class ToggleItem(BaseModel):
    key: str
    value: bool


class OutlierClipModeEnum(str, Enum):
    clip_peaks = 'clip_peaks'
    clip_subpeaks = 'clip_subpeaks'
    clip_peaks_and_subpeaks = 'clip_peaks_and_subpeaks'


class OutlierThresholdMode(str, Enum):
    constant = 'constant'
    percentile = 'percentile'


class OutlierSubstitutionMode(str, Enum):
    threshold = 'threshold'
    mean = 'mean'
    median = 'median'
    missing = 'missing'


class CleaningModeEnum(str, Enum):
    subsitution_value = "subsitution_value"
    replace_mean = "replace_mean"
    replace_median = "replace_median"
    replace_mode = "replace_mode"
    remove_row = "remove_row"
    remove_column = "remove_column"


class NormalizeTransformMethod(str, Enum):
    z_score = "z_score"
    min_max = "min_max"
    logistic = "logistic"
    log_normal = "log_normal"
    tanh = "tanh"


class PipeParams(BaseModel):
    pass

    class Config(BaseConfig):
        use_enum_values = True


class RawData(PipeParams):
    raw_data_db_path: str = Field(...)


class RowsCols(PipeParams):
    row_start: int = Field(...)
    row_end: int = Field(...)
    toggles: Optional[List[ToggleItem]] = Field(...)


class Normalization(PipeParams):
    transform_method: NormalizeTransformMethod = Field(...)
    use_0: Optional[bool] = Field(None)
    colname_list: Optional[List[str]] = Field(None)


class MissingValues(PipeParams):
    min_ratio: float = Field(...)
    max_ratio: float = Field(...)
    cleaning_mode: CleaningModeEnum = Field(...)
    replacement_value: Optional[int | float] = Field(None)
    colname_list: Optional[List[str]] = Field(None)


class Outlier(PipeParams):
    clip_mode: OutlierClipModeEnum = Field(...)
    threshold_mode: OutlierThresholdMode = Field(...)
    upperbound_value: Optional[int | float] = Field(None)
    lowerbound_value: Optional[int | float] = Field(None)
    sub_value_peaks: Optional[OutlierSubstitutionMode] = Field(None)
    sub_value_subpeaks: Optional[OutlierSubstitutionMode] = Field(None)
    colname_list: Optional[List[str]] = Field(None)


class PipeTypeEnum(str, Enum):
    raw_data = 'raw_data'
    rows_cols = 'rows_cols'
    missing_values = 'missing_values'
    outliers = 'outliers'
    normalization = 'normalization'


class PipeCreate(BaseModel):
    type: PipeTypeEnum = Field(...)
    params: RawData | RowsCols | Normalization | MissingValues | Outlier = Field(...)
    description: Optional[str] = Field(None)


class PipeInfo(BaseModel):
    step: int = Field(...)
    type: PipeTypeEnum = Field(...)
    params: RawData | RowsCols | Normalization | MissingValues | Outlier = Field(...)
    description: Optional[str] = Field(None)
    insert_date: datetime = Field(...)

    class Config(BaseConfig):
        use_enum_values = True
