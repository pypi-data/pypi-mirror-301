from pydantic import BaseModel, Field, BaseConfig
from typing import Optional, Any, List, Dict, Union
from enum import Enum


class FeatureTypeEnum(str, Enum):
    string = 'String Feature'
    datetime = 'Datetime Feature'
    numeric = 'Numeric Feature'
    categorical = 'Categorical Feature'  # 추가됨
    boolean = 'Boolean Feature'  # 추가됨


class ColumnInfo(BaseModel):
    colname: str
    dtype: str
    feature_type: FeatureTypeEnum
    timezone: Optional[str] = None  # 날짜시간 데이터에 대한 시간대 추가

    class Config(BaseConfig):
        populate_by_name = True
        use_enum_values = True  # 열거형의 값들이 출력될 때 실제 문자열 값이 사용되도록 하였습니다.


class ColumnStatsInfo(ColumnInfo):
    # 수치 데이터에 대한 통계
    mean: Optional[float] = Field(None)
    median: Optional[float] = Field(None)
    min: Optional[float] = Field(None)
    max: Optional[float] = Field(None)
    standard_deviation: Optional[float] = Field(None)

    # 범주형 데이터에 대한 통계
    mode: Optional[str | int | float] = None  # 모드 추가
    frequency: Optional[Dict[Union[str, int, float], int]] = None  # 빈도수 추가

    # 공통 통계
    unique_values: Optional[List[int | float | str]] = None
    missing_values: Optional[int] = None
    count: Optional[int] = None
    unique: Optional[int] = None

    # top: Optional[str] = Field(None)
    # freq: Optional[int] = Field(None)

    # 퍼센트값 필드
    value_25_percent: Optional[float] = Field(None, alias='25%')
    value_50_percent: Optional[float] = Field(None, alias='50%')
    value_75_percent: Optional[float] = Field(None, alias='75%')


class DataFrameInfo(BaseModel):
    rows_cols_num: Optional[tuple[int, int]] = Field(None)
    column_type_list: Optional[List[str]] = Field(None)
    column_name_list: Optional[List[str]] = Field(None)


class DataFrameStatsInfo(DataFrameInfo):
    correlations: Optional[Dict[str, Dict[str, Any]]] = None
    describe: Optional[Dict[str, Dict[str, Any]]] = None
