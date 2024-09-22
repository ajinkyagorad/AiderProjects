# Note: This script requires the LightningChart library. Install it using:
# pip install lightningchart

from lightningchart import (
    ChartXY, AxisScrollStrategies, LineSeriesXY,
    ColorHEX, SolidLine, ColorRGBA, SolidFill, PointShape,
    UIElementBuilders, UIOrigins, FontSettings, Themes,
    UIBackgrounds, UILayoutBuilders
)
import time
import math
import random
import threading

class DashboardControl:
    def __init__(self):
        self.paused = False
        self.update_interval = 0.01

def create_dashboard():
    # Create a ChartXY instance
    chart_xy = ChartXY({"theme": Themes.dark})
    chart_xy.set_title("Real-time Multi-Series Dashboard")

    # Style the chart
    chart_xy.get_default_axis_x().set_title("Time (s)")
    chart_xy.get_default_axis_y().set_title("Value")
    chart_xy.get_default_axis_x().set_scroll_strategy(AxisScrollStrategies.progressive)

    # Add line series
    line_series1 = chart_xy.add_line_series()
    line_series1.set_name("Sine Wave")
    line_series1.set_stroke(SolidLine(ColorHEX("#FF1919"), 2))

    line_series2 = chart_xy.add_line_series()
    line_series2.set_name("Cosine Wave")
    line_series2.set_stroke(SolidLine(ColorHEX("#19FF19"), 2))

    line_series3 = chart_xy.add_line_series()
    line_series3.set_name("Random Walk")
    line_series3.set_stroke(SolidLine(ColorHEX("#1919FF"), 2))

    # Add UI elements for displaying current values
    value_display1 = chart_xy.add_ui_element(
        UIElementBuilders.text_box()
        .set_text("Current Sine Value")
        .set_position({ 'x': 90, 'y': 20 })
        .set_font_size(14)
    )

    value_display2 = chart_xy.add_ui_element(
        UIElementBuilders.text_box()
        .set_text("Current Cosine Value")
        .set_position({ 'x': 90, 'y': 40 })
        .set_font_size(14)
    )

    value_display3 = chart_xy.add_ui_element(
        UIElementBuilders.text_box()
        .set_text("Current Random Value")
        .set_position({ 'x': 90, 'y': 60 })
        .set_font_size(14)
    )

    # Add control panel
    control_panel = chart_xy.add_ui_element(
        UILayoutBuilders.row()
        .set_background(UIBackgrounds.rectangle())
        .set_position({ 'x': 10, 'y': 10 })
    )

    pause_button = control_panel.add_element(UIElementBuilders.button().set_text("Pause"))
    speed_slider = control_panel.add_element(UIElementBuilders.slider()
        .set_range(1, 100)
        .set_value(100)
        .set_size({ 'x': 100, 'y': 20 })
    )

    return chart_xy, line_series1, line_series2, line_series3, value_display1, value_display2, value_display3, pause_button, speed_slider

def generate_data(control):
    """Generate sine, cosine, and random walk data points."""
    t = 0
    random_value = 5
    while True:
        y1 = math.sin(t * 0.1) * 5 + 5
        y2 = math.cos(t * 0.1) * 5 + 5
        random_value += random.uniform(-0.5, 0.5)
        random_value = max(0, min(10, random_value))  # Keep between 0 and 10
        yield t, y1, y2, random_value
        t += 0.1
        time.sleep(0.01)

def main():
    chart_xy, line_series1, line_series2, line_series3, value_display1, value_display2, value_display3, pause_button, speed_slider = create_dashboard()
    control = DashboardControl()
    data_generator = generate_data(control)

    def update_chart():
        for t, y1, y2, y3 in data_generator:
            if control.paused:
                time.sleep(0.1)
                continue

            line_series1.add_point({ 'x': t, 'y': y1 })
            line_series2.add_point({ 'x': t, 'y': y2 })
            line_series3.add_point({ 'x': t, 'y': y3 })
            
            if t > 1000:
                chart_xy.get_default_axis_x().set_interval(t - 1000, t)
            
            value_display1.set_text(f"Sine: {y1:.2f}")
            value_display2.set_text(f"Cosine: {y2:.2f}")
            value_display3.set_text(f"Random: {y3:.2f}")

            chart_xy.render()
            time.sleep(control.update_interval)

    update_thread = threading.Thread(target=update_chart)
    update_thread.start()

    def toggle_pause():
        control.paused = not control.paused
        pause_button.set_text("Resume" if control.paused else "Pause")

    def update_speed(value):
        control.update_interval = 1 / value

    pause_button.on_click(toggle_pause)
    speed_slider.on_value_changed(update_speed)

    chart_xy.render()

if __name__ == "__main__":
    main()
