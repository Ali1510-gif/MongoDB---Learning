# app.py
import streamlit as st
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, date
import pandas as pd
px = None
try:
    import plotly.express as px  # type: ignore[import]
except ModuleNotFoundError:
    px = None

from PIL import Image
import base64
from io import BytesIO

# ==========================
# Page Configuration
# ==========================
st.set_page_config(
    page_title="TaskFlow - Modern Todo Manager",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================
# Custom CSS for Modern UI
# ==========================
def load_css():
    st.markdown("""
    <style>
    /* Modern Font and Background */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Main Container */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Task Cards */
    .task-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-left: 5px solid #667eea;
    }
    
    .task-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    
    .task-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    
    .task-description {
        color: #718096;
        margin-bottom: 0.5rem;
        line-height: 1.5;
    }
    
    .task-meta {
        font-size: 0.85rem;
        color: #a0aec0;
        margin-top: 0.5rem;
    }
    
    /* Stats Cards */
    .stat-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #718096;
        margin-top: 0.5rem;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Success/Error Messages */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid;
    }
    
    /* Form Elements */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102,126,234,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================
# Database Configuration
# ==========================
@st.cache_resource
def init_connection():
    """Initialize MongoDB connection"""
    MONGO_URL = "mongodb://localhost:27017/"
    client = MongoClient(MONGO_URL)
    db = client.todo_db
    return db.tasks

task_collection = init_connection()

# ==========================
# Task Management Functions
# ==========================
def normalize_due_date(due_date):
    """Normalize due date to a MongoDB-friendly datetime object."""
    if due_date is None:
        return None
    if isinstance(due_date, datetime):
        return datetime(due_date.year, due_date.month, due_date.day)
    if isinstance(due_date, date):
        return datetime(due_date.year, due_date.month, due_date.day)
    if isinstance(due_date, str):
        try:
            return datetime.fromisoformat(due_date)
        except ValueError:
            return None
    return None


def add_task(title, description, priority, due_date):
    """Add a new task to database"""
    task = {
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": normalize_due_date(due_date),
        "status": "Pending",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    return task_collection.insert_one(task)

def get_all_tasks():
    """Get all tasks from database"""
    tasks = list(task_collection.find().sort("created_at", -1))
    # Ensure all tasks have required fields
    for task in tasks:
        if 'status' not in task:
            task['status'] = 'Pending'
        if 'created_at' not in task:
            task['created_at'] = datetime.now()
        if 'updated_at' not in task:
            task['updated_at'] = datetime.now()
        if 'description' not in task:
            task['description'] = ''
        if 'title' not in task:
            task['title'] = 'Untitled'
        if 'priority' not in task:
            task['priority'] = 'Medium'
    return tasks

def get_task_stats():
    """Get task statistics"""
    total_tasks = task_collection.count_documents({})
    
    # Handle missing status fields in count
    pending_tasks = task_collection.count_documents({
        "$or": [
            {"status": "Pending"},
            {"status": {"$exists": False}}  # Count tasks without status as Pending
        ]
    })
    completed_tasks = task_collection.count_documents({"status": "Completed"})
    
    priority_stats = {
        "High": task_collection.count_documents({"priority": "High"}),
        "Medium": task_collection.count_documents({"priority": "Medium"}),
        "Low": task_collection.count_documents({"priority": "Low"})
    }
    
    return {
        "total": total_tasks,
        "pending": pending_tasks,
        "completed": completed_tasks,
        "priority": priority_stats
    }

def update_task_status(task_id, status):
    """Update task status"""
    result = task_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {"status": status, "updated_at": datetime.now()}}
    )
    return result.modified_count > 0

def update_task(task_id, title, description, priority, due_date):
    """Update task details"""
    result = task_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": normalize_due_date(due_date),
            "updated_at": datetime.now()
        }}
    )
    return result.modified_count > 0

def delete_task(task_id):
    """Delete a task"""
    result = task_collection.delete_one({"_id": ObjectId(task_id)})
    return result.deleted_count > 0

def search_tasks(keyword):
    """Search tasks by title or description"""
    regex_pattern = {"$regex": keyword, "$options": "i"}
    tasks = list(task_collection.find({
        "$or": [
            {"title": regex_pattern},
            {"description": regex_pattern}
        ]
    }).sort("created_at", -1))
    # Ensure all tasks have required fields
    for task in tasks:
        if 'status' not in task:
            task['status'] = 'Pending'
        if 'title' not in task:
            task['title'] = 'Untitled'
        if 'description' not in task:
            task['description'] = ''
        if 'priority' not in task:
            task['priority'] = 'Medium'
    return tasks

# ==========================
# Main Application
# ==========================
def main():
    load_css()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>✨ TaskFlow ✨</h1>
        <p>Your Modern Task Management Solution</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        selected = st.radio(
            "",
            ["Dashboard", "Add Task", "View Tasks", "Search", "Statistics"],
            index=0
        )
        
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        stats = get_task_stats()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Tasks", stats['total'])
        with col2:
            st.metric("Completed", f"{stats['completed']}/{stats['total']}")
    
    # Dashboard View
    if selected == "Dashboard":
        st.markdown("## 📋 Recent Tasks")
        
        tasks = get_all_tasks()
        if not tasks:
            st.info("✨ No tasks yet! Click 'Add Task' to create your first task.")
        else:
            cols = st.columns(3)
            priority_colors = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
            
            for idx, task in enumerate(tasks[:6]):  # Show only 6 most recent
                with cols[idx % 3]:
                    # Safe access with default values
                    status = task.get('status', 'Pending')
                    status_color = "✅" if status == "Completed" else "⏳"
                    title = task.get('title', 'Untitled')
                    description = task.get('description', '')
                    priority = task.get('priority', 'Medium')
                    created_at = task.get('created_at', datetime.now())
                    
                    with st.container():
                        st.markdown(f"""
                        <div class="task-card">
                            <div class="task-title">
                                {priority_colors.get(priority, '📌')} {title}
                            </div>
                            <div class="task-description">
                                {description[:100]}{'...' if len(description) > 100 else ''}
                            </div>
                            <div class="task-meta">
                                {status_color} {status} | Priority: {priority}<br>
                                Created: {created_at.strftime('%Y-%m-%d %H:%M') if hasattr(created_at, 'strftime') else str(created_at)}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    
    # Add Task View
    elif selected == "Add Task":
        st.markdown("## ✨ Create New Task")
        
        with st.form("add_task_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("📝 Task Title", placeholder="Enter a descriptive title...")
                priority = st.selectbox("🎯 Priority Level", ["High", "Medium", "Low"])
            
            with col2:
                due_date = st.date_input("📅 Due Date", value=datetime.now().date())
            
            description = st.text_area("📄 Description", placeholder="Provide more details about this task...", height=100)
            
            submitted = st.form_submit_button("✨ Create Task", use_container_width=True)
            
            if submitted and title:
                add_task(title, description, priority, due_date)
                st.success("✅ Task created successfully!")
                st.balloons()
            elif submitted and not title:
                st.error("❌ Please enter a task title!")
    
    # View Tasks View
    elif selected == "View Tasks":
        st.markdown("## 📋 All Tasks")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Completed"])
        with col2:
            priority_filter = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
        
        tasks = get_all_tasks()
        
        # Apply filters
        if status_filter != "All":
            tasks = [t for t in tasks if t.get('status', 'Pending') == status_filter]
        if priority_filter != "All":
            tasks = [t for t in tasks if t.get('priority', 'Medium') == priority_filter]
        
        if not tasks:
            st.info("No tasks found matching the filters.")
        else:
            for task in tasks:
                # Ensure all tasks have required fields
                task_status = task.get('status', 'Pending')
                task_title = task.get('title', 'Untitled')
                task_description = task.get('description', '')
                task_priority = task.get('priority', 'Medium')
                task_id = str(task['_id'])
                
                with st.expander(f"📌 {task_title} - {task_status}"):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.write(f"**Description:** {task_description}")
                        st.write(f"**Priority:** {task_priority}")
                        if task.get('due_date'):
                            due_date_value = task['due_date']
                            if isinstance(due_date_value, datetime):
                                due_date_value = due_date_value.strftime('%Y-%m-%d')
                            st.write(f"**Due Date:** {due_date_value}")
                        created_at = task.get('created_at', datetime.now())
                        st.write(f"**Created:** {created_at.strftime('%Y-%m-%d %H:%M') if hasattr(created_at, 'strftime') else str(created_at)}")
                    
                    with col2:
                        # Status toggle
                        new_status = "Completed" if task_status == "Pending" else "Pending"
                        if st.button(f"Mark as {new_status}", key=f"status_{task_id}"):
                            update_task_status(task_id, new_status)
                            st.rerun()
                    
                    with col3:
                        # Edit button
                        if st.button("✏️ Edit", key=f"edit_{task_id}"):
                            st.session_state['editing_task'] = task_id
                            st.rerun()
                    
                    # Delete button
                    if st.button("🗑️ Delete", key=f"delete_{task_id}"):
                        if delete_task(task_id):
                            st.success("Task deleted!")
                            st.rerun()
            
            # Edit Modal
            if 'editing_task' in st.session_state:
                task_id = st.session_state['editing_task']
                task = task_collection.find_one({"_id": ObjectId(task_id)})
                
                if task:
                    with st.form("edit_task_form"):
                        st.markdown("### ✏️ Edit Task")
                        edit_title = st.text_input("Title", value=task.get('title', ''))
                        edit_description = st.text_area("Description", value=task.get('description', ''))
                        edit_priority = st.selectbox("Priority", ["High", "Medium", "Low"], 
                                                    index=["High", "Medium", "Low"].index(task.get('priority', 'Medium')))
                        edit_due_date_value = task.get('due_date')
                        if isinstance(edit_due_date_value, datetime):
                            edit_due_date_value = edit_due_date_value.date()
                        elif isinstance(edit_due_date_value, str):
                            try:
                                edit_due_date_value = date.fromisoformat(edit_due_date_value)
                            except ValueError:
                                edit_due_date_value = datetime.now().date()
                        elif edit_due_date_value is None:
                            edit_due_date_value = datetime.now().date()
                        edit_due_date = st.date_input("Due Date", value=edit_due_date_value)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("💾 Save Changes"):
                                update_task(task_id, edit_title, edit_description, edit_priority, edit_due_date)
                                del st.session_state['editing_task']
                                st.success("Task updated!")
                                st.rerun()
                        with col2:
                            if st.form_submit_button("❌ Cancel"):
                                del st.session_state['editing_task']
                                st.rerun()
    
    # Search View
    elif selected == "Search":
        st.markdown("## 🔍 Search Tasks")
        
        search_term = st.text_input("Enter keyword to search", placeholder="Search by title or description...")
        
        if search_term:
            results = search_tasks(search_term)
            
            if results:
                st.success(f"Found {len(results)} task(s)")
                for task in results:
                    with st.container():
                        st.markdown(f"""
                        <div class="task-card">
                            <div class="task-title">{task.get('title', 'Untitled')}</div>
                            <div class="task-description">{task.get('description', '')}</div>
                            <div class="task-meta">
                                Status: {task.get('status', 'Pending')} | Priority: {task.get('priority', 'Medium')}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("No tasks found matching your search.")
    
    # Statistics View
    elif selected == "Statistics":
        st.markdown("## 📊 Task Analytics")
        
        stats = get_task_stats()
        tasks = get_all_tasks()
        
        # Stats Cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{stats['total']}</div>
                <div class="stat-label">Total Tasks</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{stats['pending']}</div>
                <div class="stat-label">Pending Tasks</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{stats['completed']}</div>
                <div class="stat-label">Completed Tasks</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            completion_rate = (stats['completed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{completion_rate:.1f}%</div>
                <div class="stat-label">Completion Rate</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Priority Distribution")
            if px is not None:
                priority_data = pd.DataFrame({
                    'Priority': list(stats['priority'].keys()),
                    'Count': list(stats['priority'].values())
                })
                fig = px.pie(priority_data, values='Count', names='Priority', 
                            color='Priority', color_discrete_map={'High':'#ef4444', 'Medium':'#f59e0b', 'Low':'#10b981'})
                fig.update_layout(background_color='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Plotly is unavailable. Install plotly to view charts.")
        
        with col2:
            st.markdown("### Status Overview")
            if px is not None:
                status_data = pd.DataFrame({
                    'Status': ['Pending', 'Completed'],
                    'Count': [stats['pending'], stats['completed']]
                })
                fig = px.bar(status_data, x='Status', y='Count', 
                            color='Status', color_discrete_map={'Pending':'#f59e0b', 'Completed':'#10b981'})
                fig.update_layout(background_color='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Plotly is unavailable. Install plotly to view charts.")
        
        # Recent Activity
        st.markdown("### 📅 Recent Activity")
        recent_tasks = tasks[:10]
        if recent_tasks:
            activity_data = []
            for task in recent_tasks:
                created_at = task.get('created_at', datetime.now())
                activity_data.append({
                    'Task': task.get('title', 'Untitled')[:30],
                    'Created': created_at.strftime('%Y-%m-%d') if hasattr(created_at, 'strftime') else str(created_at),
                    'Status': task.get('status', 'Pending')
                })
            activity_df = pd.DataFrame(activity_data)
            st.dataframe(activity_df, use_container_width=True, hide_index=True)

# ==========================
# Run the Application
# ==========================
if __name__ == "__main__":
    main()