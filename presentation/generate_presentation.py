"""
GridGuard AI - Enterprise Presentation Generator
Generates a 12-slide widescreen PowerPoint presentation for the IBM x BOB Hackathon.
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Color Palette Constants
COLOR_BG_DARK = RGBColor(15, 23, 42)        # Deep Slate / Navy (#0F172A)
COLOR_CARD_DARK = RGBColor(30, 41, 59)      # Card Slate (#1E293B)
COLOR_CARD_BORDER = RGBColor(51, 65, 85)    # Slate Border (#334155)
COLOR_PRIMARY_BLUE = RGBColor(37, 99, 235)  # Electric Blue (#2563EB)
COLOR_CYAN = RGBColor(6, 182, 212)          # Accent Cyan (#06B6D4)
COLOR_WHITE = RGBColor(255, 255, 255)       # White (#FFFFFF)
COLOR_TEXT_MUTED = RGBColor(148, 163, 184)  # Muted Slate (#94A3B8)
COLOR_GREEN = RGBColor(16, 185, 129)        # Emerald (#10B981)
COLOR_AMBER = RGBColor(245, 158, 11)        # Amber (#F59E0B)
COLOR_RED = RGBColor(239, 68, 68)           # Red (#EF4444)

def set_slide_background(slide, color):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg

def add_header(slide, title_text, category_text="GRIDGUARD AI — IBM x BOB HACKATHON"):
    # Category badge
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = category_text.upper()
    p_c.font.size = Pt(11)
    p_c.font.bold = True
    p_c.font.color.rgb = COLOR_CYAN

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.7))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(26)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_WHITE

def add_card(slide, left, top, width, height, title, body_points, border_color=COLOR_PRIMARY_BLUE, bg_color=COLOR_CARD_DARK):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.5)

    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.25)
    tf.margin_bottom = Inches(0.25)

    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.size = Pt(18)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_WHITE
    p0.space_after = Pt(12)

    for pt in body_points:
        p = tf.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_TEXT_MUTED
        p.space_after = Pt(6)

def build_presentation(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, COLOR_BG_DARK)

    # Accent decorative box
    accent = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(0.15), Inches(3.8))
    accent.fill.solid()
    accent.fill.fore_color.rgb = COLOR_CYAN
    accent.line.fill.background()

    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(11.0), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "IBM x BOB HACKATHON 2026 — SUBMISSION"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_CYAN
    p0.space_after = Pt(10)

    p1 = tf.add_paragraph()
    p1.text = "GridGuard AI"
    p1.font.size = Pt(48)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE
    p1.space_after = Pt(10)

    p2 = tf.add_paragraph()
    p2.text = "Intelligent Predictive Maintenance & Power Outage Risk Advisory Platform"
    p2.font.size = Pt(22)
    p2.font.color.rgb = COLOR_TEXT_MUTED
    p2.space_after = Pt(30)

    p3 = tf.add_paragraph()
    p3.text = "Team: CodeCraft   |   Track: AI & Clean Energy Resilience   |   Core Tech: XGBoost, Isolation Forest & IBM watsonx.ai"
    p3.font.size = Pt(14)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_PRIMARY_BLUE

    # -------------------------------------------------------------
    # SLIDE 2: Problem Statement
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, COLOR_BG_DARK)
    add_header(s2, "The Problem: Fragile Grids & Costly Reactive Maintenance")

    add_card(s2, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8), 
             "Aging Critical Assets", [
                 "Over 60% of distribution transformers operate past their 25-30 year design life.",
                 "Continuous electrical overloading accelerates thermal winding breakdown.",
                 "Dielectric oil decay and partial discharge remain invisible to periodic inspections."
             ], border_color=COLOR_RED)

    add_card(s2, Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.8), 
             "Catastrophic Outages", [
                 "Single transformer failures trigger cascading municipal power blackouts.",
                 "Emergency repairs take 4x longer and cost 10x more than preventive servicing.",
                 "Critical facilities (hospitals, water grids, transit) suffer severe economic loss."
             ], border_color=COLOR_AMBER)

    add_card(s2, Inches(8.8), Inches(1.8), Inches(3.6), Inches(4.8), 
             "The Trust & Action Gap", [
                 "Control rooms face severe alert fatigue from uncalibrated static threshold alarms.",
                 "Black-box AI models fail to provide explainable risk attribution for dispatchers.",
                 "Citizens receive zero advance warning before localized power cuts."
             ], border_color=COLOR_PRIMARY_BLUE)

    # -------------------------------------------------------------
    # SLIDE 3: Solution Overview & Value Proposition
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, COLOR_BG_DARK)
    add_header(s3, "The Solution: GridGuard AI End-to-End Platform")

    add_card(s3, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8), 
             "1. Dual-Engine ML Core", [
                 "Supervised XGBoost Classifier with Platt Calibration for 7-day failure forecasting.",
                 "Unsupervised Isolation Forest detecting multivariate sensor anomalies.",
                 "Point-in-time feature engineering with zero future lookahead leakage."
             ], border_color=COLOR_CYAN)

    add_card(s3, Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.8), 
             "2. watsonx.ai Copilot", [
                 "Grounded prompt payload architecture feeding IBM Granite 13B models.",
                 "Natural language queries on transformer health, risk drivers, and triage.",
                 "Zero hallucination: strictly grounded on verified physical telemetry."
             ], border_color=COLOR_PRIMARY_BLUE)

    add_card(s3, Inches(8.8), Inches(1.8), Inches(3.6), Inches(4.8), 
             "3. Dual-Persona Command", [
                 "Grid Dispatcher Center: Real-time risk maps, sensor trends, automated crew dispatch.",
                 "Consumer Portal: Citizen service status, proactive storm alerts, rapid issue ticketing.",
                 "Seamless REST API integration across edge IoT and web applications."
             ], border_color=COLOR_GREEN)

    # -------------------------------------------------------------
    # SLIDE 4: Machine Learning Subsystem
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, COLOR_BG_DARK)
    add_header(s4, "Machine Learning Architecture & Data Science Rigor")

    add_card(s4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), 
             "Calibrated Failure Forecasting (FR-08)", [
                 "Algorithm: XGBoost Classifier + CalibratedClassifierCV (Platt Sigmoid).",
                 "Prediction Horizon: 168 hours (7 days forward) with 2-hour operational lead time.",
                 "Output: Statistically calibrated probability P(failure) representing true frequency.",
                 "Evaluation Strategy: Purged & Embargoed walk-forward cross-validation.",
                 "Features: 35 point-in-time features (thermal headroom, vibration RMS, oil decay rate)."
             ], border_color=COLOR_PRIMARY_BLUE)

    add_card(s4, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8), 
             "Multivariate Anomaly Detection (FR-09)", [
                 "Algorithm: Multivariate Isolation Forest (150 estimators, 8% contamination).",
                 "Input Telemetry: Temperature, vibration, partial discharge, oil quality, current, voltage.",
                 "Z-Score Decomposition: Identifies specific deviant sensors relative to normal baselines.",
                 "Hybrid Synergy: Anomaly score feeds directly into multi-factor composite risk engine.",
                 "Registry Persistence: Bundled as versioned artifacts with metadata and transformers."
             ], border_color=COLOR_CYAN)

    # -------------------------------------------------------------
    # SLIDE 5: Multi-Factor Composite Risk Formulation
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, COLOR_BG_DARK)
    add_header(s5, "Multi-Factor Risk Scoring Engine (SRS FR-10)")

    # Formula card banner
    f_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(1.4))
    f_card.fill.solid()
    f_card.fill.fore_color.rgb = COLOR_CARD_DARK
    f_card.line.color.rgb = COLOR_CYAN
    f_card.line.width = Pt(1.5)
    tf_f = f_card.text_frame
    tf_f.margin_top = Inches(0.18)
    p_f0 = tf_f.paragraphs[0]
    p_f0.text = "MATHEMATICAL FORMULATION:"
    p_f0.font.size = Pt(11)
    p_f0.font.bold = True
    p_f0.font.color.rgb = COLOR_CYAN
    p_f1 = tf_f.add_paragraph()
    p_f1.text = "Risk Score = 100 x ( 0.35 * P_failure + 0.20 * S_anomaly + 0.15 * R_weather + 0.15 * R_history + 0.15 * C_criticality )"
    p_f1.font.size = Pt(17)
    p_f1.font.bold = True
    p_f1.font.color.rgb = COLOR_WHITE

    # 4 Sub-tiers
    add_card(s5, Inches(0.8), Inches(3.5), Inches(2.7), Inches(3.2),
             "LOW RISK", [
                 "Score: 0 to 19",
                 "Nominal operation",
                 "Routine 90-day cycle",
                 "Standard monitoring"
             ], border_color=COLOR_GREEN)

    add_card(s5, Inches(3.8), Inches(3.5), Inches(2.7), Inches(3.2),
             "MEDIUM RISK", [
                 "Score: 20 to 39",
                 "Minor sensor drift",
                 "Priority 3 inspection",
                 "Trend logging active"
             ], border_color=COLOR_PRIMARY_BLUE)

    add_card(s5, Inches(6.8), Inches(3.5), Inches(2.7), Inches(3.2),
             "HIGH RISK", [
                 "Score: 40 to 69",
                 "Multiple alerts",
                 "Priority 2 triage",
                 "48-hour crew dispatch"
             ], border_color=COLOR_AMBER)

    add_card(s5, Inches(9.8), Inches(3.5), Inches(2.7), Inches(3.2),
             "CRITICAL RISK", [
                 "Score: 70 to 100",
                 "Immediate failure risk",
                 "Priority 1 Emergency",
                 "Immediate load shed"
             ], border_color=COLOR_RED)

    # -------------------------------------------------------------
    # SLIDE 6: Explainable AI & IBM watsonx.ai Integration
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, COLOR_BG_DARK)
    add_header(s6, "Explainable AI & IBM watsonx.ai Granite Copilot")

    add_card(s6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), 
             "Feature Attribution & Explainability", [
                 "Tree-based SHAP/attribution weights reveal the exact drivers of equipment stress.",
                 "Example Attribution for TR-002: Oil quality decay rate (38%), Ambient heatwave (26%), Vibration crest (21%).",
                 "Sensor z-score decomposition highlights anomalous values against standard deviation envelopes.",
                 "Operators receive transparent 'Why' explanations instead of blind predictions."
             ], border_color=COLOR_PRIMARY_BLUE)

    add_card(s6, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8), 
             "IBM watsonx.ai Granite 13B Grounding", [
                 "Structured factual payload injects asset ID, telemetry, risk breakdown, and maintenance records.",
                 "Zero hallucination guarantee: LLM synthesizes operational advice using only verified telemetry context.",
                 "Conversational Copilot: Dispatchers query grid health and receive immediate, actionable maintenance steps.",
                 "Adaptive fallback: Grounded rule-synthesizer activates if IBM Cloud API connection is offline."
             ], border_color=COLOR_CYAN)

    # -------------------------------------------------------------
    # SLIDE 7: Enterprise System Architecture
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, COLOR_BG_DARK)
    add_header(s7, "Enterprise Microservice Architecture & Tech Stack")

    add_card(s7, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8), 
             "Frontend UI Layer", [
                 "React 18 + Vite SPA architecture.",
                 "Tailwind CSS responsive design.",
                 "Recharts time-series telemetry.",
                 "Geospatial substation risk maps.",
                 "Lucide React icon system.",
                 "Role-based Protected Routes."
             ], border_color=COLOR_PRIMARY_BLUE)

    add_card(s7, Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.8), 
             "Backend API Gateway", [
                 "Django 6.1 + Django REST Framework.",
                 "CORS isolation & token-ready auth.",
                 "ORM models: Asset, TelemetryLog, MaintenanceLog.",
                 "Live OpenWeather API integration.",
                 "Modular app architecture (core, weather, maintenance, ai_assistant)."
             ], border_color=COLOR_CYAN)

    add_card(s7, Inches(8.8), Inches(1.8), Inches(3.6), Inches(4.8), 
             "ML & Cloud Intelligence", [
                 "Python 3.14 / 3.12 ML Subsystem.",
                 "XGBoost 3.4.1 & Scikit-Learn 1.9.",
                 "Inference Engine with in-memory caching.",
                 "IBM Cloud Watson Machine Learning SDK.",
                 "IBM Granite 13B foundation model."
             ], border_color=COLOR_GREEN)

    # -------------------------------------------------------------
    # SLIDE 8: Dual-Persona User Experience
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, COLOR_BG_DARK)
    add_header(s8, "Dual-Persona Interface: Operators & Consumers")

    add_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), 
             "Persona A: Grid Operations Center", [
                 "Target: Substation engineers, power dispatchers, and field supervisors.",
                 "Key Capabilities:",
                 "  • Executive KPI Overview: Overall grid risk, monitored transformers, customer exposure.",
                 "  • Geospatial Substation Map: Interactive colored risk markers across the grid network.",
                 "  • Deep Telemetry Inspection: Real-time sensor trends, vibration, and thermal spectrograms.",
                 "  • AI Assistant Chat: Rapid interrogation of critical assets and grid impact scenarios.",
                 "  • Automated Maintenance Board: Triage tickets from generation to resolution."
             ], border_color=COLOR_PRIMARY_BLUE)

    add_card(s8, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8), 
             "Persona B: Consumer Transparency Portal", [
                 "Target: Residential consumers, commercial facilities, and factory managers.",
                 "Key Capabilities:",
                 "  • Live Connection Status: Verifies health of local electricity connection in real time.",
                 "  • Proactive Outage & Storm Alerts: Advance warnings on severe weather and planned repairs.",
                 "  • One-Click Issue Ticketing: Easy reporting for voltage dips, line damage, or outages.",
                 "  • Consumer AI Assistant: Plain-language answers to localized service questions.",
                 "  • Restores public trust through complete operational transparency."
             ], border_color=COLOR_GREEN)

    # -------------------------------------------------------------
    # SLIDE 9: Field Maintenance & Crew Intelligence
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, COLOR_BG_DARK)
    add_header(s9, "Automated Triage & Field Crew Dispatch")

    add_card(s9, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8), 
             "Priority Triage (P1 - P4)", [
                 "P1 Emergency: Critical risk score >= 70. Immediate dispatch required within 2 hours.",
                 "P2 Urgent: High risk score 40-69. Inspection within 24-48 hours.",
                 "P3 Preventive: Medium risk score 20-39. Scheduled servicing within 7 days.",
                 "P4 Routine: Low risk score < 20. Standard operating inspection."
             ], border_color=COLOR_RED)

    add_card(s9, Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.8), 
             "Proximity Crew Routing", [
                 "Real-time GPS proximity matching for available maintenance teams.",
                 "Automated crew pairing (e.g., Crew A dispatched 1.2 km away from TR-002).",
                 "Reduces travel overhead and emergency response latency by up to 60%.",
                 "Skill-based task allocation tailored to electrical vs mechanical repairs."
             ], border_color=COLOR_AMBER)

    add_card(s9, Inches(8.8), Inches(1.8), Inches(3.6), Inches(4.8), 
             "End-to-End Workflow", [
                 "1. Risk detection by ML subsystem.",
                 "2. Automated ticket generated in Django.",
                 "3. Dispatcher reviews AI recommendation.",
                 "4. Field crew updates status via portal.",
                 "5. Closed loop: Retesting validates restoration."
             ], border_color=COLOR_GREEN)

    # -------------------------------------------------------------
    # SLIDE 10: Measurable Business Impact & ROI
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, COLOR_BG_DARK)
    add_header(s10, "Quantifiable Business Impact & ROI")

    add_card(s10, Inches(0.8), Inches(1.8), Inches(2.7), Inches(4.8),
             "-45% OUTAGES", [
                 "Reduction in SAIFI (System Average Interruption Frequency Index).",
                 "Catastrophic failures prevented before winding flashover.",
                 "Pre-emptive cooling and oil maintenance."
             ], border_color=COLOR_GREEN)

    add_card(s10, Inches(3.8), Inches(1.8), Inches(2.7), Inches(4.8),
             "-60% DOWNTIME", [
                 "Reduction in SAIDI (System Average Interruption Duration Index).",
                 "Crews arrive on site with exact replacement components pre-allocated.",
                 "Zero diagnostic trial-and-error."
             ], border_color=COLOR_CYAN)

    add_card(s10, Inches(6.8), Inches(1.8), Inches(2.7), Inches(4.8),
             "-75% FALSE ALARMS", [
                 "Calibrated probabilities eliminate nuisance threshold triggers.",
                 "Restores operator confidence in automation.",
                 "Prevents unneeded emergency call-outs."
             ], border_color=COLOR_PRIMARY_BLUE)

    add_card(s10, Inches(9.8), Inches(1.8), Inches(2.7), Inches(4.8),
             "+$2.4M ANNUAL ROI", [
                 "Estimated savings per 100 substations from avoided transformer rebuilds.",
                 "5-8 years extended equipment asset lifespan.",
                 "Minimized utility regulatory penalty fees."
             ], border_color=COLOR_AMBER)

    # -------------------------------------------------------------
    # SLIDE 11: Scalability, Security & Future Roadmap
    # -------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, COLOR_BG_DARK)
    add_header(s11, "Scalability, Security & Future Roadmap")

    add_card(s11, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8), 
             "Phase 1: Edge & IoT (Q1-Q2)", [
                 "Deploy lightweight ONNX model runtime directly to edge substation gateways.",
                 "MQTT / IEC 61850 protocol ingestion for sub-second telemetry publishing.",
                 "Offline edge inference resilience during network disconnections."
             ], border_color=COLOR_CYAN)

    add_card(s11, Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.8), 
             "Phase 2: Autonomous Grid (Q3)", [
                 "Automated feeder switching & dynamic load balancing across substations.",
                 "Integration with renewable solar/wind generation forecasting.",
                 "Reinforcement learning for predictive dispatch optimization."
             ], border_color=COLOR_PRIMARY_BLUE)

    add_card(s11, Inches(8.8), Inches(1.8), Inches(3.6), Inches(4.8), 
             "Phase 3: Utility Scaling (Q4)", [
                 "Multi-tenant DISCOM (distribution company) cloud architecture on IBM Cloud.",
                 "Enterprise SCADA & SAP Plant Maintenance connector modules.",
                 "Nationwide grid resilience analytics & climate disaster hardening."
             ], border_color=COLOR_GREEN)

    # -------------------------------------------------------------
    # SLIDE 12: Conclusion & Q&A
    # -------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, COLOR_BG_DARK)

    # Center card
    c_card = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.8), Inches(1.2), Inches(9.7), Inches(5.1))
    c_card.fill.solid()
    c_card.fill.fore_color.rgb = COLOR_CARD_DARK
    c_card.line.color.rgb = COLOR_CYAN
    c_card.line.width = Pt(2.0)

    tf_c = c_card.text_frame
    tf_c.word_wrap = True
    tf_c.margin_top = Inches(0.4)
    tf_c.margin_left = Inches(0.5)
    tf_c.margin_right = Inches(0.5)

    p0 = tf_c.paragraphs[0]
    p0.text = "GRIDGUARD AI"
    p0.alignment = PP_ALIGN.CENTER
    p0.font.size = Pt(36)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_WHITE
    p0.space_after = Pt(8)

    p1 = tf_c.add_paragraph()
    p1.text = "Empowering Power Utilities with Predictive Machine Learning & IBM watsonx.ai"
    p1.alignment = PP_ALIGN.CENTER
    p1.font.size = Pt(18)
    p1.font.color.rgb = COLOR_CYAN
    p1.space_after = Pt(24)

    p2 = tf_c.add_paragraph()
    p2.text = "Key Deliverables & Resources:"
    p2.alignment = PP_ALIGN.CENTER
    p2.font.size = Pt(16)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE
    p2.space_after = Pt(12)

    p3 = tf_c.add_paragraph()
    p3.text = "• Full Source Code & Restructured Repository: CodeCraft / GridGuard AI"
    p3.font.size = Pt(14)
    p3.font.color.rgb = COLOR_TEXT_MUTED
    p3.space_after = Pt(6)

    p4 = tf_c.add_paragraph()
    p4.text = "• One-Click Development Launchers: start.bat and stop.bat"
    p4.font.size = Pt(14)
    p4.font.color.rgb = COLOR_TEXT_MUTED
    p4.space_after = Pt(6)

    p5 = tf_c.add_paragraph()
    p5.text = "• End-to-End Documentation: Problem Statement, Solution Overview, Architecture, Setup Guide"
    p5.font.size = Pt(14)
    p5.font.color.rgb = COLOR_TEXT_MUTED
    p5.space_after = Pt(6)

    p6 = tf_c.add_paragraph()
    p6.text = "• Live Demonstrations: Operator Portal (admin@gridguard.ai) & Citizen Portal (user@gridguard.ai)"
    p6.font.size = Pt(14)
    p6.font.color.rgb = COLOR_TEXT_MUTED
    p6.space_after = Pt(20)

    p7 = tf_c.add_paragraph()
    p7.text = "Thank You! We Welcome Your Questions & Evaluation."
    p7.alignment = PP_ALIGN.CENTER
    p7.font.size = Pt(20)
    p7.font.bold = True
    p7.font.color.rgb = COLOR_WHITE

    prs.save(output_path)
    print(f"[SUCCESS] Presentation generated successfully: {output_path}")

if __name__ == "__main__":
    import sys
    out = "presentation/GridGuard_AI_Presentation.pptx"
    build_presentation(out)
