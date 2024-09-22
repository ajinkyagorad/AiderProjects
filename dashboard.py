import time
from lightningchart import (
    LightningChart, LegendBoxBuilders, AxisScrollStrategies, 
    SolidFill, ColorRGBA, SolidLine, ColorHEX
)

# Create a LightningChart instance
chart = LightningChart()

# Add a ChartXY
chart_xy = chart.add_chart_xy()

# Style the chart
chart_xy.set_title("Real-time Hello World Dashboard")

# Configure X-axis to scroll
chart_xy.get_default_axis_x().set_scroll_strategy(AxisScrollStrategies.progressive)

# Add a line series
line_series = chart_xy.add_line_series()
line_series.set_name("Hello World Data")

# Style the line series
line_series.set_stroke(SolidLine(ColorHEX("#4287f5"), 2))

# Add a legend box
chart_xy.add_legend_box().add(line_series)

# Function to generate data
def generate_data():
    t = 0
    while True:
        y = (t % 10) + 1  # Simple oscillating pattern
        yield t, y
        t += 1
        time.sleep(0.1)

# Main loop to update the chart
data_generator = generate_data()
for x, y in data_generator:
    line_series.add_point(x, y)
    
    # Keep only the last 100 points
    if x > 100:
        chart_xy.get_default_axis_x().set_interval(x - 100, x)
    
    # Update the chart
    chart.render()
