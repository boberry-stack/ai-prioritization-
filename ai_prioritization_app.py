import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
from datetime import datetime
from supabase import create_client
import anthropic
import os

# Page configuration
st.set_page_config(
    page_title="AI Project Prioritization",
    page_icon="🎯",
    layout="wide"
)

# --- Supabase Connection ---
@st.cache_resource
def get_supabase_client():
    """Initialize Supabase client"""
    url = None
    key = None
    try:
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")
    except Exception:
        pass
    if not url:
        url = os.environ.get("SUPABASE_URL")
    if not key:
        key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        st.error("Supabase credentials not found. Please set SUPABASE_URL and SUPABASE_KEY in your secrets.")
        st.stop()

    return create_client(url, key)

supabase = get_supabase_client()

# --- Database Functions ---
def db_get_all_sessions():
    """Load all sessions from Supabase"""
    try:
        response = supabase.table("sessions").select("*").order("last_modified", desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Failed to load sessions: {str(e)}")
        return []

def db_create_session(session_name):
    """Create a new session in Supabase"""
    safe_id = session_name.replace(" ", "_").lower()
    try:
        supabase.table("sessions").upsert({
            "id": safe_id,
            "name": session_name,
            "project_count": 0,
            "last_modified": datetime.now().isoformat()
        }).execute()
        return safe_id
    except Exception as e:
        st.error(f"Failed to create session: {str(e)}")
        return None

def db_load_session_projects(session_id):
    """Load all projects for a session from Supabase"""
    try:
        response = supabase.table("projects").select("*").eq("session_id", session_id).order("created_at").execute()
        projects = []
        for row in (response.data or []):
            projects.append({
                "db_id": row["id"],
                "project_name": row["project_name"],
                "description": row["description"],
                "tech_feasibility": float(row["tech_feasibility"]),
                "business_value": float(row["business_value"]),
                "category": row["category"],
                "justification": row["justification"],
                "answers": row["answers"] if row["answers"] else {},
                "timestamp": row["created_at"]
            })
        return projects
    except Exception as e:
        st.error(f"Failed to load projects: {str(e)}")
        return []

def db_add_project(session_id, project_data):
    """Add a project to Supabase"""
    try:
        supabase.table("projects").insert({
            "session_id": session_id,
            "project_name": project_data["project_name"],
            "description": project_data["description"],
            "tech_feasibility": project_data["tech_feasibility"],
            "business_value": project_data["business_value"],
            "category": project_data["category"],
            "justification": project_data["justification"],
            "answers": project_data.get("answers", {})
        }).execute()

        # Update session project count and timestamp
        count_resp = supabase.table("projects").select("id", count="exact").eq("session_id", session_id).execute()
        project_count = count_resp.count if count_resp.count else 0
        supabase.table("sessions").update({
            "project_count": project_count,
            "last_modified": datetime.now().isoformat()
        }).eq("id", session_id).execute()

        return True
    except Exception as e:
        st.error(f"Failed to add project: {str(e)}")
        return False

def db_delete_project(project_db_id, session_id):
    """Delete a project from Supabase"""
    try:
        supabase.table("projects").delete().eq("id", project_db_id).execute()

        # Update session project count
        count_resp = supabase.table("projects").select("id", count="exact").eq("session_id", session_id).execute()
        project_count = count_resp.count if count_resp.count else 0
        supabase.table("sessions").update({
            "project_count": project_count,
            "last_modified": datetime.now().isoformat()
        }).eq("id", session_id).execute()

        return True
    except Exception as e:
        st.error(f"Failed to delete project: {str(e)}")
        return False

def db_delete_session(session_id):
    """Delete a session and all its projects from Supabase"""
    try:
        supabase.table("projects").delete().eq("session_id", session_id).execute()
        supabase.table("sessions").delete().eq("id", session_id).execute()
        return True
    except Exception as e:
        st.error(f"Failed to delete session: {str(e)}")
        return False

# --- Initialize session state ---
if 'projects' not in st.session_state:
    st.session_state.projects = []
if 'current_project' not in st.session_state:
    st.session_state.current_project = {}
if 'current_session_name' not in st.session_state:
    st.session_state.current_session_name = None
if 'current_session_id' not in st.session_state:
    st.session_state.current_session_id = None

# Benchmark use cases for reference
BENCHMARK_USE_CASES = {
    "chatbot": {"tech_feasibility": 8, "business_value": 7, "category": "low_hanging"},
    "document_search": {"tech_feasibility": 9, "business_value": 8, "category": "low_hanging"},
    "sentiment_analysis": {"tech_feasibility": 8, "business_value": 6, "category": "low_hanging"},
    "code_generation": {"tech_feasibility": 7, "business_value": 8, "category": "low_hanging"},
    "predictive_maintenance": {"tech_feasibility": 6, "business_value": 9, "category": "disruptive"},
    "autonomous_systems": {"tech_feasibility": 3, "business_value": 10, "category": "disruptive"},
    "recommendation_engine": {"tech_feasibility": 7, "business_value": 8, "category": "low_hanging"},
    "fraud_detection": {"tech_feasibility": 6, "business_value": 9, "category": "disruptive"},
    "personalization": {"tech_feasibility": 7, "business_value": 7, "category": "low_hanging"},
    "image_recognition": {"tech_feasibility": 8, "business_value": 7, "category": "low_hanging"},
    "forecasting": {"tech_feasibility": 6, "business_value": 8, "category": "disruptive"},
}

# Intake questions
INTAKE_QUESTIONS = {
    "basic_info": [
        {
            "id": "project_name",
            "question": "What is the name of your AI use case/project?",
            "type": "text",
            "help": "e.g., Customer Support Chatbot, Invoice Processing AI, etc."
        },
        {
            "id": "description",
            "question": "Provide a brief description of the use case",
            "type": "textarea",
            "help": "Describe what the AI system will do and its primary purpose"
        }
    ],
    "business_value": [
        {
            "id": "revenue_impact",
            "question": "What is the expected revenue impact?",
            "type": "select",
            "options": ["None (0)", "Low ($10K-$100K)", "Medium ($100K-$1M)", "High ($1M-$10M)", "Very High (>$10M)"],
            "score_map": {"None (0)": 0, "Low ($10K-$100K)": 2, "Medium ($100K-$1M)": 5, "High ($1M-$10M)": 8, "Very High (>$10M)": 10}
        },
        {
            "id": "cost_savings",
            "question": "What are the expected cost savings?",
            "type": "select",
            "options": ["None", "Low (<$50K)", "Medium ($50K-$500K)", "High ($500K-$2M)", "Very High (>$2M)"],
            "score_map": {"None": 0, "Low (<$50K)": 2, "Medium ($50K-$500K)": 5, "High ($500K-$2M)": 8, "Very High (>$2M)": 10}
        },
        {
            "id": "users_impacted",
            "question": "How many users/customers will be impacted?",
            "type": "select",
            "options": ["<100", "100-1,000", "1,000-10,000", "10,000-100,000", ">100,000"],
            "score_map": {"<100": 2, "100-1,000": 4, "1,000-10,000": 6, "10,000-100,000": 8, ">100,000": 10}
        },
        {
            "id": "strategic_alignment",
            "question": "How well does this align with strategic priorities?",
            "type": "select",
            "options": ["Not aligned", "Somewhat aligned", "Aligned", "Highly aligned", "Critical priority"],
            "score_map": {"Not aligned": 2, "Somewhat aligned": 4, "Aligned": 6, "Highly aligned": 8, "Critical priority": 10}
        },
        {
            "id": "time_to_value",
            "question": "How quickly can value be realized?",
            "type": "select",
            "options": ["12+ months", "6-12 months", "3-6 months", "1-3 months", "<1 month"],
            "score_map": {"12+ months": 2, "6-12 months": 4, "3-6 months": 6, "1-3 months": 8, "<1 month": 10}
        }
    ],
    "tech_feasibility": [
        {
            "id": "data_availability",
            "question": "What is the current state of required data?",
            "type": "select",
            "options": ["No data exists", "Data exists but poor quality", "Data exists, needs cleaning", "Good quality data available", "Excellent, ready-to-use data"],
            "score_map": {"No data exists": 2, "Data exists but poor quality": 4, "Data exists, needs cleaning": 6, "Good quality data available": 8, "Excellent, ready-to-use data": 10}
        },
        {
            "id": "technical_complexity",
            "question": "What is the technical complexity of the solution?",
            "type": "select",
            "options": ["Very complex/novel", "Complex", "Moderate", "Straightforward", "Simple/proven technology"],
            "score_map": {"Very complex/novel": 2, "Complex": 4, "Moderate": 6, "Straightforward": 8, "Simple/proven technology": 10}
        },
        {
            "id": "team_skills",
            "question": "Does your team have the required AI/ML skills?",
            "type": "select",
            "options": ["No skills, need to hire", "Limited skills", "Some skills, need training", "Good skills available", "Expert team ready"],
            "score_map": {"No skills, need to hire": 2, "Limited skills": 4, "Some skills, need training": 6, "Good skills available": 8, "Expert team ready": 10}
        },
        {
            "id": "infrastructure",
            "question": "What is the state of required infrastructure?",
            "type": "select",
            "options": ["Needs major investment", "Needs significant setup", "Needs some setup", "Mostly ready", "Fully ready"],
            "score_map": {"Needs major investment": 2, "Needs significant setup": 4, "Needs some setup": 6, "Mostly ready": 8, "Fully ready": 10}
        },
        {
            "id": "integration",
            "question": "How easy is integration with existing systems?",
            "type": "select",
            "options": ["Very difficult, major changes", "Difficult", "Moderate effort", "Straightforward", "Very easy, APIs ready"],
            "score_map": {"Very difficult, major changes": 2, "Difficult": 4, "Moderate effort": 6, "Straightforward": 8, "Very easy, APIs ready": 10}
        }
    ]
}

def analyze_with_claude(project_name, description, answers):
    """Use Claude to intelligently score the project based on benchmarks and answers"""

    # Check if API key is available (try Streamlit secrets first, then env var)
    api_key = None
    try:
        api_key = st.secrets.get("ANTHROPIC_API_KEY")
    except Exception:
        pass
    if not api_key:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        st.warning("Claude API key not found. Using fallback scoring method.")
        return calculate_scores_fallback(answers)

    try:
        client = anthropic.Anthropic(api_key=api_key)

        prompt = f"""Analyze this AI project and provide scoring based on benchmarks and the intake questionnaire.

Project Name: {project_name}
Description: {description}

Benchmark Use Cases (for reference):
{json.dumps(BENCHMARK_USE_CASES, indent=2)}

User Answers:
{json.dumps(answers, indent=2)}

Based on the project name, description, similarity to benchmark use cases, and the questionnaire answers, provide:
1. A tech_feasibility score (1-10, where 10 is most feasible)
2. A business_value score (1-10, where 10 is highest value)
3. A category ("low_hanging" for high feasibility + high value, "disruptive" for lower feasibility but very high value, or "incremental" for others)
4. A brief justification (2-3 sentences)

Consider:
- How similar is this to proven benchmark use cases?
- Do the answers indicate strong data availability and technical readiness?
- Is there clear business value and strategic alignment?
- What are the main risks or opportunities?

Respond ONLY with valid JSON in this exact format:
{{
    "tech_feasibility": <score 1-10>,
    "business_value": <score 1-10>,
    "category": "<low_hanging|disruptive|incremental>",
    "justification": "<your analysis>"
}}"""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_text = message.content[0].text.strip()

        # Extract JSON from response
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        result = json.loads(response_text)
        return result

    except Exception as e:
        st.warning(f"Claude analysis failed ({str(e)}). Using fallback scoring.")
        return calculate_scores_fallback(answers)

def calculate_scores_fallback(answers):
    """Fallback scoring method if Claude API is not available"""
    business_scores = []
    tech_scores = []

    for category, questions in INTAKE_QUESTIONS.items():
        if category == "basic_info":
            continue

        for q in questions:
            if q["id"] in answers and "score_map" in q:
                score = q["score_map"].get(answers[q["id"]], 5)

                if category == "business_value":
                    business_scores.append(score)
                elif category == "tech_feasibility":
                    tech_scores.append(score)

    tech_feasibility = round(sum(tech_scores) / len(tech_scores), 1) if tech_scores else 5
    business_value = round(sum(business_scores) / len(business_scores), 1) if business_scores else 5

    # Determine category
    if tech_feasibility >= 7 and business_value >= 7:
        category = "low_hanging"
    elif business_value >= 8 and tech_feasibility < 7:
        category = "disruptive"
    else:
        category = "incremental"

    return {
        "tech_feasibility": tech_feasibility,
        "business_value": business_value,
        "category": category,
        "justification": "Scores calculated from questionnaire responses (Claude analysis not available)"
    }

def create_prioritization_chart(projects_df):
    """Create interactive plotly chart"""

    if projects_df.empty:
        st.info("No projects to display. Add your first project using the form below.")
        return

    # Define colors
    color_map = {
        "low_hanging": "#10b981",  # Green
        "disruptive": "#f59e0b",   # Orange
        "incremental": "#6366f1"   # Blue
    }

    fig = go.Figure()

    for category in ["low_hanging", "disruptive", "incremental"]:
        df_filtered = projects_df[projects_df['category'] == category]

        if not df_filtered.empty:
            fig.add_trace(go.Scatter(
                x=df_filtered['business_value'],
                y=df_filtered['tech_feasibility'],
                mode='markers+text',
                name=category.replace('_', ' ').title(),
                marker=dict(
                    size=20,
                    color=color_map[category],
                    line=dict(width=2, color='white')
                ),
                text=df_filtered['project_name'],
                textposition="top center",
                textfont=dict(size=10),
                hovertemplate='<b>%{text}</b><br>' +
                             'Business Value: %{x}<br>' +
                             'Tech Feasibility: %{y}<br>' +
                             '<extra></extra>'
            ))

    # Add quadrant lines
    fig.add_hline(y=5, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=5, line_dash="dash", line_color="gray", opacity=0.5)

    # Add quadrant labels
    fig.add_annotation(x=2.5, y=9, text="High Effort<br>Low Value", showarrow=False,
                      font=dict(size=12, color="gray"), opacity=0.5)
    fig.add_annotation(x=7.5, y=9, text="Quick Wins", showarrow=False,
                      font=dict(size=14, color="#10b981", family="Arial Black"), opacity=0.7)
    fig.add_annotation(x=2.5, y=2, text="Low Priority", showarrow=False,
                      font=dict(size=12, color="gray"), opacity=0.5)
    fig.add_annotation(x=7.5, y=2, text="Strategic<br>Bets", showarrow=False,
                      font=dict(size=12, color="#f59e0b"), opacity=0.7)

    fig.update_layout(
        title="AI Project Prioritization Matrix",
        xaxis_title="Business Value ->",
        yaxis_title="Technical Feasibility ->",
        xaxis=dict(range=[0, 10.5], dtick=1),
        yaxis=dict(range=[0, 10.5], dtick=1),
        height=600,
        showlegend=True,
        plot_bgcolor='rgba(250,250,250,0.8)',
        hovermode='closest'
    )

    st.plotly_chart(fig, use_container_width=True)

def main():
    st.title("AI Project Prioritization Tool")
    st.markdown("### Intelligent scoring based on benchmarks and your intake questionnaire")

    # Sidebar for navigation
    with st.sidebar:
        st.header("Navigation")
        page = st.radio("Go to", [
            "Dashboard",
            "Add Project",
            "View All Projects",
            "Export Data",
            "Sessions"
        ])

        st.markdown("---")

        # Show current session info
        if st.session_state.current_session_name:
            st.success(f"Session: **{st.session_state.current_session_name}**")
            st.caption(f"{len(st.session_state.projects)} project(s)")
        else:
            st.warning("No session loaded. Go to Sessions to create or load one.")

        st.markdown("---")
        st.markdown("### Legend")
        st.markdown("**Low Hanging Fruit**: High value, high feasibility")
        st.markdown("**Disruptive**: High value, lower feasibility")
        st.markdown("**Incremental**: Other projects")

    if page == "Dashboard":
        st.header("Project Portfolio Overview")

        if st.session_state.projects:
            projects_df = pd.DataFrame(st.session_state.projects)

            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Projects", len(projects_df))
            with col2:
                low_hanging = len(projects_df[projects_df['category'] == 'low_hanging'])
                st.metric("Quick Wins", low_hanging)
            with col3:
                disruptive = len(projects_df[projects_df['category'] == 'disruptive'])
                st.metric("Disruptive", disruptive)
            with col4:
                avg_value = projects_df['business_value'].mean()
                st.metric("Avg Business Value", f"{avg_value:.1f}")

            st.markdown("---")
            create_prioritization_chart(projects_df)

            # Top recommendations
            st.markdown("### Top Recommendations")
            top_projects = projects_df.nlargest(3, ['business_value', 'tech_feasibility'])

            for idx, project in top_projects.iterrows():
                label = "Low Hanging" if project['category']=='low_hanging' else "Disruptive" if project['category']=='disruptive' else "Incremental"
                with st.expander(f"[{label}] {project['project_name']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Business Value", project['business_value'])
                        st.metric("Tech Feasibility", project['tech_feasibility'])
                    with col2:
                        st.write("**Justification:**")
                        st.write(project['justification'])
        else:
            st.info("Welcome! Add your first AI project to get started.")

    elif page == "Add Project":
        st.header("Add New AI Project")

        if not st.session_state.current_session_id:
            st.warning("Please create or load a session first (go to Sessions).")
            st.stop()

        with st.form("project_intake"):
            st.subheader("Basic Information")
            answers = {}

            for q in INTAKE_QUESTIONS["basic_info"]:
                if q["type"] == "text":
                    answers[q["id"]] = st.text_input(q["question"], help=q.get("help"))
                elif q["type"] == "textarea":
                    answers[q["id"]] = st.text_area(q["question"], help=q.get("help"))

            st.markdown("---")
            st.subheader("Business Value Assessment")
            for q in INTAKE_QUESTIONS["business_value"]:
                answers[q["id"]] = st.selectbox(q["question"], q["options"], key=q["id"])

            st.markdown("---")
            st.subheader("Technical Feasibility Assessment")
            for q in INTAKE_QUESTIONS["tech_feasibility"]:
                answers[q["id"]] = st.selectbox(q["question"], q["options"], key=q["id"])

            submitted = st.form_submit_button("Analyze & Add Project")

            if submitted:
                if not answers["project_name"] or not answers["description"]:
                    st.error("Please provide project name and description.")
                else:
                    with st.spinner("Analyzing your project with AI benchmarking..."):
                        result = analyze_with_claude(
                            answers["project_name"],
                            answers["description"],
                            answers
                        )

                        new_project = {
                            "project_name": answers["project_name"],
                            "description": answers["description"],
                            "tech_feasibility": result["tech_feasibility"],
                            "business_value": result["business_value"],
                            "category": result["category"],
                            "justification": result["justification"],
                            "answers": answers,
                        }

                        # Save to Supabase
                        if db_add_project(st.session_state.current_session_id, new_project):
                            # Reload projects from DB
                            st.session_state.projects = db_load_session_projects(st.session_state.current_session_id)
                            st.success(f"Project '{answers['project_name']}' added and saved to database!")

                            # Show results
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Tech Feasibility", result["tech_feasibility"])
                            with col2:
                                st.metric("Business Value", result["business_value"])
                            with col3:
                                category_label = result['category'].replace('_', ' ').title()
                                st.metric("Category", category_label)

                            st.info(f"**Analysis:** {result['justification']}")

    elif page == "View All Projects":
        st.header("All Projects")

        if st.session_state.projects:
            projects_df = pd.DataFrame(st.session_state.projects)

            # Display table
            display_df = projects_df[['project_name', 'business_value', 'tech_feasibility', 'category']].copy()
            display_df.columns = ['Project Name', 'Business Value', 'Tech Feasibility', 'Category']
            display_df['Category'] = display_df['Category'].str.replace('_', ' ').str.title()

            st.dataframe(display_df, use_container_width=True)

            # Details
            st.markdown("### Project Details")
            project_names = [p['project_name'] for p in st.session_state.projects]
            selected_project = st.selectbox("Select a project to view details", project_names)

            if selected_project:
                project = next(p for p in st.session_state.projects if p['project_name'] == selected_project)

                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Description:** {project['description']}")
                    st.write(f"**Category:** {project['category'].replace('_', ' ').title()}")
                with col2:
                    st.metric("Business Value", project['business_value'])
                    st.metric("Tech Feasibility", project['tech_feasibility'])

                st.write(f"**Justification:** {project['justification']}")

                if st.button(f"Delete {selected_project}"):
                    if db_delete_project(project.get("db_id"), st.session_state.current_session_id):
                        st.session_state.projects = db_load_session_projects(st.session_state.current_session_id)
                        st.rerun()
        else:
            st.info("No projects yet. Add your first project!")

    elif page == "Export Data":
        st.header("Export Project Data")

        if st.session_state.projects:
            projects_df = pd.DataFrame(st.session_state.projects)

            # JSON export
            export_projects = [{k: v for k, v in p.items() if k != "db_id"} for p in st.session_state.projects]
            json_str = json.dumps(export_projects, indent=2)
            st.download_button(
                label="Download as JSON",
                data=json_str,
                file_name=f"ai_projects_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )

            # CSV export
            csv_df = projects_df[['project_name', 'description', 'business_value', 'tech_feasibility', 'category', 'justification']]
            csv_str = csv_df.to_csv(index=False)
            st.download_button(
                label="Download as CSV",
                data=csv_str,
                file_name=f"ai_projects_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No projects to export yet.")

    elif page == "Sessions":
        st.header("Session Management")
        st.markdown("Save your work and come back to it anytime. Each session keeps all your projects organized in the cloud.")

        # --- Create New Session ---
        st.subheader("Create New Session")
        with st.form("new_session"):
            new_session_name = st.text_input(
                "Session name",
                placeholder="e.g., Q1 2026 AI Roadmap, Marketing AI Projects..."
            )
            create_btn = st.form_submit_button("Create Session")

            if create_btn and new_session_name:
                session_id = db_create_session(new_session_name)
                if session_id:
                    st.session_state.current_session_name = new_session_name
                    st.session_state.current_session_id = session_id
                    st.session_state.projects = []
                    st.success(f"Session '{new_session_name}' created! Go to Add Project to start adding use cases.")
                    st.rerun()
            elif create_btn:
                st.error("Please enter a session name.")

        st.markdown("---")

        # --- Load Existing Session ---
        st.subheader("Saved Sessions")
        sessions = db_get_all_sessions()

        if sessions:
            for session in sessions:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    last_mod = datetime.fromisoformat(session['last_modified']).strftime("%b %d, %Y %H:%M")
                    st.markdown(f"**{session['name']}**")
                    st.caption(f"{session['project_count']} project(s) | Last modified: {last_mod}")
                with col2:
                    if st.button("Load", key=f"load_{session['id']}"):
                        st.session_state.projects = db_load_session_projects(session['id'])
                        st.session_state.current_session_name = session['name']
                        st.session_state.current_session_id = session['id']
                        st.success(f"Loaded '{session['name']}' with {len(st.session_state.projects)} project(s)")
                        st.rerun()
                with col3:
                    if st.button("Delete", key=f"del_{session['id']}"):
                        if db_delete_session(session['id']):
                            if st.session_state.current_session_id == session['id']:
                                st.session_state.current_session_name = None
                                st.session_state.current_session_id = None
                                st.session_state.projects = []
                            st.rerun()

                st.markdown("---")
        else:
            st.info("No saved sessions yet. Create your first one above!")

        # --- Import Session from JSON ---
        st.subheader("Import Session")
        uploaded_file = st.file_uploader("Upload a previously exported JSON file", type="json")
        if uploaded_file:
            try:
                imported_data = json.load(uploaded_file)
                import_name = st.text_input("Name for imported session", value=f"Imported {datetime.now().strftime('%b %d')}")
                if st.button("Import"):
                    # Handle both raw project lists and session-format files
                    if isinstance(imported_data, list):
                        projects = imported_data
                    elif isinstance(imported_data, dict) and "projects" in imported_data:
                        projects = imported_data["projects"]
                    else:
                        st.error("Unrecognized file format.")
                        projects = None

                    if projects is not None:
                        session_id = db_create_session(import_name)
                        if session_id:
                            for p in projects:
                                db_add_project(session_id, p)
                            st.session_state.projects = db_load_session_projects(session_id)
                            st.session_state.current_session_name = import_name
                            st.session_state.current_session_id = session_id
                            st.success(f"Imported {len(projects)} project(s) into '{import_name}'")
                            st.rerun()
            except Exception as e:
                st.error(f"Failed to import: {str(e)}")

if __name__ == "__main__":
    main()
