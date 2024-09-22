import lightningchart as lc
import time
import math
import random

def create_dashboard():
    # Create a Dashboard instance
    dashboard = lc.Dashboard(
        {
            "title": "Real-time Multi-Chart Dashboard",
            "theme": lc.Themes.dark
        }
    )

    # Add multiple ChartXY to the dashboard
    chart_xy1 = dashboard.create_chart_xy()
    chart_xy2 = dashboard.create_chart_xy()
    chart_3d = dashboard.create_chart_3d()

    # Style the charts
    chart_xy1.set_title("Sine Wave")
    chart_xy2.set_title("Cosine Wave")
    chart_3d.set_title("3D Random Points")

    for chart in [chart_xy1, chart_xy2]:
        chart.get_default_axis_x().set_title("Time (s)")
        chart.get_default_axis_y().set_title("Value")
        chart.get_default_axis_x().set_scroll_strategy(lc.AxisScrollStrategies.progressive)

    # Add line series to each 2D chart
    line_series1 = chart_xy1.add_line_series()
    line_series1.set_name("Sine Wave")
    line_series1.set_stroke(lc.SolidLine(lc.ColorPalettes.arction(0), 2))

    line_series2 = chart_xy2.add_line_series()
    line_series2.set_name("Cosine Wave")
    line_series2.set_stroke(lc.SolidLine(lc.ColorPalettes.arction(1), 2))

    # Add point series to 3D chart
    point_series = chart_3d.add_point_series()
    point_series.set_point_size(5)

    # Add legend boxes
    for chart, series in [(chart_xy1, line_series1), (chart_xy2, line_series2)]:
        legend = chart.add_legend_box(lc.LegendBoxBuilders.horizontal_legend_box)
        legend.add(series)

    # Add UI elements for displaying current values
    value_display1 = chart_xy1.add_ui_element(
        lc.UIElementBuilders.text_box_builder
        .set_text("Current Sine Value")
        .set_origin(lc.UIOrigins.right_top)
        .set_margin(5)
        .set_font_settings(lc.FontSettings.from_font_size(14))
    )

    value_display2 = chart_xy2.add_ui_element(
        lc.UIElementBuilders.text_box_builder
        .set_text("Current Cosine Value")
        .set_origin(lc.UIOrigins.right_top)
        .set_margin(5)
        .set_font_settings(lc.FontSettings.from_font_size(14))
    )

    # Enable AutoCursor for both 2D charts
    chart_xy1.set_auto_cursor(lc.AutoCursorModes.x)
    chart_xy2.set_auto_cursor(lc.AutoCursorModes.x)

    return dashboard, line_series1, line_series2, point_series, value_display1, value_display2

def generate_data():
    """Generate sine, cosine, and 3D random data points."""
    t = 0
    while True:
        y1 = math.sin(t * 0.1) * 5 + 5
        y2 = math.cos(t * 0.1) * 5 + 5
        x3 = random.uniform(0, 10)
        y3 = random.uniform(0, 10)
        z3 = random.uniform(0, 10)
        yield t, y1, y2, x3, y3, z3
        t += 0.1
        time.sleep(0.01)

def main():
    dashboard, line_series1, line_series2, point_series, value_display1, value_display2 = create_dashboard()
    data_generator = generate_data()

    # Main loop to update the charts
    for t, y1, y2, x3, y3, z3 in data_generator:
        line_series1.add_point(t, y1)
        line_series2.add_point(t, y2)
        point_series.add_point(x3, y3, z3)
        
        # Keep only the last 100 points for 2D charts
        if t > 100:
            dashboard.get_charts()[0].get_default_axis_x().set_interval(t - 100, t)
            dashboard.get_charts()[1].get_default_axis_x().set_interval(t - 100, t)
        
        # Keep only the last 1000 points for 3D chart
        if point_series.get_point_count() > 1000:
            point_series.clear()
        
        # Update the value displays
        value_display1.set_text(f"Sine: {y1:.2f}")
        value_display2.set_text(f"Cosine: {y2:.2f}")
        
        # Update the dashboard
        dashboard.render()

if __name__ == "__main__":
    main()
