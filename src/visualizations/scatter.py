"""
Scatter plot visualization for sample astronomical data.

This module generates interactive Bokeh scatter plots with sample
temperature vs magnitude data for demonstration purposes.
"""

import random
from bokeh.plotting import figure
from bokeh.embed import components


def get_sample_data():
    """
    Generate ~20 random astronomical data points.
    
    Returns:
        List of dictionaries with 'temperature' and 'magnitude' keys.
    """
    return [
        {"temperature": random.uniform(3000, 10000), 
         "magnitude": random.uniform(0, 10)}
        for _ in range(20)
    ]


def create_scatter_plot():
    """
    Create an interactive Bokeh scatter plot.
    
    Returns:
        Tuple of (script, div) components for embedding in HTML.
    """
    # Get sample data
    data = get_sample_data()
    temperatures = [point["temperature"] for point in data]
    magnitudes = [point["magnitude"] for point in data]
    
    # Create figure
    p = figure(
        width=800,
        height=400,
        title="Temperature vs Magnitude",
        x_axis_label="Temperature",
        y_axis_label="Magnitude",
        tools="hover,pan,box_zoom,wheel_zoom,reset,save"
    )
    
    # Add scatter points
    p.scatter(
        temperatures,
        magnitudes,
        size=10,
        alpha=0.6,
        color="#6366f1",
        marker="circle"
    )
    
    # Configure hover tooltips
    p.hover.tooltips = [
        ("Temperature", "@{x}"),
        ("Magnitude", "@{y}")
    ]
    
    # Style the plot
    p.background_fill_color = "#f5f5f7"
    p.border_fill_color = "white"
    
    # Export as embeddable components
    script, div = components(p)
    
    return {"script": script, "div": div}

