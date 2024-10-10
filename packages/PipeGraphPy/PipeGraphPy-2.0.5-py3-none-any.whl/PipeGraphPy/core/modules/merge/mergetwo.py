"""
作者: 郑水清
"""

import pandas as pd
from PipeGraphPy.constants import DATATYPE


class MergeTwo():
    INPUT = [DATATYPE.DATAFRAME, DATATYPE.DATAFRAME]
    OUTPUT = [DATATYPE.DATAFRAME]
    TEMPLATE = [
        {
            "key": "left_on",
            "name": "left_on",
            "type": "string",
            "plugin": "input",
            "need": False,
            "value": "",
            "desc": "字段说明",
        },
        {
            "key": "right_on",
            "name": "right_on",
            "type": "string",
            "plugin": "input",
            "need": False,
            "value": "",
            "desc": "字段说明",
        },
        {
            "key": "how",
            "name": "how",
            "type": "string",
            "plugin": "select",
            "need": False,
            "value": "inner",
            "source": ["inner", "left", "right", "outer"],
            "desc": "字段说明",
        },
        {
            "key": "extadd",
            "name": "附加参数",
            "type": "string",
            "plugin": "input",
            "need": False,
            "value": "{}",
            "desc": "字段说明",
        },
    ]
    params_rules = {
    }
    def __init__(self, **kw):
        self.left_on = kw.get("left_on") or ""
        self.right_on = kw.get("right_on") or ""
        self.how = kw.get("how") or "inner"
        self.extadd = kw.get("extadd") or {}

    def merge_datas(self, df1, df2):
        """合并数据
        """
        merge_params = {"how": self.how}
        if self.left_on:
            merge_params["left_on"] = self.left_on
        else:
            merge_params["left_index"] = True
        if self.right_on:
            merge_params["right_on"] = self.right_on
        else:
            merge_params["right_index"] = True
        if self.extadd and isinstance(self.extadd, dict):
            merge_params.update(self.extadd)
        return pd.merge(df1, df2, **merge_params)

    def run(self, df1, df2):
        """运行时处理合并
        """
        return self.merge_datas(df1, df2)

    def predict(self, df1, df2):
        """预测时处理合并
        """
        return self.merge_datas(df1, df2)
