import time
import math
from lightningchart import (
    LightningChart, LegendBoxBuilders, AxisScrollStrategies, 
    SolidFill, ColorRGBA, SolidLine, ColorHEX, ColorPalettes,
    UIElementBuilders, UIOrigins, FontSettings, AutoCursorModes
)

# Create a LightningChart instance
chart = LightningChart()

# Add a ChartXY
chart_xy = chart.add_chart_xy()

# Style the chart
chart_xy.set_title("Advanced Real-time Dashboard")
chart_xy.set_background_fill(SolidFill(ColorRGBA(30, 30, 30)))
chart_xy.get_default_axis_x().set_title("Time (s)")
chart_xy.get_default_axis_y().set_title("Value")

# Configure X-axis to scroll
chart_xy.get_default_axis_x().set_scroll_strategy(AxisScrollStrategies.progressive)

# Add multiple line series
line_series1 = chart_xy.add_line_series()
line_series1.set_name("Sine Wave")
line_series1.set_stroke(SolidLine(ColorPalettes.arction(0), 2))

line_series2 = chart_xy.add_line_series()
line_series2.set_name("Cosine Wave")
line_series2.set_stroke(SolidLine(ColorPalettes.arction(1), 2))

# Add a legend box
legend = chart_xy.add_legend_box(LegendBoxBuilders.horizontal_legend_box)
legend.add(line_series1)
legend.add(line_series2)

# Add a UI element for displaying current values
value_display = chart_xy.add_ui_element(
    UIElementBuilders.text_box_builder
    .set_text("Current Values")
    .set_origin(UIOrigins.right_top)
    .set_margin(5)
    .set_font_settings(FontSettings.from_font_size(14))
)

# Enable AutoCursor
chart_xy.set_auto_cursor(AutoCursorModes.x)

# Function to generate data
def generate_data():
    t = 0
    while True:
        y1 = math.sin(t * 0.1) * 5 + 5
        y2 = math.cos(t * 0.1) * 5 + 5
        yield t, y1, y2
        t += 0.1
        time.sleep(0.01)

# Main loop to update the chart
data_generator = generate_data()
for x, y1, y2 in data_generator:
    line_series1.add_point(x, y1)
    line_series2.add_point(x, y2)
    
    # Keep only the last 1000 points
    if x > 100:
        chart_xy.get_default_axis_x().set_interval(x - 100, x)
    
    # Update the value display
    value_display.set_text(f"Sine: {y1:.2f}\nCosine: {y2:.2f}")
    
    # Update the chart
    chart.render()
