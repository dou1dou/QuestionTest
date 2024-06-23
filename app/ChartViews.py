from pyecharts.charts import Pie
from pyecharts.options import TitleOpts
import pyecharts.options as opts
from pyecharts.charts import Radar
from pyecharts.charts import Bar


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

v1 = [[0.1, 0.26, 0.95]]

(
    Radar(init_opts=opts.InitOpts(width="1280px", height="720px", bg_color="#ffffff"))
    .add_schema(
        schema=[
            opts.RadarIndicatorItem(name="java", max_=1),
            opts.RadarIndicatorItem(name="python", max_=1),
            opts.RadarIndicatorItem(name="c", max_=1)
        ],
        splitarea_opt=opts.SplitAreaOpts(
            is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
        ),
        textstyle_opts=opts.TextStyleOpts(color="#999999"),
    )
    .add(
        series_name="做题正确率",
        data=v1,
        linestyle_opts=opts.LineStyleOpts(color="#CD0000"),
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .render("basic_radar_chart.html")
)

l1 = ['java', 'python', 'c']
l2 = [20, 30, 50]
bar = (
    Bar()
    .add_xaxis(l1)
    .add_yaxis("l2", l2)
    .reversal_axis()
    .set_series_opts(label_opts=opts.LabelOpts(position="right"))
)
bar.render_notebook()

bar.render("bar_chart.html")