import time
import math
from lightningchart import (
    LightningChart, LegendBoxBuilders, AxisScrollStrategies, 
    SolidFill, ColorRGBA, SolidLine, ColorPalettes,
    UIElementBuilders, UIOrigins, FontSettings, AutoCursorModes,
    Dashboard, Themes
)

def create_dashboard():
    # Create a Dashboard instance
    dashboard = Dashboard(
        {
            "title": "Advanced Multi-Chart Dashboard",
            "theme": Themes.dark
        }
    )

    # Add multiple ChartXY to the dashboard
    chart_xy1 = dashboard.create_chart_xy()
    chart_xy2 = dashboard.create_chart_xy()

    # Style the charts
    chart_xy1.set_title("Sine Wave")
    chart_xy2.set_title("Cosine Wave")

    for chart in [chart_xy1, chart_xy2]:
        chart.get_default_axis_x().set_title("Time (s)")
        chart.get_default_axis_y().set_title("Value")
        chart.get_default_axis_x().set_scroll_strategy(AxisScrollStrategies.progressive)

    # Add line series to each chart
    line_series1 = chart_xy1.add_line_series()
    line_series1.set_name("Sine Wave")
    line_series1.set_stroke(SolidLine(ColorPalettes.arction(0), 2))

    line_series2 = chart_xy2.add_line_series()
    line_series2.set_name("Cosine Wave")
    line_series2.set_stroke(SolidLine(ColorPalettes.arction(1), 2))

    # Add legend boxes
    for chart, series in [(chart_xy1, line_series1), (chart_xy2, line_series2)]:
        legend = chart.add_legend_box(LegendBoxBuilders.horizontal_legend_box)
        legend.add(series)

    # Add UI elements for displaying current values
    value_display1 = chart_xy1.add_ui_element(
        UIElementBuilders.text_box_builder
        .set_text("Current Sine Value")
        .set_origin(UIOrigins.right_top)
        .set_margin(5)
        .set_font_settings(FontSettings.from_font_size(14))
    )

    value_display2 = chart_xy2.add_ui_element(
        UIElementBuilders.text_box_builder
        .set_text("Current Cosine Value")
        .set_origin(UIOrigins.right_top)
        .set_margin(5)
        .set_font_settings(FontSettings.from_font_size(14))
    )

    # Enable AutoCursor for both charts
    chart_xy1.set_auto_cursor(AutoCursorModes.x)
    chart_xy2.set_auto_cursor(AutoCursorModes.x)

    return dashboard, line_series1, line_series2, value_display1, value_display2

def generate_data():
    """Generate sine and cosine data points."""
    t = 0
    while True:
        y1 = math.sin(t * 0.1) * 5 + 5
        y2 = math.cos(t * 0.1) * 5 + 5
        yield t, y1, y2
        t += 0.1
        time.sleep(0.01)

def main():
    dashboard, line_series1, line_series2, value_display1, value_display2 = create_dashboard()
    data_generator = generate_data()

    # Main loop to update the charts
    for x, y1, y2 in data_generator:
        line_series1.add_point(x, y1)
        line_series2.add_point(x, y2)
        
        # Keep only the last 100 points
        if x > 100:
            dashboard.get_charts()[0].get_default_axis_x().set_interval(x - 100, x)
            dashboard.get_charts()[1].get_default_axis_x().set_interval(x - 100, x)
        
        # Update the value displays
        value_display1.set_text(f"Sine: {y1:.2f}")
        value_display2.set_text(f"Cosine: {y2:.2f}")
        
        # Update the dashboard
        dashboard.render()

if __name__ == "__main__":
    main()
