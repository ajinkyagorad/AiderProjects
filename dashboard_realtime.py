from lightningchart import (
    LightningChart, ChartXY, Chart3D, LegendBoxBuilders, AxisScrollStrategies,
    SolidLine, ColorPalettes, UIElementBuilders, UIOrigins, FontSettings, AutoCursorModes,
    Dashboard
)
import time
import math
import random

def create_dashboard():
    # Create a Dashboard instance
    dashboard = Dashboard(
        {
            "title": "Advanced Multi-Chart Dashboard",
            "theme": "darkGreen"
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
        chart.get_default_axis_x().set_scroll_strategy(AxisScrollStrategies.progressive)

    # Add line series to each 2D chart
    line_series1 = chart_xy1.add_line_series()
    line_series1.set_name("Sine Wave")
    line_series1.set_stroke(SolidLine(ColorPalettes.arction(0), 2))

    line_series2 = chart_xy2.add_line_series()
    line_series2.set_name("Cosine Wave")
    line_series2.set_stroke(SolidLine(ColorPalettes.arction(1), 2))

    # Add point series to 3D chart
    point_series = chart_3d.add_point_series()
    point_series.set_point_size(5)

    # Add legend boxes
    for chart, series in [(chart_xy1, line_series1), (chart_xy2, line_series2)]:
        legend = chart.add_legend_box(LegendBoxBuilders.horizontal_legend_box)
        legend.add(series)

    # Add UI elements for displaying current values
    value_display1 = chart_xy1.add_ui_element(
        UIElementBuilders.text_box
        .set_text("Current Sine Value")
        .set_origin(UIOrigins.right_top)
        .set_margin({ 'top': 5, 'right': 5 })
        .set_font_size(14)
    )

    value_display2 = chart_xy2.add_ui_element(
        UIElementBuilders.text_box
        .set_text("Current Cosine Value")
        .set_origin(UIOrigins.right_top)
        .set_margin({ 'top': 5, 'right': 5 })
        .set_font_size(14)
    )

    # Enable AutoCursor for both 2D charts
    chart_xy1.set_auto_cursor(AutoCursorModes.x)
    chart_xy2.set_auto_cursor(AutoCursorModes.x)

    return chart, line_series1, line_series2, point_series, value_display1, value_display2

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
    chart, line_series1, line_series2, point_series, value_display1, value_display2 = create_dashboard()
    data_generator = generate_data()

    # Main loop to update the charts
    for t, y1, y2, x3, y3, z3 in data_generator:
        line_series1.add_point({ 'x': t, 'y': y1 })
        line_series2.add_point({ 'x': t, 'y': y2 })
        point_series.add_point({ 'x': x3, 'y': y3, 'z': z3 })
        
        # Keep only the last 100 points for 2D charts
        if t > 100:
            chart.get_default_axis_x().set_interval(t - 100, t)
        
        # Keep only the last 1000 points for 3D chart
        if point_series.get_point_count() > 1000:
            point_series.clear()
        
        # Update the value displays
        value_display1.set_text(f"Sine: {y1:.2f}")
        value_display2.set_text(f"Cosine: {y2:.2f}")

if __name__ == "__main__":
    main()
