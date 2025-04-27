import streamlit as st
import pandas as pd
import datetime
import os
import json

def load_sample_data():
    """
    Create a sample project data structure.
    Returns:
        dict: Sample project data
    """
    # Check if sample data exists in session state
    if 'project_data' in st.session_state:
        return st.session_state.project_data
    
    # Get current date for relative date calculations
    today = datetime.datetime.now().date()
    
    # Create sample data structure
    project_data = {
        "selected_project": "Sample Project",
        "projects": {
            "Sample Project": generate_sample_project_1(today),
            "Enterprise Software Implementation": generate_sample_project_2(today)
        }
    }
    
    return project_data

def generate_sample_project_1(today):
    """
    Generate the first sample project data (Generic IT Project).
    
    Args:
        today: Current date
        
    Returns:
        dict: Sample project data
    """
    # Calculate various dates relative to today
    project_start = today - datetime.timedelta(days=60)
    project_end = today + datetime.timedelta(days=90)
    
    # Calculate elapsed percentage
    total_days = (project_end - project_start).days
    elapsed_days = (today - project_start).days
    elapsed_pct = min(100, max(0, round(elapsed_days / total_days * 100)))
    
    # Sample WBS (Work Breakdown Structure)
    wbs = [
        {
            "id": "1",
            "task": "Project Initiation",
            "description": "Define project scope, objectives, and stakeholders",
            "start_date": (project_start).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=15)).strftime("%Y-%m-%d"),
            "duration": 15,
            "progress": 100,
            "assigned_to": "John Smith",
            "dependencies": [],
            "critical": True,
            "milestone": True
        },
        {
            "id": "2",
            "task": "Requirements Gathering",
            "description": "Collect and document business and technical requirements",
            "start_date": (project_start + datetime.timedelta(days=10)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=30)).strftime("%Y-%m-%d"),
            "duration": 20,
            "progress": 100,
            "assigned_to": "Emily Johnson",
            "dependencies": ["1"],
            "critical": True,
            "milestone": False
        },
        {
            "id": "3",
            "task": "System Design",
            "description": "Create technical architecture and detailed design documents",
            "start_date": (project_start + datetime.timedelta(days=25)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=45)).strftime("%Y-%m-%d"),
            "duration": 20,
            "progress": 90,
            "assigned_to": "Michael Chen",
            "dependencies": ["2"],
            "critical": True,
            "milestone": False
        },
        {
            "id": "4",
            "task": "Design Review",
            "description": "Review and approve system design",
            "start_date": (project_start + datetime.timedelta(days=45)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=50)).strftime("%Y-%m-%d"),
            "duration": 5,
            "progress": 80,
            "assigned_to": "Sarah Williams",
            "dependencies": ["3"],
            "critical": True,
            "milestone": True
        },
        {
            "id": "5",
            "task": "Development - Phase 1",
            "description": "Implement core functionality",
            "start_date": (project_start + datetime.timedelta(days=50)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=80)).strftime("%Y-%m-%d"),
            "duration": 30,
            "progress": 65,
            "assigned_to": "Alex Chen",
            "dependencies": ["4"],
            "critical": True,
            "milestone": False
        },
        {
            "id": "6",
            "task": "Development - Phase 2",
            "description": "Implement secondary features",
            "start_date": (project_start + datetime.timedelta(days=65)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=95)).strftime("%Y-%m-%d"),
            "duration": 30,
            "progress": 40,
            "assigned_to": "Ryan Lee",
            "dependencies": ["4"],
            "critical": False,
            "milestone": False
        },
        {
            "id": "7",
            "task": "Testing - Unit Tests",
            "description": "Perform unit testing on components",
            "start_date": (project_start + datetime.timedelta(days=75)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=85)).strftime("%Y-%m-%d"),
            "duration": 10,
            "progress": 30,
            "assigned_to": "Jessica Taylor",
            "dependencies": ["5"],
            "critical": True,
            "milestone": False
        },
        {
            "id": "8",
            "task": "Testing - Integration Tests",
            "description": "Perform integration testing",
            "start_date": (project_start + datetime.timedelta(days=85)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=100)).strftime("%Y-%m-%d"),
            "duration": 15,
            "progress": 0,
            "assigned_to": "Jessica Taylor",
            "dependencies": ["5", "6", "7"],
            "critical": True,
            "milestone": False
        },
        {
            "id": "9",
            "task": "User Acceptance Testing",
            "description": "Conduct user acceptance testing",
            "start_date": (project_start + datetime.timedelta(days=100)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=115)).strftime("%Y-%m-%d"),
            "duration": 15,
            "progress": 0,
            "assigned_to": "Emily Johnson",
            "dependencies": ["8"],
            "critical": True,
            "milestone": False
        },
        {
            "id": "10",
            "task": "Deployment",
            "description": "Deploy the system to production",
            "start_date": (project_start + datetime.timedelta(days=115)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=125)).strftime("%Y-%m-%d"),
            "duration": 10,
            "progress": 0,
            "assigned_to": "Michael Chen",
            "dependencies": ["9"],
            "critical": True,
            "milestone": False
        },
        {
            "id": "11",
            "task": "Project Closure",
            "description": "Complete project documentation and handover",
            "start_date": (project_start + datetime.timedelta(days=125)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=135)).strftime("%Y-%m-%d"),
            "duration": 10,
            "progress": 0,
            "assigned_to": "John Smith",
            "dependencies": ["10"],
            "critical": True,
            "milestone": True
        }
    ]
    
    # Calculate overall project progress
    total_duration = sum(task["duration"] for task in wbs)
    weighted_progress = sum(task["duration"] * task["progress"] for task in wbs) / total_duration
    
    # Sample resources
    resources = [
        {
            "name": "John Smith",
            "role": "Project Manager",
            "availability": 160,
            "allocated": 120,
            "skills": ["Project Management", "Stakeholder Management", "Risk Management"]
        },
        {
            "name": "Emily Johnson",
            "role": "Business Analyst",
            "availability": 160,
            "allocated": 140,
            "skills": ["Requirements Gathering", "Process Modeling", "User Stories"]
        },
        {
            "name": "Michael Chen",
            "role": "Solution Architect",
            "availability": 160,
            "allocated": 150,
            "skills": ["System Design", "Technical Leadership", "Integration"]
        },
        {
            "name": "Alex Chen",
            "role": "Lead Developer",
            "availability": 160,
            "allocated": 176,
            "skills": ["Java", "Python", "Database Design"]
        },
        {
            "name": "Ryan Lee",
            "role": "Developer",
            "availability": 160,
            "allocated": 160,
            "skills": ["JavaScript", "React", "Node.js"]
        },
        {
            "name": "Jessica Taylor",
            "role": "QA Engineer",
            "availability": 160,
            "allocated": 120,
            "skills": ["Test Planning", "Automated Testing", "Performance Testing"]
        },
        {
            "name": "Sarah Williams",
            "role": "Product Owner",
            "availability": 80,
            "allocated": 60,
            "skills": ["Product Vision", "User Experience", "Backlog Management"]
        }
    ]
    
    # Sample RAID (Risks, Assumptions, Issues, Dependencies)
    raid = {
        "risks": [
            {
                "id": "R1",
                "title": "Resource Shortage",
                "description": "Key team members may not be available for the entire project duration.",
                "probability": "Medium",
                "impact": "High",
                "severity": "High",
                "mitigation": "Cross-train team members and identify backup resources.",
                "owner": "John Smith",
                "status": "Open"
            },
            {
                "id": "R2",
                "title": "Technology Complexity",
                "description": "The selected technology stack may be more complex than initially estimated.",
                "probability": "Medium",
                "impact": "Medium",
                "severity": "Medium",
                "mitigation": "Conduct technical spike and early prototyping.",
                "owner": "Michael Chen",
                "status": "Open"
            },
            {
                "id": "R3",
                "title": "Scope Creep",
                "description": "Project scope may expand during development.",
                "probability": "High",
                "impact": "Medium",
                "severity": "High",
                "mitigation": "Implement strict change control process.",
                "owner": "John Smith",
                "status": "Open"
            },
            {
                "id": "R4",
                "title": "Integration Issues",
                "description": "Integration with legacy systems may be more difficult than expected.",
                "probability": "Medium",
                "impact": "High",
                "severity": "High",
                "mitigation": "Perform early integration testing and allocate additional time.",
                "owner": "",
                "status": "Open"
            }
        ],
        "assumptions": [
            {
                "id": "A1",
                "description": "The stakeholders will be available for regular reviews and feedback.",
                "validation_method": "Confirm availability in project kickoff.",
                "status": "Validated"
            },
            {
                "id": "A2",
                "description": "The existing infrastructure can support the new system.",
                "validation_method": "Perform infrastructure assessment.",
                "status": "Not Validated"
            },
            {
                "id": "A3",
                "description": "Users have basic technical skills to use the new system.",
                "validation_method": "Conduct user skills assessment.",
                "status": "Validated"
            }
        ],
        "issues": [
            {
                "id": "I1",
                "title": "Development Environment Setup Delay",
                "description": "Setting up development environments taking longer than expected.",
                "priority": "Medium",
                "raised_date": (today - datetime.timedelta(days=10)).strftime("%Y-%m-%d"),
                "owner": "Michael Chen",
                "status": "In Progress"
            },
            {
                "id": "I2",
                "title": "Requirements Documentation Gaps",
                "description": "Some requirements are not clearly documented.",
                "priority": "High",
                "raised_date": (today - datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
                "owner": "Emily Johnson",
                "status": "Open"
            }
        ],
        "dependencies": [
            {
                "id": "D1",
                "description": "Access to legacy system API documentation",
                "type": "External",
                "owner": "IT Operations",
                "due_date": (today - datetime.timedelta(days=15)).strftime("%Y-%m-%d"),
                "status": "Completed"
            },
            {
                "id": "D2",
                "description": "Security approval for cloud deployment",
                "type": "External",
                "owner": "Security Team",
                "due_date": (today + datetime.timedelta(days=10)).strftime("%Y-%m-%d"),
                "status": "At Risk"
            },
            {
                "id": "D3",
                "description": "User story prioritization for Phase 2",
                "type": "Internal",
                "owner": "Sarah Williams",
                "due_date": (today + datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
                "status": "On Track"
            }
        ]
    }
    
    # Sample team feedback
    team_feedback = [
        {
            "member": "Alex Chen",
            "date": (today - datetime.timedelta(days=7)).strftime("%Y-%m-%d"),
            "content": "We need more clarity on the API requirements. The documentation is incomplete and it's slowing down our development process."
        },
        {
            "member": "Jessica Taylor",
            "date": (today - datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
            "content": "The test environment is working well. We're making good progress on the automated test suite."
        },
        {
            "member": "Ryan Lee",
            "date": (today - datetime.timedelta(days=3)).strftime("%Y-%m-%d"),
            "content": "I'm concerned about the timeline for the user interface components. The designs keep changing and it's affecting our velocity."
        },
        {
            "member": "Emily Johnson",
            "date": (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
            "content": "Stakeholder feedback has been positive on the requirements. They're excited about the new features we're implementing."
        }
    ]
    
    # Sample decisions log
    decisions = [
        {
            "id": "D1",
            "title": "Technology Stack Selection",
            "description": "Decided to use React for frontend and Node.js for backend based on team expertise and project requirements.",
            "date": (project_start + datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
            "owner": "Michael Chen",
            "status": "Approved",
            "impact": "Defines the development approach and resource requirements."
        },
        {
            "id": "D2",
            "title": "Cloud Provider Selection",
            "description": "Selected AWS as the cloud provider for hosting the application.",
            "date": (project_start + datetime.timedelta(days=10)).strftime("%Y-%m-%d"),
            "owner": "John Smith",
            "status": "Approved",
            "impact": "Determines infrastructure costs and deployment strategy."
        },
        {
            "id": "D3",
            "title": "Authentication Method",
            "description": "Decided to implement OAuth 2.0 for authentication with support for social logins.",
            "date": (project_start + datetime.timedelta(days=30)).strftime("%Y-%m-%d"),
            "owner": "Alex Chen",
            "status": "Approved",
            "impact": "Affects user experience and security implementation."
        },
        {
            "id": "D4",
            "title": "Reporting Engine",
            "description": "Evaluating whether to build custom reporting or integrate with a third-party tool.",
            "date": (today - datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
            "owner": "Sarah Williams",
            "status": "Under Review",
            "impact": "Will impact development effort and timeline for reporting features."
        }
    ]
    
    # Sample activities log
    activities = [
        {
            "date": (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
            "description": "Daily standup: Team reported progress on user authentication module."
        },
        {
            "date": (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
            "description": "Risk review meeting: Added new risk related to third-party API integration."
        },
        {
            "date": (today - datetime.timedelta(days=2)).strftime("%Y-%m-%d"),
            "description": "Completed code review for data access layer components."
        },
        {
            "date": (today - datetime.timedelta(days=3)).strftime("%Y-%m-%d"),
            "description": "Client demo of UI prototype, received positive feedback."
        },
        {
            "date": (today - datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
            "description": "Updated project schedule based on current progress and resource availability."
        },
        {
            "date": (today - datetime.timedelta(days=7)).strftime("%Y-%m-%d"),
            "description": "Technical design review for reporting module."
        }
    ]
    
    # Sample scope changes
    scope_changes = [
        {
            "id": "SC1",
            "title": "Add Social Media Integration",
            "description": "Added requirement to integrate with social media platforms for content sharing.",
            "requested_by": "Marketing Team",
            "date": (project_start + datetime.timedelta(days=20)).strftime("%Y-%m-%d"),
            "status": "Approved",
            "impact": "Adds approximately 5 days to the development timeline."
        },
        {
            "id": "SC2",
            "title": "Enhanced Analytics Dashboard",
            "description": "Expanded the analytics features to include more detailed user behavior tracking.",
            "requested_by": "Product Owner",
            "date": (project_start + datetime.timedelta(days=35)).strftime("%Y-%m-%d"),
            "status": "Approved",
            "impact": "Increases development effort by approximately 15%."
        },
        {
            "id": "SC3",
            "title": "Mobile App Integration",
            "description": "Added API endpoints to support future mobile application.",
            "requested_by": "CTO",
            "date": (today - datetime.timedelta(days=10)).strftime("%Y-%m-%d"),
            "status": "Under Review",
            "impact": "May require additional resources and extend timeline."
        }
    ]
    
    # Create the complete project structure
    project = {
        "name": "Sample Project",
        "description": "Implementation of a new customer portal with enhanced user experience and reporting capabilities.",
        "start_date": project_start.strftime("%Y-%m-%d"),
        "end_date": project_end.strftime("%Y-%m-%d"),
        "budget": 500000,
        "budget_spent": 310000,
        "budget_spent_pct": 62,
        "progress": round(weighted_progress),
        "status": "On Track",
        "elapsed_pct": elapsed_pct,
        "wbs": wbs,
        "resources": resources,
        "raid": raid,
        "team_feedback": team_feedback,
        "decisions": decisions,
        "activities": activities,
        "scope_changes": scope_changes
    }
    
    return project

def save_data(project_data):
    """
    Save project data to session state.
    This function would typically save to a database, but for this app we'll use session state.
    
    Args:
        project_data: Dictionary of project data
    """
    st.session_state.project_data = project_data

def load_agile_knowledge():
    """
    Load Agile knowledge data from CSV or create if it doesn't exist.
    
    Returns:
        DataFrame: Agile knowledge data
    """
    # Check if we have it in session state first
    if 'agile_knowledge' in st.session_state:
        return st.session_state.agile_knowledge
    
    # Define sample agile knowledge
    data = {
        "question": [
            "What is Agile?",
            "What is Scrum?",
            "What is a Sprint?",
            "What is a Product Backlog?",
            "What is a Sprint Backlog?",
            "What is a Daily Standup?",
            "What is a Sprint Review?",
            "What is a Sprint Retrospective?",
            "What is a Product Owner?",
            "What is a Scrum Master?",
            "What is a Development Team?",
            "What is a User Story?",
            "What is Story Points?",
            "What is Velocity?",
            "What is Burndown Chart?",
            "What is Kanban?",
            "What is WIP Limit?",
            "What is Definition of Done?",
            "What is Definition of Ready?",
            "What is Technical Debt?"
        ],
        "answer": [
            "Agile is an iterative approach to project management and software development that helps teams deliver value to their customers faster and with fewer headaches. Instead of betting everything on a 'big bang' launch, an agile team delivers work in small, but consumable, increments.",
            "Scrum is a framework within which people can address complex adaptive problems, while productively and creatively delivering products of the highest possible value. Scrum is a lightweight framework that helps people, teams and organizations generate value through adaptive solutions for complex problems.",
            "A Sprint is a time-boxed period (typically 2-4 weeks) during which a specific set of work must be completed and made ready for review. Sprints are at the very heart of scrum and agile methodologies.",
            "The Product Backlog is an ordered list of everything that is known to be needed in the product. It is the single source of requirements for any changes to be made to the product. The Product Owner is responsible for the Product Backlog.",
            "The Sprint Backlog is the set of Product Backlog items selected for the Sprint, plus a plan for delivering the product Increment and realizing the Sprint Goal. The Sprint Backlog is a forecast by the Development Team about what functionality will be in the next Increment and the work needed to deliver that functionality.",
            "The Daily Standup (or Daily Scrum) is a 15-minute time-boxed event for the Development Team to synchronize activities and create a plan for the next 24 hours. It is held at the same time and place each day to reduce complexity.",
            "A Sprint Review is held at the end of the Sprint to inspect the Increment and adapt the Product Backlog if needed. During the Sprint Review, the Scrum Team and stakeholders collaborate about what was done in the Sprint.",
            "The Sprint Retrospective is an opportunity for the Scrum Team to inspect itself and create a plan for improvements to be enacted during the next Sprint. It occurs after the Sprint Review and prior to the next Sprint Planning.",
            "The Product Owner is responsible for maximizing the value of the product resulting from work of the Development Team. The Product Owner is the sole person responsible for managing the Product Backlog.",
            "The Scrum Master is responsible for promoting and supporting Scrum. Scrum Masters do this by helping everyone understand Scrum theory, practices, rules, and values. The Scrum Master is a servant-leader for the Scrum Team.",
            "The Development Team consists of professionals who do the work of delivering a potentially releasable Increment of 'Done' product at the end of each Sprint. Development Teams are structured and empowered by the organization to organize and manage their own work.",
            "A User Story is a small, self-contained unit of development work designed to accomplish a specific goal within a product. A user story is usually written from the end user's perspective and follows the format: 'As a [type of user], I want [some goal] so that [some reason].'",
            "Story Points are a unit of measure for expressing an estimate of the overall effort that will be required to fully implement a product backlog item or any other piece of work. Teams assign story points relative to work complexity, the amount of work, and risk or uncertainty.",
            "Velocity is a measure of the amount of work a Team can tackle during a single Sprint and is the key metric in Scrum. Velocity is calculated at the end of the Sprint by summing up the Story Points for all fully completed User Stories.",
            "A Burndown Chart is a graphical representation of work left to do versus time. The outstanding work (or backlog) is often on the vertical axis, with time along the horizontal. Burndown charts are a run chart of outstanding work.",
            "Kanban is a visual system for managing work as it moves through a process. Kanban visualizes both the process (the workflow) and the actual work passing through that process. The goal of Kanban is to identify potential bottlenecks in your process and fix them so work can flow through it cost-effectively at an optimal speed or throughput.",
            "WIP (Work In Progress) Limits are constraints on how many work items can be in progress at each stage of a workflow. By limiting WIP, teams can optimize flow, reduce context switching, identify bottlenecks, and improve delivery predictability.",
            "Definition of Done (DoD) is a shared understanding of what it means for work to be complete, and ensures everyone on the team knows exactly what is expected of everything the team delivers. It is a collection of valuable deliverables required to produce software.",
            "Definition of Ready (DoR) is a set of agreements that lets a team know when a user story is ready to be taken into a sprint. It helps the team identify whether they have enough information to be able to successfully implement the user story.",
            "Technical Debt describes what results when development teams take actions to expedite the delivery of a piece of functionality or a project which later needs to be refactored. In other words, it's the result of prioritizing speedy delivery over perfect code."
        ]
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Store in session state
    st.session_state.agile_knowledge = df
    
    return df

def load_pm_knowledge():
    """
    Load Project Management knowledge data from CSV or create if it doesn't exist.
    
    Returns:
        DataFrame: PM knowledge data
    """
    # Check if we have it in session state first
    if 'pm_knowledge' in st.session_state:
        return st.session_state.pm_knowledge
    
    # Define sample PM knowledge
    data = {
        "question": [
            "What is a Project Charter?",
            "What is a WBS?",
            "What is a Gantt Chart?",
            "What is a Critical Path?",
            "What is a RAID Log?",
            "What is a Stakeholder Analysis?",
            "What is Resource Leveling?",
            "What is Earned Value Management?",
            "What is CPI?",
            "What is SPI?",
            "What is a Milestone?",
            "What is a Risk Register?",
            "What is a Change Control Board?",
            "What is a Project Baseline?",
            "What is a Deliverable?",
            "What is a Project Management Plan?",
            "What is a RACI Matrix?",
            "What is a Lessons Learned Register?",
            "What is a Scope Statement?",
            "What is a Project Life Cycle?"
        ],
        "answer": [
            "A Project Charter is a formal, typically short document that describes the project in its entirety — including what the objectives are, how it will be carried out, and who the stakeholders are. It is the first step in the project planning process.",
            "A Work Breakdown Structure (WBS) is a hierarchical decomposition of the total scope of work to be carried out by the project team to accomplish the project objectives and create the required deliverables. It organizes and defines the total scope of the project.",
            "A Gantt Chart is a bar chart that illustrates a project schedule, showing the start and finish dates of the terminal elements and summary elements of a project. Terminal elements and summary elements constitute the work breakdown structure of the project.",
            "The Critical Path is the sequence of activities that represents the longest path through a project, which determines the shortest possible duration. It consists of the longest sequence of activities from project start to end.",
            "A RAID Log is a project management tool that helps track Risks, Assumptions, Issues, and Dependencies. It's used to document and monitor these items throughout the project lifecycle to ensure they are being managed effectively.",
            "Stakeholder Analysis is the process of identifying the individuals or groups that are likely to affect or be affected by a proposed action, and sorting them according to their impact on the action and the impact the action will have on them.",
            "Resource Leveling is a project management technique used to examine unbalanced use of resources (usually people or equipment) over time and resolve over-allocations or conflicts. It can be used to balance the workload of primary resources.",
            "Earned Value Management (EVM) is a project management technique that objectively tracks physical accomplishment of work. It integrates scope, schedule, and cost, allowing project managers to track variances from the plan.",
            "Cost Performance Index (CPI) is a measure of cost efficiency on a project. It is the ratio of earned value to actual cost. CPI = EV / AC. A value greater than 1 indicates the project is under budget.",
            "Schedule Performance Index (SPI) is a measure of schedule efficiency on a project. It is the ratio of earned value to planned value. SPI = EV / PV. A value greater than 1 indicates the project is ahead of schedule.",
            "A Milestone is a significant point or event in a project, program or portfolio. It often marks the completion of a major deliverable or phase of work. Milestones typically have zero duration and no effort.",
            "A Risk Register is a project management document that contains information about identified risks, their severity, and the actions steps to be taken. It is used to track and monitor risks throughout the project lifecycle.",
            "A Change Control Board (CCB) is a formally constituted group of stakeholders responsible for reviewing, evaluating, approving, delaying, or rejecting changes to a project, with all decisions and recommendations being recorded.",
            "A Project Baseline is the approved time phased plan (for a project, a work breakdown structure component, work package, or schedule activity), plus or minus approved project scope, cost, schedule, and technical changes.",
            "A Deliverable is any unique and verifiable product, result, or capability to perform a service that is required to be produced to complete a process, phase, or project. Deliverables are typically tangible components completed to meet project objectives.",
            "A Project Management Plan is a formal, approved document used to guide both project execution and project control. The project management plan documents the planning assumptions and decisions, facilitates communication among stakeholders, and documents approved scope, cost, and schedule baselines.",
            "A RACI Matrix (Responsible, Accountable, Consulted, Informed) is a responsibility assignment chart that maps out every task, milestone, or key decision involved in completing a project and assigns which roles are responsible for which actions.",
            "A Lessons Learned Register is a document created during a project that details the positive and negative experiences of the project. It is used to identify and record insights and lessons from the project that can be valuable for future projects.",
            "A Scope Statement is a document that provides a detailed description of the project and product, service, or result. It includes project deliverables, assumptions, constraints, and a description of what is in and out of scope.",
            "A Project Life Cycle is the series of phases that a project passes through from its initiation to its closure. The phases are generally sequential, and their names and numbers are determined by the management and control needs of the organization."
        ]
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Store in session state
    st.session_state.pm_knowledge = df
    
    return df

def generate_sample_project_2(today):
    """
    Generate the second sample project data (Enterprise Software Implementation).
    
    Args:
        today: Current date
        
    Returns:
        dict: Sample project data for Enterprise Software Implementation
    """
    # Calculate various dates relative to today
    project_start = today - datetime.timedelta(days=90)
    project_end = today + datetime.timedelta(days=180)
    
    # Calculate elapsed percentage
    total_days = (project_end - project_start).days
    elapsed_days = (today - project_start).days
    elapsed_pct = min(100, max(0, round(elapsed_days / total_days * 100)))
    
    # Sample WBS (Work Breakdown Structure)
    wbs = [
        {
            "id": "1",
            "task": "Project Initiation and Planning",
            "description": "Define project scope, objectives, and stakeholders",
            "start_date": (project_start).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=30)).strftime("%Y-%m-%d"),
            "duration": 30,
            "progress": 100,
            "assigned_to": "Jennifer Adams",
            "dependencies": [],
            "critical": True,
            "milestone": True
        },
        {
            "id": "1.1",
            "task": "Project Charter",
            "description": "Develop and get approval for project charter",
            "start_date": (project_start).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=10)).strftime("%Y-%m-%d"),
            "duration": 10,
            "progress": 100,
            "assigned_to": "Jennifer Adams",
            "dependencies": [],
            "critical": True,
            "milestone": False
        },
        {
            "id": "1.2",
            "task": "Stakeholder Analysis",
            "description": "Identify stakeholders and analyze their needs and expectations",
            "start_date": (project_start + datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=15)).strftime("%Y-%m-%d"),
            "duration": 10,
            "progress": 100,
            "assigned_to": "Marcus Wright",
            "dependencies": ["1.1"],
            "critical": False,
            "milestone": False
        },
        {
            "id": "1.3",
            "task": "Project Management Plan",
            "description": "Develop comprehensive project management plan",
            "start_date": (project_start + datetime.timedelta(days=15)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=30)).strftime("%Y-%m-%d"),
            "duration": 15,
            "progress": 100,
            "assigned_to": "Jennifer Adams",
            "dependencies": ["1.1", "1.2"],
            "critical": True,
            "milestone": False
        },
        {
            "id": "2",
            "task": "Requirements Analysis and Definition",
            "description": "Gather and document detailed business requirements",
            "start_date": (project_start + datetime.timedelta(days=30)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=75)).strftime("%Y-%m-%d"),
            "duration": 45,
            "progress": 100,
            "assigned_to": "Marcus Wright",
            "dependencies": ["1"],
            "critical": True,
            "milestone": True
        },
        {
            "id": "2.1",
            "task": "Business Process Analysis",
            "description": "Document current business processes and identify improvement opportunities",
            "start_date": (project_start + datetime.timedelta(days=30)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=50)).strftime("%Y-%m-%d"),
            "duration": 20,
            "progress": 100,
            "assigned_to": "Marcus Wright",
            "dependencies": ["1.3"],
            "critical": True,
            "milestone": False
        },
        {
            "id": "2.2",
            "task": "Functional Requirements",
            "description": "Define detailed functional requirements for the system",
            "start_date": (project_start + datetime.timedelta(days=45)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=65)).strftime("%Y-%m-%d"),
            "duration": 20,
            "progress": 100,
            "assigned_to": "Sophia Chen",
            "dependencies": ["2.1"],
            "critical": True,
            "milestone": False
        },
        {
            "id": "2.3",
            "task": "Requirements Validation",
            "description": "Validate and finalize requirements with stakeholders",
            "start_date": (project_start + datetime.timedelta(days=65)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=75)).strftime("%Y-%m-%d"),
            "duration": 10,
            "progress": 100,
            "assigned_to": "Marcus Wright",
            "dependencies": ["2.2"],
            "critical": True,
            "milestone": False
        },
        {
            "id": "3",
            "task": "System Design and Architecture",
            "description": "Design the technical architecture and system components",
            "start_date": (project_start + datetime.timedelta(days=75)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=105)).strftime("%Y-%m-%d"),
            "duration": 30,
            "progress": 90,
            "assigned_to": "Robert Kim",
            "dependencies": ["2"],
            "critical": True,
            "milestone": False
        },
        {
            "id": "3.1",
            "task": "Technical Architecture",
            "description": "Define system architecture and technical infrastructure",
            "start_date": (project_start + datetime.timedelta(days=75)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=90)).strftime("%Y-%m-%d"),
            "duration": 15,
            "progress": 100,
            "assigned_to": "Robert Kim",
            "dependencies": ["2.3"],
            "critical": True,
            "milestone": False
        },
        {
            "id": "3.2",
            "task": "Data Model Design",
            "description": "Design database schema and data structures",
            "start_date": (project_start + datetime.timedelta(days=85)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=100)).strftime("%Y-%m-%d"),
            "duration": 15,
            "progress": 85,
            "assigned_to": "David Wilson",
            "dependencies": ["3.1"],
            "critical": True,
            "milestone": False
        },
        {
            "id": "3.3",
            "task": "User Interface Design",
            "description": "Create wireframes and UI design specifications",
            "start_date": (project_start + datetime.timedelta(days=85)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=105)).strftime("%Y-%m-%d"),
            "duration": 20,
            "progress": 80,
            "assigned_to": "Lisa Johnson",
            "dependencies": ["3.1"],
            "critical": False,
            "milestone": False
        },
        {
            "id": "4",
            "task": "System Configuration and Development",
            "description": "Configure base system and develop custom components",
            "start_date": (project_start + datetime.timedelta(days=105)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=190)).strftime("%Y-%m-%d"),
            "duration": 85,
            "progress": 40,
            "assigned_to": "Robert Kim",
            "dependencies": ["3"],
            "critical": True,
            "milestone": False
        },
        {
            "id": "4.1",
            "task": "Base System Configuration",
            "description": "Install and configure the core enterprise software",
            "start_date": (project_start + datetime.timedelta(days=105)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=125)).strftime("%Y-%m-%d"),
            "duration": 20,
            "progress": 80,
            "assigned_to": "David Wilson",
            "dependencies": ["3.2"],
            "critical": True,
            "milestone": False
        },
        {
            "id": "4.2",
            "task": "Custom Development - Phase 1",
            "description": "Develop custom modules and extensions",
            "start_date": (project_start + datetime.timedelta(days=125)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=160)).strftime("%Y-%m-%d"),
            "duration": 35,
            "progress": 50,
            "assigned_to": "James Lee",
            "dependencies": ["4.1"],
            "critical": True,
            "milestone": False
        },
        {
            "id": "4.3",
            "task": "Custom Development - Phase 2",
            "description": "Develop reports and dashboards",
            "start_date": (project_start + datetime.timedelta(days=145)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=175)).strftime("%Y-%m-%d"),
            "duration": 30,
            "progress": 30,
            "assigned_to": "Sophia Chen",
            "dependencies": ["4.1"],
            "critical": False,
            "milestone": False
        },
        {
            "id": "4.4",
            "task": "Integration Development",
            "description": "Develop integrations with existing systems",
            "start_date": (project_start + datetime.timedelta(days)(160)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days)(190)).strftime("%Y-%m-%d"),
            "duration": 30,
            "progress": 10,
            "assigned_to": "James Lee",
            "dependencies": ["4.2"],
            "critical": True,
            "milestone": False
        },
        {
            "id": "5",
            "task": "Testing",
            "description": "Comprehensive system testing",
            "start_date": (project_start + datetime.timedelta(days=160)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=235)).strftime("%Y-%m-%d"),
            "duration": 75,
            "progress": 0,
            "assigned_to": "Maria Garcia",
            "dependencies": ["4"],
            "critical": True,
            "milestone": True
        },
        {
            "id": "5.1",
            "task": "Test Planning",
            "description": "Develop test plans and test cases",
            "start_date": (project_start + datetime.timedelta(days=140)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=160)).strftime("%Y-%m-%d"),
            "duration": 20,
            "progress": 70,
            "assigned_to": "Maria Garcia",
            "dependencies": ["3"],
            "critical": False,
            "milestone": False
        },
        {
            "id": "5.2",
            "task": "Unit Testing",
            "description": "Test individual components and modules",
            "start_date": (project_start + datetime.timedelta(days=160)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=180)).strftime("%Y-%m-%d"),
            "duration": 20,
            "progress": 15,
            "assigned_to": "Maria Garcia",
            "dependencies": ["4.2", "5.1"],
            "critical": True,
            "milestone": False
        },
        {
            "id": "5.3",
            "task": "Integration Testing",
            "description": "Test system integrations and data flows",
            "start_date": (project_start + datetime.timedelta(days=190)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=210)).strftime("%Y-%m-%d"),
            "duration": 20,
            "progress": 0,
            "assigned_to": "Maria Garcia",
            "dependencies": ["4.4", "5.2"],
            "critical": True,
            "milestone": False
        },
        {
            "id": "5.4",
            "task": "User Acceptance Testing",
            "description": "Conduct UAT with business users",
            "start_date": (project_start + datetime.timedelta(days=210)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=235)).strftime("%Y-%m-%d"),
            "duration": 25,
            "progress": 0,
            "assigned_to": "Marcus Wright",
            "dependencies": ["5.3"],
            "critical": True,
            "milestone": False
        },
        {
            "id": "6",
            "task": "Data Migration",
            "description": "Migrate data from legacy systems",
            "start_date": (project_start + datetime.timedelta(days=180)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=215)).strftime("%Y-%m-%d"),
            "duration": 35,
            "progress": 0,
            "assigned_to": "David Wilson",
            "dependencies": ["4.1"],
            "critical": False,
            "milestone": False
        },
        {
            "id": "7",
            "task": "Training and Change Management",
            "description": "Prepare and deliver user training, manage organizational change",
            "start_date": (project_start + datetime.timedelta(days=180)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=250)).strftime("%Y-%m-%d"),
            "duration": 70,
            "progress": 0,
            "assigned_to": "Lisa Johnson",
            "dependencies": ["3.3"],
            "critical": False,
            "milestone": False
        },
        {
            "id": "8",
            "task": "Deployment",
            "description": "System deployment to production",
            "start_date": (project_start + datetime.timedelta(days=235)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=250)).strftime("%Y-%m-%d"),
            "duration": 15,
            "progress": 0,
            "assigned_to": "Robert Kim",
            "dependencies": ["5.4", "6"],
            "critical": True,
            "milestone": True
        },
        {
            "id": "9",
            "task": "Post-Implementation Support",
            "description": "Provide support and implement refinements after go-live",
            "start_date": (project_start + datetime.timedelta(days=250)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=280)).strftime("%Y-%m-%d"),
            "duration": 30,
            "progress": 0,
            "assigned_to": "Jennifer Adams",
            "dependencies": ["8"],
            "critical": True,
            "milestone": False
        },
        {
            "id": "10",
            "task": "Project Closure",
            "description": "Complete project documentation and formal closure",
            "start_date": (project_start + datetime.timedelta(days=265)).strftime("%Y-%m-%d"),
            "end_date": (project_start + datetime.timedelta(days=280)).strftime("%Y-%m-%d"),
            "duration": 15,
            "progress": 0,
            "assigned_to": "Jennifer Adams",
            "dependencies": ["9"],
            "critical": True,
            "milestone": True
        }
    ]
    
    # Calculate overall project progress
    total_duration = sum(task["duration"] for task in wbs)
    weighted_progress = sum(task["duration"] * task["progress"] for task in wbs) / total_duration
    
    # Sample resources
    resources = [
        {
            "name": "Jennifer Adams",
            "role": "Project Manager",
            "availability": 160,
            "allocated": 130,
            "skills": ["Project Management", "Enterprise Software", "Change Management"]
        },
        {
            "name": "Marcus Wright",
            "role": "Business Analyst",
            "availability": 160,
            "allocated": 150,
            "skills": ["Requirements Analysis", "Process Modeling", "UAT Management"]
        },
        {
            "name": "Robert Kim",
            "role": "Technical Architect",
            "availability": 160,
            "allocated": 170,
            "skills": ["Enterprise Architecture", "System Integration", "Cloud Infrastructure"]
        },
        {
            "name": "Sophia Chen",
            "role": "Business Systems Analyst",
            "availability": 160,
            "allocated": 140,
            "skills": ["Functional Design", "Reporting", "Business Intelligence"]
        },
        {
            "name": "David Wilson",
            "role": "Database Specialist",
            "availability": 160,
            "allocated": 130,
            "skills": ["Database Design", "ETL", "Data Migration"]
        },
        {
            "name": "James Lee",
            "role": "Developer",
            "availability": 160,
            "allocated": 160,
            "skills": ["Java", "Enterprise APIs", "Microservices"]
        },
        {
            "name": "Lisa Johnson",
            "role": "Change Manager",
            "availability": 120,
            "allocated": 90,
            "skills": ["Training", "User Documentation", "Communication"]
        },
        {
            "name": "Maria Garcia",
            "role": "QA Lead",
            "availability": 160,
            "allocated": 140,
            "skills": ["Test Planning", "Automated Testing", "Performance Testing"]
        }
    ]
    
    # Sample RAID (Risks, Assumptions, Issues, Dependencies)
    raid = {
        "risks": [
            {
                "id": "R1",
                "title": "Data Migration Complexity",
                "description": "Legacy data structures may be more complex than anticipated, leading to data migration challenges.",
                "probability": "High",
                "impact": "High",
                "severity": "High",
                "mitigation": "Conduct detailed data profiling early in the project. Create a comprehensive data mapping strategy.",
                "owner": "David Wilson",
                "status": "Open"
            },
            {
                "id": "R2",
                "title": "Business Process Change Resistance",
                "description": "Users may resist changes to established business processes required by the new system.",
                "probability": "Medium",
                "impact": "High",
                "severity": "High",
                "mitigation": "Implement robust change management plan. Involve key users early in design process.",
                "owner": "Lisa Johnson",
                "status": "Open"
            },
            {
                "id": "R3",
                "title": "Integration Complexity",
                "description": "Integration with legacy systems may be more complex than initially estimated.",
                "probability": "Medium",
                "impact": "High",
                "severity": "High",
                "mitigation": "Conduct proof of concept for high-risk integrations. Allocate additional time for integration testing.",
                "owner": "Robert Kim",
                "status": "Open"
            },
            {
                "id": "R4",
                "title": "Resource Availability",
                "description": "Key subject matter experts may not be available when needed.",
                "probability": "Medium",
                "impact": "Medium",
                "severity": "Medium",
                "mitigation": "Secure resource commitments from department heads. Document knowledge from SMEs early.",
                "owner": "Jennifer Adams",
                "status": "Open"
            },
            {
                "id": "R5",
                "title": "Vendor Support",
                "description": "Software vendor support may be inadequate for complex implementation issues.",
                "probability": "Low",
                "impact": "High",
                "severity": "Medium",
                "mitigation": "Establish escalation paths with vendor. Consider premium support package.",
                "owner": "",
                "status": "Open"
            }
        ],
        "assumptions": [
            {
                "id": "A1",
                "description": "Executive sponsors will remain committed to the project throughout its duration.",
                "validation_method": "Regular status updates and executive steering committee meetings.",
                "status": "Validated"
            },
            {
                "id": "A2",
                "description": "Current hardware infrastructure is sufficient to support the new system.",
                "validation_method": "Technical assessment and performance testing.",
                "status": "Validated"
            },
            {
                "id": "A3",
                "description": "Departments will provide subject matter experts as needed throughout the project.",
                "validation_method": "Resource commitments documented in project charter.",
                "status": "Validated"
            },
            {
                "id": "A4",
                "description": "The software vendor will provide timely fixes for any critical bugs discovered.",
                "validation_method": "Review SLA in vendor contract.",
                "status": "Not Validated"
            },
            {
                "id": "A5",
                "description": "Legacy systems will remain operational during transition period.",
                "validation_method": "Confirm with IT operations team.",
                "status": "Validated"
            }
        ],
        "issues": [
            {
                "id": "I1",
                "title": "Requirements Gap in Finance Module",
                "description": "Financial reporting requirements are not fully defined for the new system.",
                "priority": "High",
                "raised_date": (today - datetime.timedelta(days=10)).strftime("%Y-%m-%d"),
                "owner": "Sophia Chen",
                "status": "In Progress"
            },
            {
                "id": "I2",
                "title": "Development Environment Performance",
                "description": "Development environment is experiencing performance issues, slowing development progress.",
                "priority": "Medium",
                "raised_date": (today - datetime.timedelta(days=15)).strftime("%Y-%m-%d"),
                "owner": "Robert Kim",
                "status": "In Progress"
            },
            {
                "id": "I3",
                "title": "API Documentation Gaps",
                "description": "Documentation for third-party API is incomplete, affecting integration design.",
                "priority": "Medium",
                "raised_date": (today - datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
                "owner": "James Lee",
                "status": "Open"
            }
        ],
        "dependencies": [
            {
                "id": "D1",
                "description": "Network infrastructure upgrade",
                "type": "External",
                "owner": "IT Infrastructure Team",
                "due_date": (project_start + datetime.timedelta(days=45)).strftime("%Y-%m-%d"),
                "status": "Completed"
            },
            {
                "id": "D2",
                "description": "Single Sign-On implementation",
                "type": "External",
                "owner": "Security Team",
                "due_date": (project_start + datetime.timedelta(days=120)).strftime("%Y-%m-%d"),
                "status": "At Risk"
            },
            {
                "id": "D3",
                "description": "Finance department approval of chart of accounts",
                "type": "Internal",
                "owner": "Finance Department",
                "due_date": (today + datetime.timedelta(days=15)).strftime("%Y-%m-%d"),
                "status": "On Track"
            },
            {
                "id": "D4",
                "description": "Legacy system API documentation",
                "type": "External",
                "owner": "IT Documentation Team",
                "due_date": (project_start + datetime.timedelta(days=90)).strftime("%Y-%m-%d"),
                "status": "Completed"
            }
        ]
    }
    
    # Sample team feedback
    team_feedback = [
        {
            "member": "James Lee",
            "date": (today - datetime.timedelta(days=7)).strftime("%Y-%m-%d"),
            "content": "We're facing challenges with the integration between the new system and the CRM. The API documentation doesn't cover all the endpoints we need to use."
        },
        {
            "member": "Sophia Chen",
            "date": (today - datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
            "content": "The finance department has been very cooperative in providing requirements, but there are still some open questions about the tax calculation logic."
        },
        {
            "member": "Maria Garcia",
            "date": (today - datetime.timedelta(days=3)).strftime("%Y-%m-%d"),
            "content": "Test environment setup is progressing well. We should be ready to start systematic testing by next week."
        },
        {
            "member": "David Wilson",
            "date": (today - datetime.timedelta(days=2)).strftime("%Y-%m-%d"),
            "content": "The data model design is almost complete, but we've identified additional tables needed for reporting purposes that weren't in the original scope."
        },
        {
            "member": "Lisa Johnson",
            "date": (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
            "content": "Initial user feedback on the UI design has been positive. Users particularly like the dashboard layout and the simplified navigation."
        }
    ]
    
    # Sample decisions log
    decisions = [
        {
            "id": "D1",
            "title": "Enterprise Software Selection",
            "description": "Selected XYZ Enterprise Suite as the core system based on functional fit, scalability, and total cost of ownership analysis.",
            "date": (project_start + datetime.timedelta(days=10)).strftime("%Y-%m-%d"),
            "owner": "Jennifer Adams",
            "status": "Approved",
            "impact": "Determines the core technology platform and implementation approach for the entire project."
        },
        {
            "id": "D2",
            "title": "Cloud vs. On-Premise Deployment",
            "description": "Decided to deploy the system in a hybrid model with core components on-premise and certain modules in the cloud.",
            "date": (project_start + datetime.timedelta(days=20)).strftime("%Y-%m-%d"),
            "owner": "Robert Kim",
            "status": "Approved",
            "impact": "Affects infrastructure requirements, security approach, and operational costs."
        },
        {
            "id": "D3",
            "title": "Phased Implementation Approach",
            "description": "Approved a phased roll-out strategy with finance and HR modules in Phase 1, followed by operations and sales in Phase 2.",
            "date": (project_start + datetime.timedelta(days=30)).strftime("%Y-%m-%d"),
            "owner": "Jennifer Adams",
            "status": "Approved",
            "impact": "Reduces implementation risk but extends overall timeline. Requires maintaining legacy systems longer."
        },
        {
            "id": "D4",
            "title": "Custom Development for Reporting",
            "description": "Decision to develop custom reporting module rather than using vendor's standard reports due to specific business requirements.",
            "date": (project_start + datetime.timedelta(days=80)).strftime("%Y-%m-%d"),
            "owner": "Sophia Chen",
            "status": "Approved",
            "impact": "Increases development effort but provides better alignment with business needs. May affect upgradability."
        },
        {
            "id": "D5",
            "title": "Legacy Data Migration Strategy",
            "description": "Decision on what historical data to migrate (3 years of transactional data, all master data) and migration approach.",
            "date": (project_start + datetime.timedelta(days=100)).strftime("%Y-%m-%d"),
            "owner": "David Wilson",
            "status": "Approved",
            "impact": "Affects data migration effort, storage requirements, and system performance."
        },
        {
            "id": "D6",
            "title": "Training Approach",
            "description": "Evaluating whether to use train-the-trainer approach or direct end-user training by implementation team.",
            "date": (today - datetime.timedelta(days=10)).strftime("%Y-%m-%d"),
            "owner": "Lisa Johnson",
            "status": "Under Review",
            "impact": "Will affect training timeline, resource requirements, and knowledge transfer effectiveness."
        }
    ]
    
    # Sample activities log
    activities = [
        {
            "date": (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
            "description": "Weekly status meeting: Reviewed progress on data model design and development tasks."
        },
        {
            "date": (today - datetime.timedelta(days=2)).strftime("%Y-%m-%d"),
            "description": "Technical review meeting for integration approach with CRM system."
        },
        {
            "date": (today - datetime.timedelta(days=3)).strftime("%Y-%m-%d"),
            "description": "Stakeholder meeting with Finance department to review requirements for tax calculation."
        },
        {
            "date": (today - datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
            "description": "Risk review meeting: Identified new risk related to data migration complexity."
        },
        {
            "date": (today - datetime.timedelta(days=7)).strftime("%Y-%m-%d"),
            "description": "Demo of UI prototype to key users from HR department."
        },
        {
            "date": (today - datetime.timedelta(days=8)).strftime("%Y-%m-%d"),
            "description": "Technical environment setup for development team."
        }
    ]
    
    # Sample scope changes
    scope_changes = [
        {
            "id": "SC1",
            "title": "Additional Reporting Requirements",
            "description": "Added 15 custom reports for executive dashboard not in original requirements.",
            "requested_by": "CFO",
            "date": (project_start + datetime.timedelta(days=60)).strftime("%Y-%m-%d"),
            "status": "Approved",
            "impact": "Increases development effort by approximately 15 person-days. No impact on critical path."
        },
        {
            "id": "SC2",
            "title": "Advanced Analytics Module",
            "description": "Added requirement for predictive analytics capabilities in sales forecasting.",
            "requested_by": "Sales Director",
            "date": (project_start + datetime.timedelta(days=95)).strftime("%Y-%m-%d"),
            "status": "Approved",
            "impact": "Adds new phase to project with 30 person-days effort. Extends timeline by 15 days."
        },
        {
            "id": "SC3",
            "title": "Mobile Application Access",
            "description": "Added requirement for mobile access to key system functions.",
            "requested_by": "COO",
            "date": (today - datetime.timedelta(days=20)).strftime("%Y-%m-%d"),
            "status": "Under Review",
            "impact": "Potentially adds 45 person-days of effort and new technical requirements. May extend timeline by 30 days."
        },
        {
            "id": "SC4",
            "title": "Integration with Additional Third-Party System",
            "description": "Added requirement to integrate with new supply chain management system.",
            "requested_by": "Logistics Manager",
            "date": (today - datetime.timedelta(days=10)).strftime("%Y-%m-%d"),
            "status": "Under Review",
            "impact": "Adds complexity to integration scope. Estimated 20 person-days additional effort."
        }
    ]
    
    # Create the complete project structure
    project = {
        "name": "Enterprise Software Implementation",
        "description": "Implementation of company-wide ERP system replacing legacy applications, including finance, HR, operations, and reporting modules.",
        "start_date": project_start.strftime("%Y-%m-%d"),
        "end_date": project_end.strftime("%Y-%m-%d"),
        "budget": 2500000,
        "budget_spent": 1125000,
        "budget_spent_pct": 45,
        "progress": round(weighted_progress),
        "status": "On Track",
        "elapsed_pct": elapsed_pct,
        "wbs": wbs,
        "resources": resources,
        "raid": raid,
        "team_feedback": team_feedback,
        "decisions": decisions,
        "activities": activities,
        "scope_changes": scope_changes
    }
    
    return project