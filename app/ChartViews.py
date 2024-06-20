from pyecharts.charts import Pie
from pyecharts.options import LabelOpts, TitleOpts, AxisOpts, LegendOpts, InitOpts
import pyecharts.options as opts


p = (
    Pie().add(
        series_name="完成占比",
        data_pair=[["截止已完成", 1], ["截止未完成", 0.1]],
        radius="35%",
        center=["50%", "50%"],
    ).set_global_opts(
        title_opts=TitleOpts(
            # title="get_sum_chart",
            pos_left="center",
            pos_top="50"
        ),
        legend_opts=opts.LegendOpts(pos_top="30%", pos_left="80%", orient="vertical"),
    )
)

p.set_series_opts(
    label_opts=opts.LabelOpts(is_show=False)
)


p.render("get_sum_chart.html")