import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="Healthcare Finance Innovation Suite",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'change_requests' not in st.session_state:
    st.session_state.change_requests = []
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f4788;
        text-align: center;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-top: 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stAlert {
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🏥 Healthcare Finance Innovation Suite</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Professional Financial Intelligence Platform for Hospital Systems</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🧭 Navigation")
    selected_feature = st.selectbox(
        "Select Feature",
        [
            "Executive Dashboard",
            "Real-Time Integration Hub",
            "Interactive Forecasting",
            "AI Variance Analysis",
            "Performance Scorecard",
            "Equity Budget Modeling",
            "Change Requests",
            "Strategic Initiatives"
        ]
    )
    
    st.markdown("---")
    st.markdown("### 📁 Data Upload")
    st.markdown("Upload your CSV files:")
    
    # File uploaders
    uploaded_files = {
        'budget': st.file_uploader("Budget & Actuals", type=['csv'], key="budget_upload"),
        'clinical': st.file_uploader("Clinical Data", type=['csv'], key="clinical_upload"),
        'payer': st.file_uploader("Payer Mix", type=['csv'], key="payer_upload"),
        'staffing': st.file_uploader("Staffing Data", type=['csv'], key="staffing_upload"),
        'equity': st.file_uploader("Equity Data", type=['csv'], key="equity_upload"),
        'strategic': st.file_uploader("Strategic Initiatives", type=['csv'], key="strategic_upload")
    }

# Data loading function - NOT cached to ensure fresh reads
def load_all_data(uploaded_files):
    """Load data from uploaded files or create sample data"""
    data = {}
    
    # Budget data
    if uploaded_files['budget'] is not None:
        try:
            df = pd.read_csv(uploaded_files['budget'])
            df['month'] = pd.to_datetime(df['month'])
            data['budget'] = df
            st.sidebar.success("✅ Budget data loaded successfully")
        except Exception as e:
            st.sidebar.error(f"❌ Error loading budget data: {str(e)}")
            data['budget'] = create_sample_budget_data()
    else:
        data['budget'] = create_sample_budget_data()
    
    # Clinical data
    if uploaded_files['clinical'] is not None:
        try:
            df = pd.read_csv(uploaded_files['clinical'])
            df['month'] = pd.to_datetime(df['month'])
            data['clinical'] = df
            st.sidebar.success("✅ Clinical data loaded successfully")
        except Exception as e:
            st.sidebar.error(f"❌ Error loading clinical data: {str(e)}")
            data['clinical'] = create_sample_clinical_data()
    else:
        data['clinical'] = create_sample_clinical_data()
    
    # Payer data
    if uploaded_files['payer'] is not None:
        try:
            df = pd.read_csv(uploaded_files['payer'])
            df['month'] = pd.to_datetime(df['month'])
            data['payer'] = df
            st.sidebar.success("✅ Payer data loaded successfully")
        except Exception as e:
            st.sidebar.error(f"❌ Error loading payer data: {str(e)}")
            data['payer'] = create_sample_payer_data()
    else:
        data['payer'] = create_sample_payer_data()
    
    # Staffing data
    if uploaded_files['staffing'] is not None:
        try:
            df = pd.read_csv(uploaded_files['staffing'])
            df['month'] = pd.to_datetime(df['month'])
            data['staffing'] = df
            st.sidebar.success("✅ Staffing data loaded successfully")
        except Exception as e:
            st.sidebar.error(f"❌ Error loading staffing data: {str(e)}")
            data['staffing'] = create_sample_staffing_data()
    else:
        data['staffing'] = create_sample_staffing_data()
    
    # Equity data
    if uploaded_files['equity'] is not None:
        try:
            df = pd.read_csv(uploaded_files['equity'])
            data['equity'] = df
            st.sidebar.success("✅ Equity data loaded successfully")
        except Exception as e:
            st.sidebar.error(f"❌ Error loading equity data: {str(e)}")
            data['equity'] = create_sample_equity_data()
    else:
        data['equity'] = create_sample_equity_data()
    
    # Strategic data
    if uploaded_files['strategic'] is not None:
        try:
            df = pd.read_csv(uploaded_files['strategic'])
            df['start_date'] = pd.to_datetime(df['start_date'])
            df['target_completion'] = pd.to_datetime(df['target_completion'])
            data['strategic'] = df
            st.sidebar.success("✅ Strategic data loaded successfully")
        except Exception as e:
            st.sidebar.error(f"❌ Error loading strategic data: {str(e)}")
            data['strategic'] = create_sample_strategic_data()
    else:
        data['strategic'] = create_sample_strategic_data()
    
    return data

# Sample data creation functions
def create_sample_budget_data():
    """Create sample budget data for demonstration"""
    departments = ['Cardiology', 'Primary Care', 'Gastroenterology', 'Orthopedics']
    months = pd.date_range('2024-01-01', periods=6, freq='M')
    gl_codes = {
        '610001': 'Salaries',
        '620001': 'Medical Supplies',
        '630001': 'IT Costs',
        '640001': 'Facility Costs'
    }
    
    data = []
    for dept in departments:
        base_amounts = {
            'Cardiology': {'Salaries': 450000, 'Medical Supplies': 75000, 'IT Costs': 15000, 'Facility Costs': 25000},
            'Primary Care': {'Salaries': 380000, 'Medical Supplies': 45000, 'IT Costs': 12000, 'Facility Costs': 20000},
            'Gastroenterology': {'Salaries': 420000, 'Medical Supplies': 65000, 'IT Costs': 14000, 'Facility Costs': 23000},
            'Orthopedics': {'Salaries': 480000, 'Medical Supplies': 85000, 'IT Costs': 16000, 'Facility Costs': 28000}
        }
        
        for i, month in enumerate(months):
            seasonal_factor = 1 + 0.1 * np.sin(i * np.pi / 6)
            
            for gl_code, description in gl_codes.items():
                base_amount = base_amounts[dept][description]
                
                if description == 'Salaries':
                    actual_variance = np.random.uniform(0.98, 1.05)
                elif description == 'Medical Supplies':
                    actual_variance = np.random.uniform(0.85, 1.15) * seasonal_factor
                else:
                    actual_variance = np.random.uniform(0.95, 1.05)
                
                data.append({
                    'month': month,
                    'department': dept,
                    'cost_center': f'CC-{departments.index(dept)+1}00',
                    'gl_code': gl_code,
                    'gl_description': description,
                    'budget_amount': base_amount,
                    'actual_amount': base_amount * actual_variance,
                    'fte_budget': np.random.uniform(10, 15) if gl_code == '610001' else 0,
                    'fte_actual': np.random.uniform(9, 16) if gl_code == '610001' else 0
                })
    
    return pd.DataFrame(data)

def create_sample_clinical_data():
    """Create sample clinical data"""
    departments = ['Cardiology', 'Primary Care', 'Gastroenterology', 'Orthopedics']
    months = pd.date_range('2024-01-01', periods=6, freq='M')
    
    base_visits = {
        'Cardiology': 1200,
        'Primary Care': 2800,
        'Gastroenterology': 900,
        'Orthopedics': 1100
    }
    
    data = []
    for dept in departments:
        for i, month in enumerate(months):
            seasonal_factor = 1 + 0.15 * np.sin(i * np.pi / 6)
            visits_budget = base_visits[dept]
            
            data.append({
                'month': month,
                'department': dept,
                'visits_actual': int(visits_budget * seasonal_factor * np.random.uniform(0.9, 1.1)),
                'visits_budget': visits_budget,
                'no_show_rate': np.random.uniform(0.05, 0.15),
                'avg_wait_days': np.random.uniform(1, 5),
                'patient_satisfaction': np.random.uniform(80, 95),
                'provider_wrvus': np.random.uniform(3000, 5000)
            })
    
    return pd.DataFrame(data)

def create_sample_payer_data():
    """Create sample payer mix data"""
    departments = ['Cardiology', 'Primary Care', 'Gastroenterology', 'Orthopedics']
    months = pd.date_range('2024-01-01', periods=6, freq='M')
    
    data = []
    for dept in departments:
        base_commercial = {
            'Cardiology': 0.45,
            'Primary Care': 0.35,
            'Gastroenterology': 0.40,
            'Orthopedics': 0.50
        }
        
        for month in months:
            commercial = base_commercial[dept] + np.random.uniform(-0.05, 0.05)
            medicare = 0.30 + np.random.uniform(-0.05, 0.05)
            medicaid = 0.15 + np.random.uniform(-0.05, 0.05)
            self_pay = max(0, 1 - commercial - medicare - medicaid)
            
            data.append({
                'month': month,
                'department': dept,
                'commercial_pct': commercial,
                'medicare_pct': medicare,
                'medicaid_pct': medicaid,
                'self_pay_pct': self_pay,
                'avg_reimbursement': 150 + (commercial * 100) - (medicaid * 50)
            })
    
    return pd.DataFrame(data)

def create_sample_staffing_data():
    """Create sample staffing data"""
    departments = ['Cardiology', 'Primary Care', 'Gastroenterology', 'Orthopedics']
    months = pd.date_range('2024-01-01', periods=6, freq='M')
    
    base_staffing = {
        'Cardiology': {'provider': 4.0, 'rn': 3.5, 'ma': 4.0, 'admin': 1.5},
        'Primary Care': {'provider': 3.0, 'rn': 2.5, 'ma': 5.0, 'admin': 2.0},
        'Gastroenterology': {'provider': 3.5, 'rn': 3.0, 'ma': 3.5, 'admin': 1.5},
        'Orthopedics': {'provider': 4.5, 'rn': 4.0, 'ma': 4.5, 'admin': 2.0}
    }
    
    data = []
    for dept in departments:
        for i, month in enumerate(months):
            overtime_factor = 1.5 if i in [0, 1, 11] else 1.0
            
            data.append({
                'month': month,
                'department': dept,
                'provider_fte': base_staffing[dept]['provider'] + np.random.uniform(-0.2, 0.2),
                'rn_fte': base_staffing[dept]['rn'] + np.random.uniform(-0.3, 0.3),
                'ma_fte': base_staffing[dept]['ma'] + np.random.uniform(-0.5, 0.5),
                'admin_fte': base_staffing[dept]['admin'],
                'overtime_hours': np.random.uniform(50, 150) * overtime_factor,
                'overtime_cost': np.random.uniform(2000, 6000) * overtime_factor
            })
    
    return pd.DataFrame(data)

def create_sample_equity_data():
    """Create sample equity data"""
    departments = ['Cardiology', 'Primary Care', 'Gastroenterology', 'Orthopedics']
    zip_codes = ['29401', '29403', '29405', '29407']
    
    equity_profiles = {
        'Cardiology': {'svi': 0.45, 'medicaid': 0.25, 'transit': 0.7, 'language': 0.10, 'complexity': 0.30},
        'Primary Care': {'svi': 0.75, 'medicaid': 0.45, 'transit': 0.4, 'language': 0.20, 'complexity': 0.25},
        'Gastroenterology': {'svi': 0.55, 'medicaid': 0.30, 'transit': 0.6, 'language': 0.15, 'complexity': 0.35},
        'Orthopedics': {'svi': 0.35, 'medicaid': 0.20, 'transit': 0.8, 'language': 0.08, 'complexity': 0.40}
    }
    
    data = []
    for i, dept in enumerate(departments):
        profile = equity_profiles[dept]
        data.append({
            'department': dept,
            'zip_code': zip_codes[i],
            'svi_score': profile['svi'],
            'medicaid_pct': profile['medicaid'],
            'transit_score': profile['transit'],
            'language_barrier_pct': profile['language'],
            'complexity_tier_3_pct': profile['complexity']
        })
    
    return pd.DataFrame(data)

def create_sample_strategic_data():
    """Create sample strategic initiatives data"""
    initiatives = [
        {
            'initiative_id': 'SI-001',
            'initiative_name': 'New GI Suite',
            'department': 'Gastroenterology',
            'status': 'Active',
            'phase': 'Planning',
            'start_date': '2024-01-15',
            'target_completion': '2024-12-01',
            'capex_budget': 500000,
            'opex_budget': 180000,
            'projected_monthly_revenue': 75000
        },
        {
            'initiative_id': 'SI-002',
            'initiative_name': 'Telehealth Expansion',
            'department': 'Primary Care',
            'status': 'Active',
            'phase': 'Implementation',
            'start_date': '2024-02-01',
            'target_completion': '2024-06-30',
            'capex_budget': 50000,
            'opex_budget': 120000,
            'projected_monthly_revenue': 45000
        },
        {
            'initiative_id': 'SI-003',
            'initiative_name': 'Cardiac Cath Lab Upgrade',
            'department': 'Cardiology',
            'status': 'Active',
            'phase': 'Procurement',
            'start_date': '2024-03-01',
            'target_completion': '2024-09-30',
            'capex_budget': 1200000,
            'opex_budget': 240000,
            'projected_monthly_revenue': 150000
        },
        {
            'initiative_id': 'SI-004',
            'initiative_name': 'Orthopedic Robotics Program',
            'department': 'Orthopedics',
            'status': 'Planning',
            'phase': 'Feasibility',
            'start_date': '2024-04-01',
            'target_completion': '2025-03-31',
            'capex_budget': 2000000,
            'opex_budget': 400000,
            'projected_monthly_revenue': 200000
        }
    ]
    
    return pd.DataFrame(initiatives)

# Load data - this runs every time to ensure fresh data
data = load_all_data(uploaded_files)

# Show data status
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📊 Data Status")
    
    # Check which files were uploaded
    uploaded_count = sum(1 for f in uploaded_files.values() if f is not None)
    
    if uploaded_count > 0:
        st.success(f"✅ {uploaded_count}/6 data files uploaded")
        st.session_state.data_loaded = True
        
        # Show data preview
        if st.checkbox("Show Data Preview"):
            for name, file in uploaded_files.items():
                if file is not None:
                    st.markdown(f"**{name.title()} Data:**")
                    st.dataframe(data[name].head(3), use_container_width=True)
    else:
        st.info("ℹ️ Using sample data (upload files to use real data)")
        st.session_state.data_loaded = False

# Constants
BUDGET_VARIANCE_THRESHOLD = 0.05
OVERTIME_THRESHOLD = 0.10
NO_SHOW_THRESHOLD = 0.10
# Main content based on selected feature
if selected_feature == "Executive Dashboard":
    st.markdown("## 📊 Executive Dashboard")
    st.markdown("Real-time overview of key financial and operational metrics")
    
    # Data source indicator
    if st.session_state.data_loaded:
        st.success("📁 Using uploaded data files")
    else:
        st.info("📁 Using sample demonstration data")
    
    # Get latest data
    budget_data = data['budget']
    clinical_data = data['clinical']
    
    # Latest month
    latest_month = budget_data['month'].max()
    current_budget = budget_data[budget_data['month'] == latest_month]
    current_clinical = clinical_data[clinical_data['month'] == latest_month]
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_budget = current_budget['budget_amount'].sum()
        total_actual = current_budget['actual_amount'].sum()
        variance_pct = ((total_actual - total_budget) / total_budget) * 100 if total_budget > 0 else 0
        
        st.metric(
            "Budget Variance",
            f"{variance_pct:+.1f}%",
            f"${total_actual - total_budget:,.0f}",
            delta_color="inverse"
        )
    
    with col2:
        total_visits_actual = current_clinical['visits_actual'].sum()
        total_visits_budget = current_clinical['visits_budget'].sum()
        visit_variance = ((total_visits_actual - total_visits_budget) / total_visits_budget) * 100 if total_visits_budget > 0 else 0
        
        st.metric(
            "Visit Volume",
            f"{total_visits_actual:,}",
            f"{visit_variance:+.1f}% vs target"
        )
    
    with col3:
        avg_satisfaction = current_clinical['patient_satisfaction'].mean()
        # Calculate trend
        if len(clinical_data['month'].unique()) > 1:
            prev_month = sorted(clinical_data['month'].unique())[-2]
            prev_satisfaction = clinical_data[clinical_data['month'] == prev_month]['patient_satisfaction'].mean()
            satisfaction_delta = avg_satisfaction - prev_satisfaction
        else:
            satisfaction_delta = 0
        
        st.metric(
            "Patient Satisfaction",
            f"{avg_satisfaction:.1f}%",
            f"{satisfaction_delta:+.1f}%"
        )
    
    with col4:
        avg_wait = current_clinical['avg_wait_days'].mean()
        # Calculate trend
        if len(clinical_data['month'].unique()) > 1:
            prev_month = sorted(clinical_data['month'].unique())[-2]
            prev_wait = clinical_data[clinical_data['month'] == prev_month]['avg_wait_days'].mean()
            wait_delta = avg_wait - prev_wait
        else:
            wait_delta = 0
        
        st.metric(
            "Avg Wait Time",
            f"{avg_wait:.1f} days",
            f"{wait_delta:+.1f} days",
            delta_color="inverse"
        )
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Department Performance")
        
        dept_summary = current_budget.groupby('department').agg({
            'budget_amount': 'sum',
            'actual_amount': 'sum'
        }).reset_index()
        
        dept_summary['variance_pct'] = ((dept_summary['actual_amount'] - dept_summary['budget_amount']) / 
                                        dept_summary['budget_amount']) * 100
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Budget',
            x=dept_summary['department'],
            y=dept_summary['budget_amount'],
            text=[f'${x:,.0f}' for x in dept_summary['budget_amount']],
            textposition='auto',
        ))
        fig.add_trace(go.Bar(
            name='Actual',
            x=dept_summary['department'],
            y=dept_summary['actual_amount'],
            text=[f'${x:,.0f}' for x in dept_summary['actual_amount']],
            textposition='auto',
        ))
        
        fig.update_layout(
            barmode='group',
            yaxis_title="Amount ($)",
            xaxis_title="Department",
            showlegend=True,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Monthly Trend")
        
        monthly_trend = budget_data.groupby('month').agg({
            'budget_amount': 'sum',
            'actual_amount': 'sum'
        }).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly_trend['month'],
            y=monthly_trend['budget_amount'],
            mode='lines+markers',
            name='Budget',
            line=dict(color='blue', dash='dash')
        ))
        fig.add_trace(go.Scatter(
            x=monthly_trend['month'],
            y=monthly_trend['actual_amount'],
            mode='lines+markers',
            name='Actual',
            line=dict(color='red')
        ))
        
        fig.update_layout(
            yaxis_title="Amount ($)",
            xaxis_title="Month",
            showlegend=True,
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Key Insights
    st.markdown("### Key Insights")
    
    total_ytd_budget = budget_data['budget_amount'].sum()
    total_ytd_actual = budget_data['actual_amount'].sum()
    ytd_variance = ((total_ytd_actual - total_ytd_budget) / total_ytd_budget) * 100 if total_ytd_budget > 0 else 0
    
    # Find department with highest variance
    if not dept_summary.empty:
        dept_variances = dept_summary.set_index('department')['variance_pct']
        worst_dept = dept_variances.abs().idxmax()
        worst_variance = dept_variances[worst_dept]
    else:
        worst_dept = "N/A"
        worst_variance = 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"""
        **YTD Performance**
        - Total Budget: ${total_ytd_budget:,.0f}
        - Total Actual: ${total_ytd_actual:,.0f}
        - Variance: {ytd_variance:+.1f}%
        """)
    
    with col2:
        st.warning(f"""
        **Attention Required**
        - {worst_dept}: {worst_variance:+.1f}% variance
        - Review cost drivers
        - Consider corrective action
        """)
    
    with col3:
        avg_no_show = current_clinical['no_show_rate'].mean()
        st.success(f"""
        **Operational Metrics**
        - Avg No-Show Rate: {avg_no_show:.1%}
        - Total Monthly Visits: {total_visits_actual:,}
        - Utilization: {(total_visits_actual/total_visits_budget)*100:.1f}%
        """)

