from anomalylab.config import *
from anomalylab.empirical import (
    Correlation,
    FamaMacBethRegression,
    Persistence,
    PortfolioAnalysis,
    Summary,
)
from anomalylab.preprocess import FillNa, Normalize, Shift, Winsorize
from anomalylab.structure import PanelData, TimeSeries
from anomalylab.utils import *
from anomalylab.utils.imports import *


@dataclass
class Panel:
    df: DataFrame
    name: Optional[str] = None
    id: str = "id"
    time: str = "date"
    frequency: Literal["D", "M", "Y"] = "M"
    ret: str = "return"
    classifications: Optional[list[str] | str] = None

    def __post_init__(self) -> None:
        self.panel_data: PanelData = PanelData(
            df=self.df,
            name=self.name,
            id=self.id,
            time=self.time,
            frequency=self.frequency,
            ret=self.ret,
            classifications=self.classifications,
        )
        self.panel_data.set_flag()
        self.normalize_processor = None
        self.fillna_processor = None
        self.winsorize_processor = None
        self.shift_processor = None
        self.summary_processor = None
        self.correlation_processor = None
        self.fm_preprocessor = None

    def __repr__(self) -> str:
        return repr(self.panel_data)

    def normalize(
        self,
        columns: Columns = None,
        method: Literal["zscore", "rank"] = "zscore",
        group_columns: Columns = None,
        no_process_columns: Columns = None,
        process_all_characteristics: bool = True,
    ) -> None:
        if self.normalize_processor is None:
            self.normalize_processor = Normalize(panel_data=self.panel_data)
        self.panel_data = self.normalize_processor.normalize(
            columns=columns,
            method=method,
            group_columns=group_columns,
            no_process_columns=no_process_columns,
            process_all_characteristics=process_all_characteristics,
        ).panel_data

    def fillna(
        self,
        columns: Columns = None,
        method: Literal["mean", "median", "constant"] = "mean",
        value: Optional[Union[float, int]] = None,
        group_columns: Columns = None,
        no_process_columns: Columns = None,
        process_all_characteristics: bool = True,
    ) -> None:
        if self.fillna_processor is None:
            self.fillna_processor = FillNa(panel_data=self.panel_data)
        self.panel_data = self.fillna_processor.fillna(
            columns=columns,
            method=method,
            value=value,
            group_columns=group_columns,
            no_process_columns=no_process_columns,
            process_all_characteristics=process_all_characteristics,
        ).panel_data

    def fill_group_column(self, group_column: str, value: Scalar) -> None:
        if self.fillna_processor is None:
            self.fillna_processor = FillNa(panel_data=self.panel_data)
        self.panel_data = self.fillna_processor.fill_group_column(
            group_column=group_column, value=value
        ).panel_data

    def winsorize(
        self,
        columns: Columns = None,
        method: Literal["winsorize", "truncate"] = "winsorize",
        limits: tuple[float, float] = (0.01, 0.01),
        group_columns: list[str] | str = "time",
        no_process_columns: Columns = None,
        process_all_characteristics: bool = True,
    ) -> None:
        if self.winsorize_processor is None:
            self.winsorize_processor = Winsorize(panel_data=self.panel_data)
        self.panel_data = self.winsorize_processor.winsorize(
            columns=columns,
            method=method,
            limits=limits,
            group_columns=group_columns,
            no_process_columns=no_process_columns,
            process_all_characteristics=process_all_characteristics,
        ).panel_data

    def shift(
        self,
        columns: Columns = None,
        periods: int | list[int] = 1,
        no_process_columns: Columns = None,
        process_all_characteristics: bool = True,
        drop_original: bool = False,
        dropna: bool = False,
    ) -> None:
        if self.shift_processor is None:
            self.shift_processor = Shift(panel_data=self.panel_data)
        self.panel_data = self.shift_processor.shift(
            columns=columns,
            periods=periods,
            no_process_columns=no_process_columns,
            process_all_characteristics=process_all_characteristics,
            drop_original=drop_original,
            dropna=dropna,
        ).panel_data

    def summary(
        self,
        columns: Columns = None,
        no_process_columns: Columns = None,
        process_all_characteristics: bool = True,
        decimal: Optional[int] = None,
    ) -> DataFrame:
        if self.summary_processor is None:
            self.summary_processor = Summary(panel_data=self.panel_data)
        return self.summary_processor.average_statistics(
            columns=columns,
            no_process_columns=no_process_columns,
            process_all_characteristics=process_all_characteristics,
            decimal=decimal,
        )

    def correlation(
        self,
        columns: Columns = None,
        no_process_columns: Columns = None,
        process_all_characteristics: bool = True,
        decimal: Optional[int] = None,
    ) -> DataFrame:
        if self.correlation_processor is None:
            self.correlation_processor = Correlation(panel_data=self.panel_data)
        return self.correlation_processor.average_correlation(
            columns=columns,
            no_process_columns=no_process_columns,
            process_all_characteristics=process_all_characteristics,
            decimal=decimal,
        )

    def fm_reg(
        self,
        dependent: Optional[str] = None,
        exogenous: Optional[list[str]] = None,
        models: Optional[list[list[str] | dict[str, list[str]]]] = None,
        exogenous_order: Optional[list[str]] = None,
        model_names: Optional[list[str]] = None,
        weight_column: Optional[str] = None,
        industry_column: Optional[str] = None,
        industry_weighed_method: Literal["value", "equal"] = "value",
        is_winsorize: bool = False,
        is_normalize: bool = False,
        decimal: Optional[int] = None,
    ) -> DataFrame:
        if self.fm_preprocessor is None:
            self.fm_preprocessor = FamaMacBethRegression(panel_data=self.panel_data)
        return self.fm_preprocessor.fit(
            dependent=dependent,
            exogenous=exogenous,
            models=models,
            exogenous_order=exogenous_order,
            model_names=model_names,
            weight_column=weight_column,
            industry_column=industry_column,
            industry_weighed_method=industry_weighed_method,
            is_winsorize=is_winsorize,
            is_normalize=is_normalize,
            decimal=decimal,
        )


if __name__ == "__main__":
    from anomalylab.datasets import DataSet
    from anomalylab.preprocess.fillna import FillNa

    df: DataFrame = DataSet.get_panel_data()
    panel = Panel(df, classifications="industry")
    pp(panel)
    panel.fill_group_column(group_column="industry", value="Other")
    panel.fillna(
        # columns="size",
        method="mean",
        group_columns="time",
        no_process_columns="size",
        process_all_characteristics=True,
    )
    panel.normalize(
        # columns="size",
        # method="zscore",
        # group_columns="time",
        # no_process_columns="size",
        # process_all_characteristics=False,
    )
    panel.winsorize()
    # panel.shift()
    pp(panel)
    pp(panel.summary())
    pp(panel.correlation())
    pp(
        panel.fm_reg(
            models=[
                ["ret", "size", "illiquidity"],
                ["ret", "size"],
                ["ret", "idiosyncratic_volatility"],
            ],
            weight_column="size",
            industry_column="industry",
            industry_weighed_method="value",
            is_winsorize=True,
            is_normalize=True,
        )
    )
