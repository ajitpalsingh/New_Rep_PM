import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud
import datetime

def create_gantt_chart(wbs_data):
    """
    Create a Gantt chart for WBS tasks using Plotly.
    
    Args:
        wbs_data: List of WBS task dictionaries
        
    Returns:
        Plotly figure object
    """
    # Calculate the duration of tasks in days
    tasks = []
    for task in wbs_data:
        start_date = datetime.datetime.strptime(task["start_date"], "%Y-%m-%d")
        end_date = datetime.datetime.strptime(task["end_date"], "%Y-%m-%d")
        
        # Task color based on progress
        if task["progress"] == 100:
            color = '#4CAF50'  # Green for completed tasks
        elif task["progress"] >= 75:
            color = '#8BC34A'  # Light green for almost completed tasks
        elif task["progress"] >= 50:
            color = '#FFEB3B'  # Yellow for half completed tasks
        elif task["progress"] >= 25:
            color = '#FFC107'  # Orange for started tasks
        else:
            color = '#F44336'  # Red for not started tasks
        
        tasks.append({
            "Task": task["task"],
            "Start": start_date,
            "Finish": end_date,
            "Progress": task["progress"],
            "Assigned To": task["assigned_to"],
            "Color": color,
            "Critical": task["critical"]
        })
    
    df = pd.DataFrame(tasks)
    
    # Sort by start date
    df = df.sort_values(by="Start")
    
    # Create Gantt chart
    fig = px.timeline(
        df, 
        x_start="Start", 
        x_end="Finish", 
        y="Task",
        color="Progress",
        color_continuous_scale=[(0, "red"), (0.25, "orange"), (0.5, "yellow"), (0.75, "lightgreen"), (1, "green")],
        hover_data=["Assigned To", "Progress"]
    )
    
    # Add critical path indicator
    for i, task in enumerate(df.itertuples()):
        if task.Critical:
            fig.add_shape(
                type="rect",
                x0=task.Start,
                x1=task.Finish,
                y0=i-0.4,
                y1=i+0.4,
                line=dict(color="black", width=2),
                opacity=0.1
            )
    
    # Customize layout
    fig.update_layout(
        title="Project Gantt Chart",
        xaxis_title="Timeline",
        yaxis_title="Tasks",
        height=600,
        xaxis=dict(
            type='date',
            tickformat='%d %b %Y',
            rangeslider_visible=True
        ),
        coloraxis_colorbar=dict(
            title="Progress %",
        )
    )
    
    # Add Today marker
    today = datetime.datetime.now()
    fig.add_vline(x=today, line_width=2, line_dash="dash", line_color="black")
    fig.add_annotation(
        x=today,
        y=1.05,
        text="Today",
        showarrow=False,
        xref="x",
        yref="paper"
    )
    
    return fig

def create_resource_allocation_chart(resource_data):
    """
    Create a resource allocation chart using Plotly.
    
    Args:
        resource_data: List of resource dictionaries
        
    Returns:
        Plotly figure object
    """
    # Prepare data
    resources = []
    for resource in resource_data:
        resources.append({
            "Name": resource["name"],
            "Role": resource["role"],
            "Availability": resource["availability"],
            "Allocated": resource["allocated"],
            "Utilization": resource["allocated"] / resource["availability"] * 100
        })
    
    df = pd.DataFrame(resources)
    
    # Sort by utilization (highest first)
    df = df.sort_values(by="Utilization", ascending=False)
    
    # Create horizontal bar chart
    fig = go.Figure()
    
    # Add allocated bar
    fig.add_trace(go.Bar(
        y=df["Name"],
        x=df["Allocated"],
        name="Allocated",
        orientation='h',
        marker=dict(color='#2196F3')
    ))
    
    # Add availability bar
    fig.add_trace(go.Bar(
        y=df["Name"],
        x=df["Availability"],
        name="Availability",
        orientation='h',
        marker=dict(color='rgba(204, 204, 204, 0.5)')
    ))
    
    # Add utilization percentage as text
    for i, row in enumerate(df.itertuples()):
        # Color based on utilization
        if row.Utilization > 100:
            color = "red"  # Over-allocated
        elif row.Utilization > 90:
            color = "orange"  # Near capacity
        else:
            color = "green"  # Good allocation
            
        fig.add_annotation(
            x=row.Allocated + 5,
            y=i,
            text=f"{row.Utilization:.0f}%",
            showarrow=False,
            font=dict(color=color, size=12),
            xanchor="left"
        )
    
    # Customize layout
    fig.update_layout(
        title="Resource Allocation",
        xaxis_title="Hours",
        yaxis_title="Resource",
        barmode='overlay',
        height=max(400, len(df) * 40),  # Adjust height based on number of resources
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_raid_compliance_chart(raid_data):
    """
    Create RAID compliance visualization using Plotly.
    
    Args:
        raid_data: Dictionary of RAID data
        
    Returns:
        Plotly figure object
    """
    # Calculate compliance metrics
    metrics = {
        "Risks": len([r for r in raid_data["risks"] if r["mitigation"] and r["owner"]]) / max(1, len(raid_data["risks"])) * 100,
        "Assumptions": len([a for a in raid_data["assumptions"] if a["validation_method"]]) / max(1, len(raid_data["assumptions"])) * 100,
        "Issues": len([i for i in raid_data["issues"] if i["owner"] and i["status"] != "Open"]) / max(1, len(raid_data["issues"])) * 100,
        "Dependencies": len([d for d in raid_data["dependencies"] if d["status"] != "At Risk"]) / max(1, len(raid_data["dependencies"])) * 100
    }
    
    # Create radar chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=[metrics["Risks"], metrics["Assumptions"], metrics["Issues"], metrics["Dependencies"]],
        theta=["Risks", "Assumptions", "Issues", "Dependencies"],
        fill='toself',
        name='Compliance',
        marker_color='rgba(54, 162, 235, 0.7)'
    ))
    
    # Add reference circle at 75% compliance (minimum target)
    fig.add_trace(go.Scatterpolar(
        r=[75, 75, 75, 75],
        theta=["Risks", "Assumptions", "Issues", "Dependencies"],
        fill='toself',
        name='Target (75%)',
        marker_color='rgba(255, 99, 132, 0.2)'
    ))
    
    # Customize layout
    fig.update_layout(
        title="RAID Management Compliance",
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True
    )
    
    return fig