elif selected_feature == "Real-Time Integration Hub":
    st.markdown("## 🔄 Real-Time Finance + Clinical Integration Hub")
    st.markdown("Automated variance detection and root cause analysis")
    
    # Department selector
    selected_dept = st.selectbox("Select Department", data['budget']['department'].unique())
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_month = st.date_input("Start Month", value=data['budget']['month'].min())
    with col2:
        end_month = st.date_input("End Month", value=data['budget']['month'].max())
    
    # Filter data
    dept_budget = data['budget'][
        (data['budget']['department'] == selected_dept) & 
        (data['budget']['month'] >= pd.to_datetime(start_month)) &
        (data['budget']['month'] <= pd.to_datetime(end_month))
    ]
    dept_clinical = data['clinical'][
        (data['clinical']['department'] == selected_dept) &
        (data['clinical']['month'] >= pd.to_datetime(start_month)) &
        (data['clinical']['month'] <= pd.to_datetime(end_month))
    ]
    dept_staffing = data['staffing'][
        (data['staffing']['department'] == selected_dept) &
        (data['staffing']['month'] >= pd.to_datetime(start_month)) &
        (data['staffing']['month'] <= pd.to_datetime(end_month))
    ]
    
    if dept_budget.empty:
        st.warning("No data available for selected department and date range")
    else:
        # Calculate variance
        total_budget = dept_budget['budget_amount'].sum()
        total_actual = dept_budget['actual_amount'].sum()
        total_variance = total_actual - total_budget
        variance_pct = (total_variance / total_budget) * 100 if total_budget > 0 else 0
        
        # Variance alert
        if abs(variance_pct) > BUDGET_VARIANCE_THRESHOLD * 100:
            st.error(f"⚠️ {selected_dept} is {variance_pct:+.1f}% {'over' if variance_pct > 0 else 'under'} budget (${total_variance:+,.0f})")
        else:
            st.success(f"✅ {selected_dept} is within budget tolerance ({variance_pct:+.1f}%)")
        
        # Analysis columns
        col1, col2, col3 = st.columns([1.5, 1.5, 1])
        
        with col1:
            st.markdown("### Variance Drivers")
            
            # GL variance analysis
            gl_variance = dept_budget.groupby('gl_description').agg({
                'budget_amount': 'sum',
                'actual_amount': 'sum'
            }).reset_index()
            
            gl_variance['variance'] = gl_variance['actual_amount'] - gl_variance['budget_amount']
            gl_variance['variance_pct'] = (gl_variance['variance'] / gl_variance['budget_amount'] * 100).fillna(0)
            
            # Create bar chart
            fig = px.bar(
                gl_variance.sort_values('variance'),
                y='gl_description',
                x='variance',
                orientation='h',
                title="Variance by Category ($)",
                color='variance',
                color_continuous_scale=['red', 'yellow', 'green'],
                color_continuous_midpoint=0,
                text=[f'${x:,.0f}' for x in gl_variance.sort_values('variance')['variance']]
            )
            fig.update_traces(textposition='auto')
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Clinical Metrics Impact")
            
            if not dept_clinical.empty:
                # Merge data for correlation
                monthly_metrics = dept_budget.groupby('month')['actual_amount'].sum().reset_index()
                monthly_clinical = dept_clinical.groupby('month').agg({
                    'visits_actual': 'sum',
                    'no_show_rate': 'mean'
                }).reset_index()
                
                monthly_data = pd.merge(monthly_metrics, monthly_clinical, on='month', how='inner')
                
                if not monthly_data.empty:
                    # Dual-axis chart
                    fig = go.Figure()
                    
                    fig.add_trace(go.Bar(
                        x=monthly_data['month'],
                        y=monthly_data['visits_actual'],
                        name='Visit Volume',
                        yaxis='y2',
                        opacity=0.5
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=monthly_data['month'],
                        y=monthly_data['actual_amount'],
                        mode='lines+markers',
                        name='Actual Cost',
                        yaxis='y',
                        line=dict(color='red', width=3)
                    ))
                    
                    fig.update_layout(
                        title="Cost vs Volume Correlation",
                        yaxis=dict(title="Cost ($)", side="left"),
                        yaxis2=dict(title="Visit Volume", side="right", overlaying='y'),
                        hovermode='x unified',
                        height=400,
                        showlegend=True
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No clinical data available for correlation")
            else:
                st.info("No clinical data available")
        
        with col3:
            st.markdown("### Root Cause Indicators")
            
            if not dept_staffing.empty and not dept_clinical.empty:
                # Get latest month data
                latest_month = dept_staffing['month'].max()
                latest_staffing = dept_staffing[dept_staffing['month'] == latest_month].iloc[0]
                latest_clinical = dept_clinical[dept_clinical['month'] == latest_month].iloc[0]
                
                # Calculate indicators
                total_fte = (latest_staffing['provider_fte'] + latest_staffing['rn_fte'] + 
                            latest_staffing['ma_fte'] + latest_staffing['admin_fte'])
                overtime_ratio = (latest_staffing['overtime_hours'] / (total_fte * 160) * 100) if total_fte > 0 else 0
                
                st.metric("Overtime %", f"{overtime_ratio:.1f}%", 
                         "High" if overtime_ratio > 10 else "Normal")
                
                st.metric("No-Show Rate", f"{latest_clinical['no_show_rate']:.1%}",
                         "Above Target" if latest_clinical['no_show_rate'] > 0.10 else "On Target")
                
                visit_achievement = (latest_clinical['visits_actual'] / latest_clinical['visits_budget']) * 100 if latest_clinical['visits_budget'] > 0 else 0
                st.metric("Visit Achievement", f"{visit_achievement:.1f}%",
                         f"{visit_achievement - 100:+.1f}%")
                
                # Insights
                st.markdown("#### Key Findings")
                insights = []
                
                if overtime_ratio > 10:
                    insights.append(f"• High overtime ({overtime_ratio:.1f}%)")
                
                if latest_clinical['no_show_rate'] > 0.10:
                    insights.append(f"• No-show rate: {latest_clinical['no_show_rate']:.1%}")
                
                if visit_achievement < 95:
                    insights.append("• Visit volume below target")
                
                if insights:
                    for insight in insights:
                        st.write(insight)
                else:
                    st.success("No significant issues")
            else:
                st.info("Insufficient data for analysis")
        
        # Detailed variance table
        st.markdown("### Detailed Variance Analysis")
        
        if not gl_variance.empty:
            summary_df = gl_variance.copy()
            summary_df['Status'] = summary_df['variance_pct'].apply(
                lambda x: '🔴' if abs(x) > 10 else '🟡' if abs(x) > 5 else '🟢'
            )
            
            summary_df['Budget'] = summary_df['budget_amount'].apply(lambda x: f'${x:,.0f}')
            summary_df['Actual'] = summary_df['actual_amount'].apply(lambda x: f'${x:,.0f}')
            summary_df['Variance $'] = summary_df['variance'].apply(lambda x: f'${x:+,.0f}')
            summary_df['Variance %'] = summary_df['variance_pct'].apply(lambda x: f'{x:+.1f}%')
            
            st.dataframe(
                summary_df[['Status', 'gl_description', 'Budget', 'Actual', 'Variance $', 'Variance %']],
                use_container_width=True,
                hide_index=True
            )

elif selected_feature == "Interactive Forecasting":
    st.markdown("## 🎚️ Interactive Budget Forecasting")
    st.markdown("Adjust key drivers to see real-time impact on financial metrics")
    
    # Select department
    dept = st.selectbox("Select Department for Forecasting", data['budget']['department'].unique())
    
    # Get baseline data
    dept_budget = data['budget'][data['budget']['department'] == dept]
    dept_clinical = data['clinical'][data['clinical']['department'] == dept]
    dept_payer = data['payer'][data['payer']['department'] == dept]
    dept_staffing = data['staffing'][data['staffing']['department'] == dept]
    
    if dept_budget.empty or dept_clinical.empty or dept_payer.empty or dept_staffing.empty:
        st.warning("Insufficient data for forecasting. Please ensure all data files are uploaded.")
    else:
        # Calculate baselines
        baseline_monthly_cost = dept_budget.groupby('month')['actual_amount'].sum().mean()
        baseline_visits = dept_clinical['visits_actual'].mean()
        baseline_reimbursement = dept_payer['avg_reimbursement'].mean()
        
        # Total FTE calculation
        staffing_cols = ['provider_fte', 'rn_fte', 'ma_fte', 'admin_fte']
        baseline_fte = dept_staffing[staffing_cols].sum(axis=1).mean()
        
        # Display baselines
        st.markdown("### Current Baseline Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.info(f"**Monthly Cost**\n${baseline_monthly_cost:,.0f}")
        with col2:
            st.info(f"**Avg Monthly Visits**\n{baseline_visits:,.0f}")
        with col3:
            st.info(f"**Avg Reimbursement**\n${baseline_reimbursement:,.2f}")
        with col4:
            st.info(f"**Total FTEs**\n{baseline_fte:.1f}")
        
        st.markdown("---")
        
        # Interactive sliders
        st.markdown("### Adjust Forecast Drivers")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Volume & Efficiency")
            volume_change = st.slider(
                "Patient Volume Change (%)",
                min_value=-20,
                max_value=20,
                value=0,
                help="Adjust expected patient volume"
            )
            
            productivity_change = st.slider(
                "Provider Productivity Change (%)",
                min_value=-10,
                max_value=10,
                value=0,
                help="Change in provider efficiency"
            )
            
            no_show_change = st.slider(
                "No-Show Rate Change (pp)",
                min_value=-5,
                max_value=5,
                value=0,
                help="Percentage point change in no-show rate"
            )
        
        with col2:
            st.markdown("#### Financial Drivers")
            payer_mix_shift = st.slider(
                "Commercial Payer Mix Change (pp)",
                min_value=-10,
                max_value=10,
                value=0,
                help="Percentage point change in commercial payer mix"
            )
            
            supply_inflation = st.slider(
                "Supply Cost Inflation (%)",
                min_value=0,
                max_value=15,
                value=3,
                help="Expected supply cost inflation"
            )
            
            wage_increase = st.slider(
                "Wage Increase (%)",
                min_value=0,
                max_value=10,
                value=3,
                help="Annual wage increase percentage"
            )
        
        st.markdown("#### Staffing Changes")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            provider_fte_change = st.number_input(
                "Provider FTE Change",
                min_value=-2.0,
                max_value=5.0,
                value=0.0,
                step=0.5
            )
        
        with col2:
            rn_fte_change = st.number_input(
                "RN FTE Change",
                min_value=-2.0,
                max_value=5.0,
                value=0.0,
                step=0.5
            )
        
        with col3:
            ma_fte_change = st.number_input(
                "MA FTE Change",
                min_value=-2.0,
                max_value=5.0,
                value=0.0,
                step=0.5
            )
        
        with col4:
            admin_fte_change = st.number_input(
                "Admin FTE Change",
                min_value=-2.0,
                max_value=5.0,
                value=0.0,
                step=0.5
            )
        
        # Calculate forecast
        st.markdown("### 📊 Forecast Results")
        
        # Revenue calculation
        effective_visits = baseline_visits * (1 + volume_change/100) * (1 + productivity_change/100) * (1 - no_show_change/100)
        new_reimbursement = baseline_reimbursement * (1 + payer_mix_shift * 0.02)
        forecast_monthly_revenue = effective_visits * new_reimbursement
        
        # Cost calculation
        salary_portion = baseline_monthly_cost * 0.60
        supply_portion = baseline_monthly_cost * 0.20
        other_portion = baseline_monthly_cost * 0.20
        
        # FTE costs
        provider_cost = 20000
        rn_cost = 8000
        ma_cost = 4500
        admin_cost = 4000
        
        fte_cost_change = (
            provider_fte_change * provider_cost +
            rn_fte_change * rn_cost +
            ma_fte_change * ma_cost +
            admin_fte_change * admin_cost
        )
        
        new_salary = salary_portion * (1 + wage_increase/100) + fte_cost_change
        new_supplies = supply_portion * (1 + supply_inflation/100) * (1 + volume_change/100)
        new_other = other_portion * (1 + volume_change/100 * 0.5)
        
        forecast_monthly_cost = new_salary + new_supplies + new_other
        
        # Margins
        forecast_margin = forecast_monthly_revenue - forecast_monthly_cost
        baseline_margin = (baseline_visits * baseline_reimbursement) - baseline_monthly_cost
        
        # Display results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            revenue_delta = forecast_monthly_revenue - (baseline_visits * baseline_reimbursement)
            revenue_pct_change = (revenue_delta / (baseline_visits * baseline_reimbursement)) * 100 if baseline_visits * baseline_reimbursement > 0 else 0
            st.metric(
                "Projected Monthly Revenue",
                f"${forecast_monthly_revenue:,.0f}",
                f"{revenue_pct_change:+.1f}% (${revenue_delta:+,.0f})"
            )
        
        with col2:
            cost_delta = forecast_monthly_cost - baseline_monthly_cost
            cost_pct_change = (cost_delta / baseline_monthly_cost) * 100 if baseline_monthly_cost > 0 else 0
            st.metric(
                "Projected Monthly Cost",
                f"${forecast_monthly_cost:,.0f}",
                f"{cost_pct_change:+.1f}% (${cost_delta:+,.0f})"
            )
        
        with col3:
            margin_delta = forecast_margin - baseline_margin
            st.metric(
                "Projected Net Margin",
                f"${forecast_margin:,.0f}",
                f"${margin_delta:+,.0f}"
            )
        
        # Additional KPIs
        st.markdown("#### Key Performance Indicators")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            cost_per_visit = forecast_monthly_cost / effective_visits if effective_visits > 0 else 0
            baseline_cost_per_visit = baseline_monthly_cost / baseline_visits if baseline_visits > 0 else 0
            st.metric(
                "Cost per Visit",
                f"${cost_per_visit:.2f}",
                f"${cost_per_visit - baseline_cost_per_visit:+.2f}"
            )
        
        with col2:
            new_total_fte = baseline_fte + provider_fte_change + rn_fte_change + ma_fte_change + admin_fte_change
            fte_per_1000 = (new_total_fte / effective_visits) * 1000 if effective_visits > 0 else 0
            baseline_fte_per_1000 = (baseline_fte / baseline_visits * 1000) if baseline_visits > 0 else 0
            st.metric(
                "FTE per 1,000 Visits",
                f"{fte_per_1000:.2f}",
                f"{fte_per_1000 - baseline_fte_per_1000:+.2f}"
            )
        
        with col3:
            margin_percentage = (forecast_margin / forecast_monthly_revenue) * 100 if forecast_monthly_revenue > 0 else 0
            baseline_margin_pct = (baseline_margin / (baseline_visits * baseline_reimbursement)) * 100 if baseline_visits * baseline_reimbursement > 0 else 0
            st.metric(
                "Operating Margin %",
                f"{margin_percentage:.1f}%",
                f"{margin_percentage - baseline_margin_pct:+.1f}pp"
            )
        
        with col4:
            revenue_per_fte = forecast_monthly_revenue / new_total_fte if new_total_fte > 0 else 0
            baseline_revenue_per_fte = (baseline_visits * baseline_reimbursement) / baseline_fte if baseline_fte > 0 else 0
            change_pct = ((revenue_per_fte / baseline_revenue_per_fte) - 1) * 100 if baseline_revenue_per_fte > 0 else 0
            st.metric(
                "Revenue per FTE",
                f"${revenue_per_fte:,.0f}",
                f"{change_pct:+.1f}%"
            )
        
        # Visualization
        st.markdown("### 12-Month Forecast Projection")
        
        # Create projections
        months = pd.date_range(start=pd.Timestamp.now().normalize(), periods=12, freq='M')
        
        forecast_data = []
        for i, month in enumerate(months):
            seasonal_factor = 1 + 0.05 * np.sin(i * np.pi / 6)
            
            month_revenue = forecast_monthly_revenue * seasonal_factor
            month_cost = forecast_monthly_cost * seasonal_factor
            month_margin = month_revenue - month_cost
            
            forecast_data.append({
                'Month': month,
                'Revenue': month_revenue,
                'Cost': month_cost,
                'Margin': month_margin,
                'Baseline Revenue': baseline_visits * baseline_reimbursement,
                'Baseline Cost': baseline_monthly_cost,
                'Baseline Margin': baseline_margin
            })
        
        forecast_df = pd.DataFrame(forecast_data)
        
        # Create chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=forecast_df['Month'],
            y=forecast_df['Revenue'],
            mode='lines',
            name='Forecast Revenue',
            line=dict(color='green', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=forecast_df['Month'],
            y=forecast_df['Cost'],
            mode='lines',
            name='Forecast Cost',
            line=dict(color='red', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=forecast_df['Month'],
            y=forecast_df['Margin'],
            mode='lines',
            name='Forecast Margin',
            line=dict(color='blue', width=3),
            fill='tozeroy',
            fillcolor='rgba(0,100,255,0.1)'
        ))
        
        # Add baseline lines
        fig.add_hline(
            y=baseline_visits * baseline_reimbursement,
            line_dash="dash",
            line_color="lightgreen",
            annotation_text="Baseline Revenue"
        )
        
        fig.add_hline(
            y=baseline_monthly_cost,
            line_dash="dash",
            line_color="lightcoral",
            annotation_text="Baseline Cost"
        )
        
        fig.update_layout(
            title="Financial Forecast vs Baseline",
            yaxis_title="Amount ($)",
            xaxis_title="Month",
            hovermode='x unified',
            showlegend=True,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)

elif selected_feature == "AI Variance Analysis":
    st.markdown("## 🤖 AI-Powered Variance Analysis")
    st.markdown("Automated insights and explanations for budget variances")
    
    # Department selection
    dept = st.selectbox("Select Department for Analysis", data['budget']['department'].unique())
    
    # Month selection
    available_months = sorted(data['budget']['month'].unique())
    if available_months:
        selected_month = st.selectbox(
            "Select Month", 
            available_months,
            format_func=lambda x: x.strftime('%B %Y'),
            index=len(available_months)-1
        )
        
        # Get data
        dept_budget = data['budget'][
            (data['budget']['department'] == dept) & 
            (data['budget']['month'] == selected_month)
        ]
        
        if not dept_budget.empty:
            # Get context data
            dept_clinical = data['clinical'][
                (data['clinical']['department'] == dept) & 
                (data['clinical']['month'] == selected_month)
            ]
            dept_staffing = data['staffing'][
                (data['staffing']['department'] == dept) & 
                (data['staffing']['month'] == selected_month)
            ]
            
            # Calculate variances
            variances = []
            for _, row in dept_budget.iterrows():
                variance = row['actual_amount'] - row['budget_amount']
                variance_pct = (variance / row['budget_amount']) * 100 if row['budget_amount'] != 0 else 0
                
                variances.append({
                    'GL Code': row['gl_code'],
                    'GL Description': row['gl_description'],
                    'Budget': row['budget_amount'],
                    'Actual': row['actual_amount'],
                    'Variance $': variance,
                    'Variance %': variance_pct,
                    'Significant': abs(variance_pct) > 5
                })
            
            variance_df = pd.DataFrame(variances)
            
            # Overall status
            total_budget = variance_df['Budget'].sum()
            total_actual = variance_df['Actual'].sum()
            total_variance = total_actual - total_budget
            total_variance_pct = (total_variance / total_budget) * 100 if total_budget > 0 else 0
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                if abs(total_variance_pct) > 5:
                    st.error(f"### ⚠️ {dept} - {selected_month.strftime('%B %Y')}")
                    st.markdown(f"**Total Variance: {total_variance_pct:+.1f}% (${total_variance:+,.0f})**")
                else:
                    st.success(f"### ✅ {dept} - {selected_month.strftime('%B %Y')}")
                    st.markdown(f"**Total Variance: {total_variance_pct:+.1f}% (${total_variance:+,.0f})**")
            
            with col2:
                st.metric("Budget", f"${total_budget:,.0f}")
            
            with col3:
                st.metric("Actual", f"${total_actual:,.0f}")
            
            # Waterfall chart
            st.markdown("### Variance Breakdown by Category")
            
            fig = go.Figure(go.Waterfall(
                name="",
                orientation="v",
                measure=["absolute"] + ["relative"] * len(variance_df) + ["total"],
                x=["Budget"] + variance_df['GL Description'].tolist() + ["Actual"],
                textposition="outside",
                text=[f"${total_budget:,.0f}"] + 
                     [f"${v:+,.0f}" for v in variance_df['Variance $']] + 
                     [f"${total_actual:,.0f}"],
                y=[total_budget] + variance_df['Variance $'].tolist() + [0],
                connector={"line": {"color": "rgb(63, 63, 63)"}},
            ))
            
            fig.update_layout(
                title="Budget to Actual Waterfall",
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Significant variances
            significant_variances = variance_df[variance_df['Significant']].copy()
            
            if not significant_variances.empty:
                st.markdown("### 🔍 Significant Variances Detected")
                
                # Format display
                display_df = significant_variances.copy()
                display_df['Budget'] = display_df['Budget'].apply(lambda x: f'${x:,.0f}')
                display_df['Actual'] = display_df['Actual'].apply(lambda x: f'${x:,.0f}')
                display_df['Variance $'] = display_df['Variance $'].apply(lambda x: f'${x:+,.0f}')
                display_df['Variance %'] = display_df['Variance %'].apply(lambda x: f'{x:+.1f}%')
                display_df['Status'] = display_df['Variance %'].apply(
                    lambda x: '🔴' if abs(float(x.strip('%'))) > 10 else '🟡'
                )
                
                st.dataframe(
                    display_df[['Status', 'GL Description', 'Budget', 'Actual', 'Variance $', 'Variance %']],
                    use_container_width=True,
                    hide_index=True
                )
                
                # AI-Generated Explanations
                st.markdown("### 💡 AI-Generated Insights & Explanations")
                
                # Get context
                clinical_context = dept_clinical.iloc[0] if not dept_clinical.empty else None
                staffing_context = dept_staffing.iloc[0] if not dept_staffing.empty else None
                
                # Generate explanations
                for _, variance in significant_variances.iterrows():
                    gl_desc = variance['GL Description']
                    var_pct = variance['Variance %']
                    var_amt = variance['Variance $']
                    
                    with st.expander(f"📊 {gl_desc} Analysis ({var_pct:+.1f}%)"):
                        if gl_desc == 'Salaries' and var_pct > 0:
                            if staffing_context is not None and staffing_context['overtime_hours'] > 100:
                                overtime_impact = staffing_context['overtime_cost']
                                st.markdown(f"""
                                **Variance Analysis: {gl_desc}**
                                
                                **Amount**: ${var_amt:+,.0f} ({var_pct:+.1f}% over budget)
                                
                                **Primary Drivers Identified**:
                                1. **Overtime Usage**: {staffing_context['overtime_hours']:.0f} hours (${overtime_impact:,.0f} cost)
                                   - Represents {(overtime_impact/var_amt)*100:.1f}% of total variance
                                   - Likely due to staffing shortages or increased patient volume
                                
                                2. **Clinical Context**:
                                   - Visit volume: {clinical_context['visits_actual']:,} ({((clinical_context['visits_actual']/clinical_context['visits_budget'])-1)*100:+.1f}% vs target)
                                
                                **Recommendations**:
                                - Review staffing model and consider permanent hires
                                - Analyze scheduling patterns to optimize coverage
                                - Consider float pool or PRN staff for peak periods
                                """)
                            else:
                                st.markdown(f"""
                                **Variance Analysis: {gl_desc}**
                                
                                **Amount**: ${var_amt:+,.0f} ({var_pct:+.1f}% over budget)
                                
                                **Potential Drivers**:
                                1. Unplanned salary adjustments or market rate corrections
                                2. Additional hiring beyond budgeted positions
                                3. Shift differential or holiday pay above projections
                                
                                **Recommendations**:
                                - Verify all new hires were approved in budget
                                - Review compensation adjustments
                                - Update forecast for remainder of year
                                """)
                        
                        elif gl_desc == 'Medical Supplies' and var_pct > 0:
                            if clinical_context is not None:
                                visit_variance = ((clinical_context['visits_actual'] / clinical_context['visits_budget']) - 1) * 100 if clinical_context['visits_budget'] > 0 else 0
                                cost_per_visit_budget = variance['Budget'] / clinical_context['visits_budget'] if clinical_context['visits_budget'] > 0 else 0
                                cost_per_visit_actual = variance['Actual'] / clinical_context['visits_actual'] if clinical_context['visits_actual'] > 0 else 0
                                
                                st.markdown(f"""
                                **Variance Analysis: {gl_desc}**
                                
                                **Amount**: ${var_amt:+,.0f} ({var_pct:+.1f}% over budget)
                                
                                **Usage Analysis**:
                                1. **Volume Impact**:
                                   - Visit volume variance: {visit_variance:+.1f}%
                                   - Budgeted cost/visit: ${cost_per_visit_budget:.2f}
                                   - Actual cost/visit: ${cost_per_visit_actual:.2f}
                                   - Per-visit variance: ${cost_per_visit_actual - cost_per_visit_budget:+.2f}
                                
                                2. **Department Specifics**:
                                   - No-show rate: {clinical_context['no_show_rate']:.1%}
                                   - Provider wRVUs: {clinical_context['provider_wrvus']:,.0f}
                                
                                **Recommendations**:
                                - Conduct supply utilization audit
                                - Review vendor contracts
                                - Implement par level monitoring
                                """)
                            else:
                                st.markdown(f"""
                                **Variance Analysis: {gl_desc}**
                                
                                **Amount**: ${var_amt:+,.0f} ({var_pct:+.1f}% over budget)
                                
                                This variance requires investigation of:
                                - Recent price changes from suppliers
                                - Changes in clinical protocols
                                - Inventory management practices
                                """)
                        
                        else:
                            st.markdown(f"""
                            **Variance Analysis: {gl_desc}**
                            
                            **Amount**: ${var_amt:+,.0f} ({var_pct:+.1f}% {"over" if var_pct > 0 else "under"} budget)
                            
                            **Analysis Required**:
                            1. Review transaction detail for unusual items
                            2. Check for timing differences or accruals
                            3. Validate budget assumptions vs. actual activity
                            
                            **Next Steps**:
                            - Pull detailed GL transactions
                            - Meet with department manager
                            - Update forecast if variance is permanent
                            """)
                        
                        # Action items
                        st.markdown("#### 📋 Action Items")
                        if abs(var_pct) > 10:
                            st.warning("⚠️ Immediate review required - variance exceeds 10%")
                            st.markdown("""
                            - [ ] Schedule variance review meeting within 48 hours
                            - [ ] Prepare corrective action plan
                            - [ ] Update monthly forecast
                            - [ ] Report to Finance Director
                            """)
                        elif abs(var_pct) > 5:
                            st.info("ℹ️ Monitor closely - variance exceeds 5%")
                            st.markdown("""
                            - [ ] Investigate root cause
                            - [ ] Document findings
                            - [ ] Determine if temporary or permanent
                            - [ ] Update forecast if needed
                            """)

elif selected_feature == "Performance Scorecard":
    st.markdown("## 🏆 Clinic Performance Scorecard")
    st.markdown("Comprehensive performance assessment across multiple dimensions")
    
    # Calculate scores for all departments
    scores = []
    
    for dept in data['budget']['department'].unique():
        # Get latest month data
        latest_month = data['budget']['month'].max()
        
        # Get department data
        dept_budget = data['budget'][
            (data['budget']['department'] == dept) & 
            (data['budget']['month'] == latest_month)
        ]
        dept_clinical = data['clinical'][
            (data['clinical']['department'] == dept) & 
            (data['clinical']['month'] == latest_month)
        ]
        dept_staffing = data['staffing'][
            (data['staffing']['department'] == dept) & 
            (data['staffing']['month'] == latest_month)
        ]
        
        if not dept_clinical.empty and not dept_staffing.empty:
            clinical = dept_clinical.iloc[0]
            staffing = dept_staffing.iloc[0]
            
            # 1. Budget Variance Score (15%)
            variance_pct = ((dept_budget['actual_amount'].sum() - dept_budget['budget_amount'].sum()) / 
                          dept_budget['budget_amount'].sum()) * 100 if dept_budget['budget_amount'].sum() > 0 else 0
            budget_score = max(0, min(100, 100 - abs(variance_pct) * 5))
            
            # 2. Volume Score (15%)
            volume_achievement = (clinical['visits_actual'] / clinical['visits_budget']) * 100 if clinical['visits_budget'] > 0 else 0
            volume_score = max(0, min(100, volume_achievement))
            
            # 3. Productivity Score (20%)
            productivity_score = min(100, (clinical['provider_wrvus'] / 4000) * 100)
            
            # 4. Access Score (10%)
            wait_days = clinical['avg_wait_days']
            access_score = max(0, min(100, 100 - (wait_days - 1) * 25))
            
            # 5. Overtime Score (10%)
            total_hours = (staffing['provider_fte'] + staffing['rn_fte'] + 
                         staffing['ma_fte'] + staffing['admin_fte']) * 160
            overtime_ratio = (staffing['overtime_hours'] / total_hours) * 100 if total_hours > 0 else 0
            overtime_score = max(0, min(100, 100 - overtime_ratio * 10))
            
            # 6. Satisfaction Score (10%)
            satisfaction_score = clinical['patient_satisfaction']
            
            # 7. Strategic Alignment Score (20%)
            dept_strategic = data['strategic'][data['strategic']['department'] == dept]
            if not dept_strategic.empty:
                active_initiatives = dept_strategic[dept_strategic['status'] == 'Active']
                strategic_score = min(100, 70 + len(active_initiatives) * 10)
            else:
                strategic_score = 70
            
            # Calculate composite score
            composite_score = (
                budget_score * 0.15 +
                volume_score * 0.15 +
                productivity_score * 0.20 +
                access_score * 0.10 +
                overtime_score * 0.10 +
                satisfaction_score * 0.10 +
                strategic_score * 0.20
            )
            
            scores.append({
                'Department': dept,
                'Budget': round(budget_score, 1),
                'Volume': round(volume_score, 1),
                'Productivity': round(productivity_score, 1),
                'Access': round(access_score, 1),
                'Overtime': round(overtime_score, 1),
                'Satisfaction': round(satisfaction_score, 1),
                'Strategic': round(strategic_score, 1),
                'Overall Score': round(composite_score, 1)
            })
    
    if scores:
        scores_df = pd.DataFrame(scores)
        
        # Department selector
        selected_dept = st.selectbox("Select Department for Detailed View", scores_df['Department'])
        
        # Get department scores
        dept_scores = scores_df[scores_df['Department'] == selected_dept].iloc[0]
        
        # Display overall score
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            overall_score = dept_scores['Overall Score']
            
            # Create gauge chart
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = overall_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': f"{selected_dept} Performance Score"},
                delta = {'reference': 75},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "gray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # Status interpretation
            if overall_score >= 80:
                st.success(f"🌟 Excellent Performance - Score: {overall_score:.1f}/100")
            elif overall_score >= 60:
                st.warning(f"📊 Good Performance - Score: {overall_score:.1f}/100")
            else:
                st.error(f"⚠️ Needs Improvement - Score: {overall_score:.1f}/100")
        
        # Component scores radar chart
        st.markdown("### Performance Dimensions")
        
        categories = ['Budget', 'Volume', 'Productivity', 'Access', 'Overtime', 'Satisfaction', 'Strategic']
        values = [dept_scores[cat] for cat in categories]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=selected_dept,
            line_color='blue'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=[75] * len(categories),
            theta=categories,
            fill=None,
            mode='lines',
            name='Benchmark',
            line=dict(color='red', dash='dash')
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Performance Profile vs Benchmark"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Department ranking
        st.markdown("### Department Rankings")
        
        ranking_df = scores_df[['Department', 'Overall Score']].sort_values('Overall Score', ascending=False).reset_index(drop=True)
        ranking_df['Rank'] = range(1, len(ranking_df) + 1)
        ranking_df['Status'] = ranking_df['Overall Score'].apply(
            lambda x: '🥇' if x >= 80 else '🥈' if x >= 70 else '🥉' if x >= 60 else '⚠️'
        )
        
        st.dataframe(
            ranking_df[['Rank', 'Status', 'Department', 'Overall Score']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("Insufficient data to calculate performance scores")

elif selected_feature == "Equity Budget Modeling":
    st.markdown("## 🏥 Equity-Aware Budget Modeling")
    st.markdown("Adjust budgets based on social determinants and population health needs")
    
    # Department selection
    dept = st.selectbox("Select Department", data['equity']['department'].unique())
    dept_equity = data['equity'][data['equity']['department'] == dept].iloc[0]
    
    # Display equity metrics
    st.markdown("### Population Health Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        svi_score = dept_equity['svi_score']
        st.metric(
            "Social Vulnerability Index",
            f"{svi_score:.2f}",
            "High" if svi_score > 0.75 else "Moderate" if svi_score > 0.5 else "Low"
        )
    
    with col2:
        medicaid_pct = dept_equity['medicaid_pct']
        st.metric(
            "Medicaid %",
            f"{medicaid_pct:.1%}",
            "Above avg" if medicaid_pct > 0.3 else "Below avg"
        )
    
    with col3:
        complexity_pct = dept_equity['complexity_tier_3_pct']
        st.metric(
            "High Complexity Patients",
            f"{complexity_pct:.1%}",
            "High burden" if complexity_pct > 0.25 else "Typical"
        )
    
    with col4:
        transit_score = dept_equity['transit_score']
        language_pct = dept_equity['language_barrier_pct']
        
        st.metric(
            "Transit Access",
            f"{transit_score:.2f}",
            "Limited" if transit_score < 0.5 else "Good"
        )
    
    # Calculate equity adjustments
    st.markdown("### Recommended Budget Adjustments")
    
    # Base budget
    dept_budget = data['budget'][data['budget']['department'] == dept]
    base_monthly_budget = dept_budget.groupby('month')['budget_amount'].sum().mean()
    
    # Calculate adjustments
    adjustments = {}
    
    if svi_score > 0.75:
        adjustments['High SVI Population'] = base_monthly_budget * 0.08
    elif svi_score > 0.5:
        adjustments['Moderate SVI Population'] = base_monthly_budget * 0.04
    
    if medicaid_pct > 0.4:
        adjustments['High Medicaid Mix'] = base_monthly_budget * 0.06
    elif medicaid_pct > 0.3:
        adjustments['Above-Avg Medicaid'] = base_monthly_budget * 0.03
    
    if complexity_pct > 0.3:
        adjustments['Complex Patient Mix'] = base_monthly_budget * 0.10
    elif complexity_pct > 0.2:
        adjustments['Moderate Complexity'] = base_monthly_budget * 0.05
    
    if language_pct > 0.15:
        adjustments['Language Services'] = base_monthly_budget * 0.03
    
    if transit_score < 0.5:
        adjustments['Transportation Support'] = base_monthly_budget * 0.02
    
    # Display adjustments
    total_adjustment = sum(adjustments.values())
    equity_budget = base_monthly_budget + total_adjustment
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Standard Budget Model")
        st.metric("Monthly Budget", f"${base_monthly_budget:,.0f}")
        
        st.markdown("#### Equity Adjustments")
        for reason, amount in adjustments.items():
            st.write(f"• {reason}: +${amount:,.0f}")
    
    with col2:
        st.markdown("#### Equity-Aware Budget")
        st.metric(
            "Adjusted Monthly Budget",
            f"${equity_budget:,.0f}",
            f"+${total_adjustment:,.0f} ({(total_adjustment/base_monthly_budget)*100:.1f}%)"
        )
        
        st.info(f"""
        **Annual Impact**
        - Standard: ${base_monthly_budget * 12:,.0f}
        - Equity-Aware: ${equity_budget * 12:,.0f}
        - Additional Need: ${total_adjustment * 12:,.0f}
        """)
    
    # Narrative
    st.markdown("### Budget Justification")
    
    narrative = f"""
    The {dept} department serves a population with significant health equity challenges:
    
    - **Social Vulnerability**: SVI score of {svi_score:.2f}
    - **Insurance Mix**: {medicaid_pct:.1%} Medicaid coverage
    - **Care Complexity**: {complexity_pct:.1%} high-complexity patients
    - **Language Access**: {language_pct:.1%} with language barriers
    
    These factors justify a {(total_adjustment/base_monthly_budget)*100:.1f}% budget increase to maintain equitable access and quality of care.
    """
    
    st.info(narrative)

elif selected_feature == "Change Requests":
    st.markdown("## 📝 Change Request Management System")
    st.markdown("Submit and track mid-year budget modifications")
    
    tab1, tab2 = st.tabs(["Submit Request", "View Requests"])
    
    with tab1:
        st.markdown("### New Change Request")
        
        with st.form("change_request_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                request_type = st.selectbox(
                    "Request Type",
                    ["Add FTE", "Remove FTE", "Adjust Volume Target", "CAPEX Request", "Other"]
                )
                
                department = st.selectbox(
                    "Department",
                    data['budget']['department'].unique()
                )
                
                effective_date = st.date_input(
                    "Effective Date",
                    min_value=datetime.now().date()
                )
            
            with col2:
                if request_type == "Add FTE":
                    fte_role = st.selectbox("Role", ["MD", "NP", "PA", "RN", "MA", "Admin"])
                    fte_count = st.number_input("FTE Count", min_value=0.5, max_value=5.0, step=0.5, value=1.0)
                    request_details = f"Add {fte_count} {fte_role}"
                else:
                    request_details = st.text_input("Request Details")
            
            justification = st.text_area(
                "Justification",
                placeholder="Explain the business case for this change..."
            )
            
            submitted = st.form_submit_button("Submit Request")
            
            if submitted and request_details and justification:
                new_request = {
                    'request_id': f"CR-{len(st.session_state.change_requests) + 1:04d}",
                    'date_submitted': datetime.now(),
                    'department': department,
                    'request_type': request_type,
                    'details': request_details,
                    'justification': justification,
                    'effective_date': effective_date,
                    'status': 'Pending'
                }
                
                st.session_state.change_requests.append(new_request)
                st.success(f"✅ Request {new_request['request_id']} submitted successfully!")
    
    with tab2:
        st.markdown("### Change Request Dashboard")
        
        if st.session_state.change_requests:
            requests_df = pd.DataFrame(st.session_state.change_requests)
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Requests", len(requests_df))
            with col2:
                pending_count = len(requests_df[requests_df['status'] == 'Pending'])
                st.metric("Pending Review", pending_count)
            with col3:
                approved_count = len(requests_df[requests_df['status'] == 'Approved']) if 'Approved' in requests_df['status'].values else 0
                st.metric("Approved", approved_count)
            
            # Display table
            st.dataframe(
                requests_df[['request_id', 'department', 'request_type', 'details', 'status']],
                use_container_width=True
            )
        else:
            st.info("No change requests submitted yet")

elif selected_feature == "Strategic Initiatives":
    st.markdown("## 🎯 Strategic Initiative Tracker")
    st.markdown("Link strategic projects to financial impact and track progress")
    
    strategic_data = data['strategic']
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_initiatives = len(strategic_data)
        active_initiatives = len(strategic_data[strategic_data['status'] == 'Active'])
        st.metric("Active Initiatives", f"{active_initiatives}/{total_initiatives}")
    
    with col2:
        total_investment = (strategic_data['capex_budget'] + strategic_data['opex_budget']).sum()
        st.metric("Total Investment", f"${total_investment:,.0f}")
    
    with col3:
        projected_revenue = strategic_data['projected_monthly_revenue'].sum() * 12
        st.metric("Projected Annual Revenue", f"${projected_revenue:,.0f}")
    
    with col4:
        avg_roi = ((projected_revenue - strategic_data['opex_budget'].sum()) / total_investment * 100) if total_investment > 0 else 0
        st.metric("Portfolio ROI", f"{avg_roi:.0f}%")
    
    # Initiative details
    st.markdown("### Active Strategic Initiatives")
    
    today = pd.Timestamp.now()
    strategic_data['days_to_completion'] = (strategic_data['target_completion'] - today).dt.days
    strategic_data['progress_pct'] = ((today - strategic_data['start_date']).dt.days / 
                                     (strategic_data['target_completion'] - strategic_data['start_date']).dt.days * 100).clip(0, 100)
    
    for _, initiative in strategic_data.iterrows():
        with st.expander(f"{initiative['initiative_name']} - {initiative['department']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Investment", f"${initiative['capex_budget'] + initiative['opex_budget']:,.0f}")
                st.metric("Status", initiative['status'])
            
            with col2:
                st.metric("Monthly Revenue", f"${initiative['projected_monthly_revenue']:,.0f}")
                st.metric("Phase", initiative['phase'])
            
            with col3:
                months_to_breakeven = ((initiative['capex_budget'] + initiative['opex_budget']) / 
                                     initiative['projected_monthly_revenue']) if initiative['projected_monthly_revenue'] > 0 else float('inf')
                st.metric("Breakeven", f"{months_to_breakeven:.0f} months" if months_to_breakeven != float('inf') else "N/A")
                st.metric("Progress", f"{initiative['progress_pct']:.0f}%")
            
            st.progress(min(initiative['progress_pct'] / 100, 1.0))

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        Healthcare Finance Innovation Suite v1.0 | Professional Financial Intelligence Platform
    </div>
    """,
    unsafe_allow_html=True
)