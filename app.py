import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from fpdf import FPDF
from agents import RealEstateCrew
import json

# --- 1. INITIALIZATION ---
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'map_coords' not in st.session_state:
    st.session_state.map_coords = (3.139, 101.686) # Default KL

# --- 2. UTILITIES ---
def get_coords(location_name):
    geolocator = Nominatim(user_agent="real_estate_app_unikl")
    try:
        loc = geolocator.geocode(location_name + ", Malaysia")
        if loc: return (loc.latitude, loc.longitude)
    except: pass
    return st.session_state.map_coords

def generate_pdf(data, location):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, f"Strategy Report: {location}", ln=True, align='C')
    pdf.ln(10)
    for k, v in data.items():
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(0, 10, k.replace('_', ' ').title(), ln=True)
        pdf.set_font("helvetica", "", 11)
        pdf.multi_cell(0, 7, str(v))
        pdf.ln(3)
    return bytes(pdf.output())

# --- 3. UI LAYOUT ---
st.set_page_config(page_title="PropTech AI", layout="wide")
st.title("🏙️ AI Real Estate Developer Dashboard")

with st.sidebar:
    st.header("Site Parameters")
    loc_input = st.text_input("Area / Address", "Cheras, KL")
    size_input = st.number_input("Land Size (Acres)", 0.1, 100.0, 1.0)
    budget_input = st.number_input("Budget (RM)", 100000, 100000000, 5000000)
    run_btn = st.button("Generate Strategy", type="primary")
    
    if st.button("Clear Results"):
        st.session_state.analysis_result = None
        st.rerun()

# --- 4. INTERACTIVE MAP ---
st.subheader("Site Overview")
coords = get_coords(loc_input)
st.session_state.map_coords = coords

m = folium.Map(location=coords, zoom_start=14, tiles=None)
folium.TileLayer('OpenStreetMap', name='Street Map').add_to(m)
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri', name='Satellite View'
).add_to(m)
folium.LayerControl().add_to(m)

folium.Marker(coords, popup=f"Site: {loc_input}").add_to(m)
folium.Circle(coords, radius=5000, color='blue', fill=True, fill_opacity=0.1).add_to(m)

# Prevent reruns on hover
st_folium(m, width=1400, height=400, returned_objects=[])

# --- 5. EXECUTION ---
if run_btn:
    with st.spinner("AI Agents are calculating... (3-5 mins on CPU)"):
        crew = RealEstateCrew(loc_input, size_input, budget_input)
        result = crew.run()
        
        # --- JSON SAFETY NET ---
        # If the model fails Pydantic validation, it returns raw text.
        # This block catches that and formats it so the dashboard doesn't crash.
        try:
            if hasattr(result, 'json_dict') and result.json_dict:
                st.session_state.analysis_result = result.json_dict
            else:
                # Fallback: Parse manually or use raw string
                st.session_state.analysis_result = {
                    "proposed_building": "Strategic Recommendation",
                    "logic": result.raw,
                    "target_segment": "Identified in Report",
                    "roi": "See Analysis",
                    "risk_analysis": "Check Risks Tab",
                    "space_utilization": "As per Land Size",
                    "estimated_total_cost": f"Within RM {budget_input}",
                    "financial_feasibility_note": "Validation Error - Showing Raw Text"
                }
        except Exception as e:
            st.error(f"Data Processing Error: {e}")

# --- 6. DISPLAY RESULTS ---
if st.session_state.analysis_result:
    data = st.session_state.analysis_result
    st.divider()
    
    # KPIs
    m1, m2, m3 = st.columns(3)
    m1.metric("Proposed Type", data.get('proposed_building', 'N/A'))
    m2.metric("Target Segment", data.get('target_segment', 'N/A'))
    m3.metric("ROI Potential", data.get('roi', 'N/A'))

    # Tabs
    tab1, tab2, tab3 = st.tabs(["💡 Investment Logic", "⚠️ Risk Assessment", "💰 Financials"])
    with tab1: st.info(data.get('logic', 'No logic provided.'))
    with tab2: st.warning(data.get('risk_analysis', 'No risk analysis available.'))
    with tab3: 
        st.write(f"**Estimated Cost:** {data.get('estimated_total_cost', 'N/A')}")
        st.write(f"**Feasibility Note:** {data.get('financial_feasibility_note', 'N/A')}")
        st.write(f"**Utilization:** {data.get('space_utilization', 'N/A')}")

    # Export
    pdf_bytes = generate_pdf(data, loc_input)
    st.download_button("📥 Download PDF", 
                       data = pdf_bytes,
                       file_name = f"{loc_input}_report.pdf", 
                       mime = "application/pdf")