def create_decision_status_chart(decisions):
    """
    Create a decision status visualization using Plotly.
    
    Args:
        decisions: List of decision dictionaries
        
    Returns:
        Plotly figure object
    """
    # Count decisions by status
    status_counts = {}
    for decision in decisions:
        status = decision["status"]
        if status in status_counts:
            status_counts[status] += 1
        else:
            status_counts[status] = 1
    
    # Define color mapping
    color_map = {
        "Approved": "#4CAF50",
        "Pending": "#FFC107",
        "Rejected": "#F44336",
        "Under Review": "#2196F3",
        "Deferred": "#9E9E9E"
    }
    
    # Prepare data for pie chart
    labels = list(status_counts.keys())
    values = list(status_counts.values())
    colors = [color_map.get(status, "#9C27B0") for status in labels]
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        textinfo='value+percent',
        hole=0.4,
    )])
    
    # Customize layout
    fig.update_layout(
        title="Decision Status Distribution",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig

def create_sentiment_gauge(sentiment_score):
    """
    Create a sentiment gauge chart using Plotly.
    
    Args:
        sentiment_score: Sentiment score between -1 and 1
        
    Returns:
        Plotly figure object
    """
    # Map sentiment score from -1:1 to 0:100 for gauge
    gauge_value = (sentiment_score + 1) / 2 * 100
    
    # Define color stops for the gauge
    color_stops = [
        [0, "#F44336"],      # Red (Negative)
        [0.25, "#FFC107"],   # Yellow-Orange (Somewhat Negative)
        [0.5, "#FFEB3B"],    # Yellow (Neutral)
        [0.75, "#8BC34A"],   # Light Green (Somewhat Positive)
        [1, "#4CAF50"]       # Green (Positive)
    ]
    
    # Create gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=gauge_value,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "Team Sentiment"},
        delta={"reference": 50, "increasing": {"color": "#4CAF50"}, "decreasing": {"color": "#F44336"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "darkblue"},
            "bar": {"color": "darkblue"},
            "bgcolor": "white",
            "borderwidth": 2,
            "bordercolor": "gray",
            "steps": [
                {"range": [0, 25], "color": "rgba(244, 67, 54, 0.5)"},
                {"range": [25, 50], "color": "rgba(255, 193, 7, 0.5)"},
                {"range": [50, 75], "color": "rgba(139, 195, 74, 0.5)"},
                {"range": [75, 100], "color": "rgba(76, 175, 80, 0.5)"}
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": 50
            }
        }
    ))
    
    # Customize layout
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

def create_wordcloud(feedback_text):
    """
    Create a wordcloud from feedback text.
    
    Args:
        feedback_text: List of feedback text entries
        
    Returns:
        Matplotlib figure
    """
    # Combine all feedback text
    if isinstance(feedback_text, list):
        text = " ".join([fb.get("content", "") if isinstance(fb, dict) else fb for fb in feedback_text])
    else:
        text = feedback_text
    
    # Generate wordcloud
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color="white", 
        max_words=100, 
        contour_width=3, 
        contour_color="steelblue",
        colormap="viridis"
    ).generate(text)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    plt.tight_layout()
    
    return fig

