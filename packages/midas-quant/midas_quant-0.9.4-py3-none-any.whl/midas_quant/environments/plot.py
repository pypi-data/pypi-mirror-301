from danbi.extends import bibokeh as bibo
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, CDSView, BooleanFilter, BoxAnnotation, Span, Range1d, LinearAxis
from bokeh.models import HoverTool,WheelZoomTool, PanTool, ResetTool, CrosshairTool, BoxSelectTool, BoxZoomTool, SaveTool

tools = [PanTool(), WheelZoomTool(), ResetTool(), CrosshairTool(), BoxSelectTool(), BoxZoomTool(), SaveTool()]


def plotCandle(data, width: int = 1200, height: int = 350, **options):
    cds = ColumnDataSource(data)
    tooltips = [
        ("date", "@reg_day{%F}"),
        ("price", "@close{,}")
    ]
    fig = bibo.getFigure(width, height, "Candle")
    
    # Candle
    inc = (cds.data["open"] <= cds.data["close"]).tolist()
    dec = (cds.data["close"] < cds.data["open"]).tolist()
    view_inc = CDSView(filter=BooleanFilter(inc))
    view_dec = CDSView(filter=BooleanFilter(dec))
    width = 12 * 60 * 60 * 1200
    fig.segment(x0="reg_day", x1="reg_day", y0="low", y1="high", color="#38812F", line_color="#23511E", source=cds, view=view_inc, legend_label="candle", alpha=0.6, muted_alpha=0)
    fig.segment(x0="reg_day", x1="reg_day", y0="low", y1="high", color="#8A8D90", line_color="#6A6E73", source=cds, view=view_dec, legend_label="candle", alpha=0.6, muted_alpha=0)
    fig.vbar(x="reg_day", width=width, top="open", bottom="close", fill_color="#7CC674", line_color="#38812F", source=cds, view=view_inc, legend_label="candle", alpha=0.6, muted_alpha=0)
    fig.vbar(x="reg_day", width=width, top="open", bottom="close", fill_color="#D2D2D2", line_color="#8A8D90", source=cds, view=view_dec, legend_label="candle", alpha=0.6, muted_alpha=0)
    tooltips.append(("close", "@close{,}"))
    
    # Moving Average
    base_line = fig.line(x="reg_day", y="ma5", source=cds, line_width=1.3, color="#F4C145", alpha=0.8, legend_label="price flow", muted_alpha=0)
    if "ma10" in cds.data:
        fig.line(x="reg_day", y="ma10", source=cds, line_width=1.5, color="#5752D1", alpha=0.6, legend_label = "ma10", muted_alpha=0)
    if "ma20" in cds.data:
        fig.line(x="reg_day", y="ma20", source=cds, line_width=1.6, color="#C46100", alpha=0.7, legend_label = "ma20", muted_alpha=0)
    if "ma60" in cds.data:
        fig.line(x="reg_day", y="ma60", source=cds, line_width=1.7, color="#005F60", alpha=0.8, legend_label = "ma60", muted_alpha=0)
        
    fig.line(x="reg_day", y="average_price", source=cds, line_width=2, color="black", alpha=1, legend_label="average_price", muted_alpha=0)

    fig.scatter(x="reg_day", y="buy_price", source=cds, size=8, marker="triangle", color="red", alpha=0.5)
    fig.scatter(x="reg_day", y="sell_price", source=cds, size=8, marker="inverted_triangle", color="blue", alpha=0.5)
    
    # Setup Figure Style
    formatters={"@reg_day": "datetime"}
    bibo.setFigureStyle(fig, tooltips, formatters, base_line)
    
    return fig


def plotAccount(data, width: int = 1200, height: int = 350, code="test", name="test", **options):
    cds = ColumnDataSource(data)
    tooltips = [
        ("date", "@reg_day{%F}"),
        ("account", "@account{,}"),
        ("quantity", "@quantity{,}")
    ]

    fig = bibo.getFigure(width, height, f"Account & Quantity [{name}, {code}]")
    
    # account axis
    fig.y_range = Range1d(start=min(cds.data['account']), end=max(cds.data['account']))
    base_line = fig.line(x="reg_day", y="account", source=cds, line_width=1.5, color="#C46100", alpha=0.8, legend_label="account", muted_alpha=0)

    # quantity axis
    fig.extra_y_ranges = {"right_y": Range1d(start=min(cds.data['quantity']), end=max(cds.data['quantity'])*3)}
    fig.add_layout(LinearAxis(y_range_name="right_y", axis_label="quantity"), 'right')
    fig.line(x="reg_day", y="quantity", source=cds, line_width=1, color="gray", y_range_name="right_y", legend_label="quantity")
    
    # Setup Figure Style
    formatters={"@reg_day": "datetime"}
    bibo.setFigureStyle(fig, tooltips, formatters, base_line)
    
    return fig


def showGraph(code, name, asset, data, col_daytime, plots: dict = {}, width: int = 1200, extra_height = 130):
    extra_plots = []
    for name in plots:
        extra_plots.append(bibo.plotTimeseries(data, col_daytime, plots[name], extra_height, hlines=[0], title=name))
    
    bibo.showAsRows([
        plotAccount(asset, height=130, code=code, name=name),
        plotCandle(data, height=350),
    ] + extra_plots, "x", width)


