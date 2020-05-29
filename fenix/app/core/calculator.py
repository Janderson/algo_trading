from app.core.cdataframe import CDataFrame, CCalcDataFrame
from app.core.filter_dataframe import begin_build_bars, end_build_bars
from app.indicators.indicators_collection import IndicatorsCollection


class Calculator:
    def __init__(self, cdataframe: CDataFrame):
        self.cdataframe = cdataframe
        self.indicators = IndicatorsCollection()

    def add_indicator(self, indicator):
        self.indicators.add(indicator)

    def add_indicators(self, indicators):
        for indicator in indicators:
            self.indicators.add(indicator)

    def prepare_params(self, params):
        for key in params.keys():
            if key == "lag":
                params[key] = int(params[key])
            else:
                params[key] = float(str(params[key]).replace(",", "."))
        return params
    
    def calc(self):
        dataframe = self.cdataframe
        for indicator in self.indicators:
            dataframe = indicator(dataframe)
        return dataframe

    def calc_inside_dataframe(self, formulas_dict, timeframe):
        if not self.is_valid(formulas_dict):
            raise Exception("Params not valid")
        dataframe = begin_build_bars(self.cdataframe.get(), timeframe)
        for formula in formulas_dict:
            formula_name = formula['formula']
            formula_params = self.prepare_params(formula["params"])
            if not self.check_formula_is_avaliable(formula_name):
                print("{} not avaliable".format(formula_name))
            exec_formula = getattr(sys.modules[__name__], formula_name)
            dataframe = exec_formula(dataframe=dataframe, 
                **self.cleanup_kwargs_from_a_function(exec_formula, formula_params))

        dataframe = returns_op(dataframe, lag=0)
        dataframe = end_build_bars(dataframe)
        return CDataFrame(dataframe)

    def is_valid(self, formulas_dict):
        validate_types = all([
            isinstance(self.cdataframe, CDataFrame),
            type(formulas_dict) == list,
        ])

        if not validate_types:
            return validate_types

        validate_content = any([
                all([
                    len(formulas_dict)>0, 
                    type(formulas_dict[0])==dict
                ]),
                len(formulas_dict)==0,
            ])
        return validate_content



