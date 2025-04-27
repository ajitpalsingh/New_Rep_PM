import streamlit as st
import os
import sys
import datetime
import json

# Add the project root to the path so we can import modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import modules (use relative imports)
try:
    from utils.data_utils import load_sample_data, save_data
except ImportError:
    # Also try to import from local directory (for cloud deployment)
    from utils.data_utils import load_sample_data, save_data

# Set page config
st.set_page_config(
    page_title="AI PM Buddy v2.0",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main .block-container {padding-top: 1rem;}
    .stTabs [data-baseweb="tab-list"] {gap: 2px;}
    .stTabs [data-baseweb="tab"] {
        height: 50px; 
        white-space: pre-wrap;
        background-color: #f0f0f0;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4CAF50 !important;
        color: white !important;
    }
    div[data-testid="stSidebarNav"] li div a {
        margin-left: 1rem;
        padding: 1rem;
        width: 300px;
        border-radius: 0.5rem;
    }
    div[data-testid="stSidebarNav"] li div::focus-visible {
        background-color: rgba(151, 166, 195, 0.15);
    }
    div[data-testid="stMarkdownContainer"] h1 {margin-bottom: 0rem;}
    div[data-testid="stMarkdownContainer"] h2 {margin-bottom: 0rem;}
    
    /* Card-like containers */
    .card {
        border-radius: 8px;
        padding: 20px;
        background-color: #ffffff;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    /* Info panels */
    .info-panel {
        background-color: #e8f4fd;
        border-left: 4px solid #2196F3;
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 0px 4px 4px 0px;
    }
    
    /* Status colors */
    .status-on-track {color: #4CAF50;}
    .status-at-risk {color: #FF9800;}
    .status-delayed {color: #F44336;}
    .status-completed {color: #2196F3;}
    
    /* Custom metrics */
    .metric-container {
        display: inline-block;
        text-align: center;
        margin: 10px;
        min-width: 120px;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

def show_dashboard():
    """Display the main dashboard with project overview."""
    
    # Load sample data if not in session state
    if 'project_data' not in st.session_state:
        st.session_state.project_data = load_sample_data()
        save_data(st.session_state.project_data)
    
    project_data = st.session_state.project_data
    current_project = project_data["selected_project"]
    project = project_data["projects"][current_project]
    
    st.title(f"📊 AI PM Buddy v2.0")
    
    # Project selection and details
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        selected_project = st.selectbox(
            "Project",
            options=list(project_data["projects"].keys()),
            index=list(project_data["projects"].keys()).index(current_project)
        )
        if selected_project != current_project:
            project_data["selected_project"] = selected_project
            save_data(project_data)
            # Force a rerun to update the UI
            st.rerun()
    
    # Project status and metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="metric-container">
                <p class="metric-value">{project['progress']}%</p>
                <p class="metric-label">Progress</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Days remaining
        today = datetime.datetime.now().date()
        end_date = datetime.datetime.strptime(project['end_date'], "%Y-%m-%d").date()
        days_remaining = (end_date - today).days
        
        status_color = "status-on-track"
        if days_remaining < 0:
            status_color = "status-delayed"
        elif days_remaining < 14:
            status_color = "status-at-risk"
            
        st.markdown(f"""
            <div class="metric-container">
                <p class="metric-value {status_color}">{days_remaining}</p>
                <p class="metric-label">Days Remaining</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        # Calculate tasks completed
        total_tasks = len(project['wbs'])
        completed_tasks = len([t for t in project['wbs'] if t['progress'] == 100])
        
        st.markdown(f"""
            <div class="metric-container">
                <p class="metric-value">{completed_tasks}/{total_tasks}</p>
                <p class="metric-label">Tasks Completed</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        # Calculate risks
        high_risks = len([r for r in project['raid']['risks'] if r['severity'] == 'High'])
        
        risk_color = "status-on-track"
        if high_risks > 3:
            risk_color = "status-delayed"
        elif high_risks > 1:
            risk_color = "status-at-risk"
            
        st.markdown(f"""
            <div class="metric-container">
                <p class="metric-value {risk_color}">{high_risks}</p>
                <p class="metric-label">High Risks</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Dashboard tabs
    tabs = st.tabs(["Overview", "Key Milestones", "Resource Status", "AI Insight Summary"])
    
    with tabs[0]:  # Overview
        col1, col2 = st.columns([2, 1])
        with col1:
            # Project health indicators
            st.subheader("Project Health")
            health_col1, health_col2, health_col3, health_col4 = st.columns(4)
            
            with health_col1:
                schedule_status = "On Track"
                schedule_color = "status-on-track"
                if days_remaining < 0:
                    schedule_status = "Delayed"
                    schedule_color = "status-delayed"
                elif project['progress'] < 50 and project['elapsed_pct'] > 60:
                    schedule_status = "At Risk"
                    schedule_color = "status-at-risk"
                
                st.markdown(f"""
                <div class="card">
                    <h4>Schedule</h4>
                    <h2 class="{schedule_color}">{schedule_status}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with health_col2:
                budget_status = "On Track"
                budget_color = "status-on-track"
                if project['budget_spent_pct'] > project['progress'] + 15:
                    budget_status = "Over Budget"
                    budget_color = "status-delayed"
                elif project['budget_spent_pct'] > project['progress'] + 5:
                    budget_status = "At Risk"
                    budget_color = "status-at-risk"
                
                st.markdown(f"""
                <div class="card">
                    <h4>Budget</h4>
                    <h2 class="{budget_color}">{budget_status}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with health_col3:
                scope_status = "On Track"
                scope_color = "status-on-track"
                if len(project.get('scope_changes', [])) > 5:
                    scope_status = "Significant Changes"
                    scope_color = "status-delayed"
                elif len(project.get('scope_changes', [])) > 2:
                    scope_status = "Minor Changes"
                    scope_color = "status-at-risk"
                
                st.markdown(f"""
                <div class="card">
                    <h4>Scope</h4>
                    <h2 class="{scope_color}">{scope_status}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with health_col4:
                quality_status = "High"
                quality_color = "status-on-track"
                if len(project.get('defects', [])) > 10:
                    quality_status = "Low"
                    quality_color = "status-delayed"
                elif len(project.get('defects', [])) > 5:
                    quality_status = "Medium"
                    quality_color = "status-at-risk"
                
                st.markdown(f"""
                <div class="card">
                    <h4>Quality</h4>
                    <h2 class="{quality_color}">{quality_status}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            # Recent activities
            st.subheader("Recent Activities")
            if 'activities' in project:
                for activity in project['activities'][:5]:  # Show latest 5 activities
                    st.markdown(f"""
                    <div class="info-panel">
                        <strong>{activity['date']}</strong> - {activity['description']}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No recent activities recorded.")
        
        with col2:
            # Key risks
            st.subheader("Top Risks")
            if 'raid' in project and 'risks' in project['raid']:
                high_risks = [r for r in project['raid']['risks'] if r['severity'] == 'High']
                if high_risks:
                    for risk in high_risks[:3]:  # Show top 3 high risks
                        st.markdown(f"""
                        <div class="card">
                            <h4>{risk['title']}</h4>
                            <p><strong>Impact:</strong> {risk['impact']}</p>
                            <p><strong>Mitigation:</strong> {risk['mitigation'] if risk['mitigation'] else "Not defined"}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No high risks identified.")
            else:
                st.info("No risks defined.")
                
            # OpenAI API Check
            st.subheader("OpenAI API Status")
            openai_key = os.environ.get("OPENAI_API_KEY", "")
            if openai_key:
                st.markdown(f"""
                <div class="card">
                    <h4 class="status-on-track">✅ OpenAI API Configured</h4>
                    <p>AI features are available</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="card">
                    <h4 class="status-delayed">❌ OpenAI API Not Configured</h4>
                    <p>Add your OpenAI API key in the Settings tab to enable AI features</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tabs[1]:  # Key Milestones
        st.subheader("Project Milestones")
        
        # Extract milestones from WBS
        milestones = [task for task in project['wbs'] if task.get('milestone', False)]
        
        if milestones:
            # Create a table
            milestone_data = []
            for ms in milestones:
                status_class = ""
                if ms['progress'] == 100:
                    status = "Completed"
                    status_class = "status-completed"
                else:
                    # Calculate if milestone is delayed
                    end_date = datetime.datetime.strptime(ms['end_date'], "%Y-%m-%d").date()
                    if end_date < today and ms['progress'] < 100:
                        status = "Delayed"
                        status_class = "status-delayed"
                    elif (end_date - today).days <= 7 and ms['progress'] < 100:
                        status = "At Risk"
                        status_class = "status-at-risk"
                    else:
                        status = "On Track"
                        status_class = "status-on-track"
                
                milestone_data.append({
                    "Name": ms['task'],
                    "Due Date": ms['end_date'],
                    "Owner": ms['assigned_to'],
                    "Progress": f"{ms['progress']}%",
                    "Status": f'<span class="{status_class}">{status}</span>'
                })
            
            # Create the table with custom formatting
            milestone_html = '<table style="width:100%">'
            milestone_html += '<tr><th>Name</th><th>Due Date</th><th>Owner</th><th>Progress</th><th>Status</th></tr>'
            
            for ms in milestone_data:
                milestone_html += f'<tr>'
                milestone_html += f'<td>{ms["Name"]}</td>'
                milestone_html += f'<td>{ms["Due Date"]}</td>'
                milestone_html += f'<td>{ms["Owner"]}</td>'
                milestone_html += f'<td>{ms["Progress"]}</td>'
                milestone_html += f'<td>{ms["Status"]}</td>'
                milestone_html += f'</tr>'
            
            milestone_html += '</table>'
            
            st.markdown(milestone_html, unsafe_allow_html=True)
        else:
            st.info("No milestones defined in the project.")
    
    with tabs[2]:  # Resource Status
        st.subheader("Team Resources")
        
        team_resources = project.get('resources', [])
        if team_resources:
            # Create columns for resource cards
            cols = st.columns(3)
            
            for i, resource in enumerate(team_resources):
                utilization = resource['allocated'] / resource['availability'] * 100
                
                # Determine utilization status
                util_status = "status-on-track"
                if utilization > 100:
                    util_status = "status-delayed"
                elif utilization > 90:
                    util_status = "status-at-risk"
                
                # Create a card for each resource
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class="card">
                        <h3>{resource['name']}</h3>
                        <p><strong>Role:</strong> {resource['role']}</p>
                        <p><strong>Utilization:</strong> <span class="{util_status}">{utilization:.0f}%</span></p>
                        <div style="background-color: #f0f0f0; height: 10px; border-radius: 5px; margin-top: 10px;">
                            <div style="background-color: {'#F44336' if utilization > 100 else '#4CAF50'}; width: {min(100, utilization)}%; height: 10px; border-radius: 5px;"></div>
                        </div>
                        <p><strong>Allocated:</strong> {resource['allocated']} hrs / <strong>Available:</strong> {resource['availability']} hrs</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No resource information available.")
    
    with tabs[3]:  # AI Insight Summary
        st.subheader("AI Project Insights")
        
        # Check if OpenAI API is configured
        openai_key = os.environ.get("OPENAI_API_KEY", "")
        if not openai_key:
            st.warning("OpenAI API key not configured. Please add your API key to use AI insights.")
            st.markdown("""
            To configure the OpenAI API key:
            1. Create an account at [OpenAI](https://platform.openai.com)
            2. Generate an API key
            3. Add it to your environment variables or .env file
            """)
        else:
            # Placeholder for AI insights
            st.markdown("""
            <div class="info-panel">
                <h4>Schedule Risk Analysis</h4>
                <p>Based on current progress and resource allocation, there's a moderate risk of schedule slippage in the Implementation phase. Consider reviewing task assignments for team members with high utilization.</p>
            </div>
            
            <div class="info-panel">
                <h4>Budget Forecast</h4>
                <p>Current spending rate suggests the project may exceed budget by approximately 8% if current trends continue. Early cost-control measures are recommended.</p>
            </div>
            
            <div class="info-panel">
                <h4>Risk Pattern Detection</h4>
                <p>Several technical risks related to integration components have been identified. A technical review session with the architecture team is recommended.</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("AI Analysis Details"):
                st.markdown("""
                **Performance Metrics:**
                - Schedule Performance Index (SPI): 0.92
                - Cost Performance Index (CPI): 0.94
                - Estimate at Completion (EAC): 108% of budget
                
                **Critical Path Analysis:**
                - 3 tasks on the critical path are currently delayed
                - Bottleneck identified in the "System Integration" phase
                
                **Resource Management:**
                - 2 team members are over-allocated
                - QA resources are under-allocated for upcoming testing phase
                """)

def show_ai_assistant():
    """Display the AI Personal Assistant module."""
    st.title("📱 AI Personal Assistant")
    
    # Check if OpenAI API is configured
    openai_key = os.environ.get("OPENAI_API_KEY", "")
    if not openai_key:
        st.warning("OpenAI API key not configured. Please add your API key to use this feature.")
        st.markdown("""
        To configure the OpenAI API key:
        1. Create an account at [OpenAI](https://platform.openai.com)
        2. Generate an API key
        3. Add it to your environment variables or .env file
        """)
        return
    
    # Load sample data if not in session state
    if 'project_data' not in st.session_state:
        st.session_state.project_data = load_sample_data()
        save_data(st.session_state.project_data)
    
    if 'assistant_messages' not in st.session_state:
        st.session_state.assistant_messages = [
            {"role": "assistant", "content": "Hello! I'm your AI PM Assistant. What can I help you with today? You can ask me about project management concepts, request analysis on your current project, or get help drafting project documents."}
        ]
    
    # Display chat messages
    for message in st.session_state.assistant_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # User input
    user_input = st.chat_input("Ask your PM assistant...")
    
    if user_input:
        # Add user message to chat history
        st.session_state.assistant_messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # For demo purposes, provide canned responses
        # In a real implementation, this would make a call to OpenAI
        with st.chat_message("assistant"):
            if "risk" in user_input.lower():
                response = """
                # Risk Analysis
                
                Based on your project data, I've identified these key risks:
                
                1. **Schedule Risk**: Current progress (65%) is trailing behind elapsed time (70%)
                2. **Resource Constraint**: Team member "Alex Chen" is currently over-allocated (110%)
                3. **Technical Risk**: Integration with legacy systems has unresolved dependencies
                
                **Recommendations**:
                - Consider adjusting timeline for the implementation phase
                - Redistribute tasks from over-allocated resources
                - Schedule a technical review session for integration components
                """
            elif "status report" in user_input.lower() or "report" in user_input.lower():
                response = """
                # Project Status Report
                
                **Period**: April 15-27, 2023
                
                ## Summary
                Project is currently at 65% completion with moderate schedule risk. Budget spending is on track at 62%.
                
                ## Key Achievements
                - Completed user authentication module
                - Finalized database schema design
                - Conducted first round of user acceptance testing
                
                ## Issues & Risks
                - Integration with payment gateway experiencing delays
                - Resource constraint in QA team
                
                ## Next Steps
                - Complete payment gateway integration
                - Begin final testing phase
                - Prepare deployment documentation
                """
            elif "milestone" in user_input.lower():
                response = """
                # Milestone Status
                
                | Milestone | Due Date | Status | Days Remaining |
                |-----------|----------|--------|---------------|
                | Requirements Sign-off | 2023-01-15 | Completed | - |
                | Design Approval | 2023-02-28 | Completed | - |
                | Alpha Release | 2023-04-15 | Completed | - |
                | Beta Release | 2023-05-30 | At Risk | 33 |
                | Final Delivery | 2023-07-15 | On Track | 79 |
                
                **Note**: Beta Release milestone is at risk due to delays in the payment integration module. Consider allocating additional resources or adjusting the timeline.
                """
            elif "budget" in user_input.lower():
                response = """
                # Budget Analysis
                
                Current budget status:
                - Total budget: $450,000
                - Spent to date: $279,000 (62%)
                - Remaining: $171,000 (38%)
                
                Forecast analysis shows current spending rate might lead to a 5% budget overrun by project completion. Cost control measures recommended for the testing and deployment phases.
                
                **Cost Distribution**:
                - Development: 45%
                - Testing: 20%
                - Project Management: 15%
                - Infrastructure: 12%
                - Training & Documentation: 8%
                """
            else:
                response = """
                I understand you're asking about project management insights. Based on the current project data, here are some observations:
                
                1. The project is progressing at an acceptable rate with 65% completion
                2. There are some resource allocation concerns that may need attention
                3. Several high-priority risks have been identified that should be addressed
                
                What specific aspect of the project would you like me to analyze in more detail? For example, I can provide insights on schedule, budget, risks, resource allocation, or help draft project documents.
                """
            
            st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.assistant_messages.append({"role": "assistant", "content": response})

def render_sidebar():
    """Render the enhanced sidebar with improved navigation."""
    
    st.sidebar.image("https://i.imgur.com/1YIKFIQ.png", width=280)
    
    st.sidebar.markdown("## Navigation")
    
    # Main Navigation
    selected = st.sidebar.radio(
        "Main Menu",
        options=["Dashboard", "AI Assistant"],
        index=0,
        key="main_navigation",
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    # OpenAI API Key input
    st.sidebar.markdown("## Settings")
    
    openai_key = os.environ.get("OPENAI_API_KEY", "")
    if openai_key:
        st.sidebar.success("OpenAI API Key is configured")
    else:
        st.sidebar.warning("OpenAI API Key is not set")
        api_key = st.sidebar.text_input("Enter OpenAI API Key:", type="password")
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            st.sidebar.success("API Key set for this session!")
            st.sidebar.button("Reload App", on_click=lambda: st.rerun())
    
    st.sidebar.markdown("---")
    
    # About section
    with st.sidebar.expander("About AI PM Buddy"):
        st.markdown("""
        **AI PM Buddy v2.0** is an AI-powered Project Management Assistant.
        
        Key features:
        - Interactive project dashboard
        - AI insights and analysis
        - Resource management
        - Risk assessment
        - Smart document generation
        
        Built with Streamlit and OpenAI.
        """)
    
    return selected

def main():
    """Main application function."""
    
    # Render sidebar and get selected navigation
    selected = render_sidebar()
    
    # Display the appropriate page based on selection
    if selected == "Dashboard":
        show_dashboard()
    elif selected == "AI Assistant":
        show_ai_assistant()

if __name__ == '__main__':
    main()