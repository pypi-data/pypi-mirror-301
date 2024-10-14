"""
作者: 郑水清
算法说明：把多个df数据合并到一个df数据上
使用说明：kw参数配置 {"left_on":["", "time"], "right_on":["", "time"], "how": "inner"}
          left_on: string 或 list 原始数据使用merge的列, 非必传,默认使用index, 传值为空代表使用index,
                   string 代表使用同一列 list 表示使用不同的列
          right_on: string 或 list 需要合并的数据使用merge的列, 非必传,默认使用index, 传值为空代表使用index,
                   string 代表使用同一列 list 表示使用不同的列
          how: string 合并方式["inner", "outer", "left", "right"] 非必传, 默认为inner
注意事项:
    1.参数可以不传，默认使用index作merge.
    2.如果left_on或right_on为list,请确保长度和要合并的DataFrame列表长度一致
    3.如果在merge时找不到对应的列,会出现Null值情况，本算法不会自动去掉Nul值.
    4.如果要合并的数据有和原数据有相同的列，会直接替换掉原有列
"""

import pandas as pd


class MergeMany():
    def __init__(self, **kw):
        self.params = kw
        self.how = self.params.get("how") or "inner"

    def check_params(self, length: int):
        """校验传参
        """
        for param in ['left_on', 'right_on']:
            if (
                self.params.get(param) and
                isinstance(self.params[param], list) and
                len(self.params[param]) != length
            ):
                raise Exception(
                        "%s算法参数%s长度不正确" % (
                            self.__class__.__name__, param
                            ))
        if self.how not in ["inner", "outer", "left", "right"]:
            raise Exception(
                        "%s算法how参数取值不正确" % self.__class__.__name__
                    )

    def replace(self, df1, df2):
        """替换相同字段的列
        """
        right_on = self.params.get("right_on") or ""
        right_on = right_on if isinstance(right_on, list) else [right_on]
        drop_columns = []
        for c in df2.columns:
            if c in df1.columns and c not in right_on:
                df1[c] = df2[c]
                drop_columns.append(c)
        df2.drop(columns=drop_columns, inplace=True)
        return df1, df2

    def merge(self, df1, df2, idx):
        """合并两个Dataframe
        """
        merge_params = {"how": self.how}
        for param in ['left_on', 'right_on']:
            on_field = self.params.get(param) or ""
            on_field = on_field[idx] if isinstance(on_field, list) else on_field
            if on_field:
                merge_params[param] = on_field
            else:
                index = param.replace("on", "index")
                merge_params[index] = True
        return pd.merge(df1, df2, **merge_params)

    def merge_datas(self, df, df_lst):
        """合并数据
        """
        for idx, item in enumerate(df_lst):
            df, item = self.replace(df, item)
            df = self.merge(df, item, idx)
        return df

    def run(self, df, df_lst):
        """运行时处理合并
        params
            df: Dataframe 要合并的原始数据
            df_lst: list(Dataframe) 需要合并的数据
        return
            合并处理后的数据
        """
        self.check_params(len(df_lst))
        return self.merge_datas(df, df_lst)

    def predict(self, df, df_lst):
        """预测时处理合并
        params
            df: Dataframe 要合并的原始数据
            df_lst: list(Dataframe) 需要合并的数据
        return
            合并处理后的数据
        """
        return self.merge_datas(df, df_lst)