def create_critical_path_network(wbs_data):
    """
    Create a network diagram of the critical path using NetworkX and Matplotlib.
    
    Args:
        wbs_data: List of WBS task dictionaries
        
    Returns:
        Matplotlib figure
    """
    # Create directed graph
    G = nx.DiGraph()
    
    # Add nodes and edges
    for task in wbs_data:
        # Node attributes to store task info
        G.add_node(
            task["id"],
            label=f"{task['id']}. {task['task']}",
            critical=task["critical"],
            progress=task["progress"]
        )
        
        # Add edges for dependencies
        for dep in task["dependencies"]:
            G.add_edge(dep, task["id"])
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Position nodes using a hierarchical layout algorithm
    pos = nx.spring_layout(G, seed=42)  # Use spring layout instead of graphviz-dependent layouts
    
    # Prepare node colors based on critical path and progress
    node_colors = []
    for node in G.nodes():
        if G.nodes[node]["critical"]:
            # Shade of red based on progress (darker = higher progress)
            progress = G.nodes[node]["progress"] / 100
            node_colors.append((1.0, 0.4 * (1 - progress), 0.4 * (1 - progress)))
        else:
            # Shade of blue based on progress (darker = higher progress)
            progress = G.nodes[node]["progress"] / 100
            node_colors.append((0.4 * (1 - progress), 0.4 * (1 - progress), 1.0))
    
    # Draw nodes and edges
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800, alpha=0.8)
    nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.7, edge_color='gray', arrows=True, arrowsize=15)
    
    # Draw node labels
    nx.draw_networkx_labels(G, pos, labels=nx.get_node_attributes(G, 'label'), font_size=10)
    
    # Add legend
    critical_patch = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Critical Path')
    normal_patch = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Normal Task')
    ax.legend(handles=[critical_patch, normal_patch], loc='upper right')
    
    # Add title and remove axis
    plt.title("Project Critical Path Network")
    plt.axis('off')
    plt.tight_layout()
    
    return fig

def create_scope_creep_chart(baseline_wbs, current_wbs):
    """
    Create a visualization comparing baseline WBS to current WBS to show scope creep.
    
    Args:
        baseline_wbs: Original WBS tasks
        current_wbs: Current WBS tasks
        
    Returns:
        Plotly figure object
    """
    # Calculate scope changes
    baseline_ids = set(task["id"] for task in baseline_wbs)
    current_ids = set(task["id"] for task in current_wbs)
    
    added_tasks = current_ids - baseline_ids
    removed_tasks = baseline_ids - current_ids
    common_tasks = baseline_ids.intersection(current_ids)
    
    # Get the tasks that have changed (same ID but different duration or description)
    modified_tasks = []
    for task_id in common_tasks:
        baseline_task = next(task for task in baseline_wbs if task["id"] == task_id)
        current_task = next(task for task in current_wbs if task["id"] == task_id)
        
        if (baseline_task["duration"] != current_task["duration"] or
            baseline_task["description"] != current_task["description"]):
            modified_tasks.append(task_id)
    
    # Prepare data for visualization
    categories = ["Added", "Modified", "Removed", "Unchanged"]
    values = [
        len(added_tasks),
        len(modified_tasks),
        len(removed_tasks),
        len(common_tasks) - len(modified_tasks)
    ]
    
    colors = ["#4CAF50", "#FFC107", "#F44336", "#2196F3"]
    
    # Create bar chart
    fig = go.Figure()
    
    # Add bars
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color=colors,
        text=values,
        textposition='auto'
    ))
    
    # Customize layout
    fig.update_layout(
        title="Scope Change Analysis",
        xaxis_title="Task Status",
        yaxis_title="Number of Tasks",
        height=400
    )
    
    # Add a second visualization for task duration comparison
    baseline_duration = sum(task["duration"] for task in baseline_wbs)
    current_duration = sum(task["duration"] for task in current_wbs)
    
    # Create a second plot if there's a difference in total duration
    if baseline_duration != current_duration:
        duration_change = ((current_duration - baseline_duration) / baseline_duration) * 100
        
        # Add an annotation about duration change
        fig.add_annotation(
            x=1.5,
            y=max(values) * 0.8,
            text=f"Total Duration Change: {duration_change:.1f}%",
            showarrow=False,
            font=dict(size=14, color="red" if duration_change > 0 else "green")
        )
    
    return fig