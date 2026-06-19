from fpdf import FPDF
import os

class PitchDeck(FPDF):
    def header(self):
        # Obsidian charcoal background
        self.set_fill_color(20, 20, 25)
        self.rect(0, 0, 297, 210, 'F')
        
    def add_content_slide(self, title, items, subtitle=""):
        self.add_page()
        # Title (Amber)
        self.set_text_color(255, 175, 50) # Signal Amber
        self.set_font("helvetica", "B", 26)
        self.cell(0, 15, title, ln=True, align="L")
        
        if subtitle:
            self.set_text_color(150, 160, 170)
            self.set_font("courier", "B", 14) # Monospace for ops feel
            self.cell(0, 10, f"[{subtitle}]", ln=True, align="L")
            self.ln(5)
        else:
            self.ln(10)
            
        self.set_font("helvetica", "", 18)
        self.set_text_color(230, 235, 240)
        for item in items:
            self.multi_cell(0, 10, f"> {item}")
            self.ln(6)

pdf = PitchDeck(orientation="L", unit="mm", format="A4")
pdf.set_auto_page_break(auto=True, margin=15)

# Slide 1: Cover
pdf.add_page()
pdf.set_text_color(255, 175, 50)
pdf.set_font("helvetica", "B", 56)
pdf.ln(50)
pdf.cell(0, 20, "BandOps", ln=True, align="C")
pdf.set_text_color(255, 255, 255)
pdf.set_font("helvetica", "", 22)
pdf.cell(0, 15, "Multi-Agent Command Rooms for Crisis Operations", ln=True, align="C")
pdf.set_text_color(200, 50, 50) # Safety Red
pdf.set_font("courier", "B", 16)
pdf.cell(0, 15, "STATUS: SYSTEM ONLINE", ln=True, align="C")

# Slide 2: Hook
pdf.add_content_slide("The $15,000/Minute Problem", [
    "A grounded plane (AOG) costs airlines $15,000 per minute.",
    "The clock starts immediately.",
    "Every second wasted on logistics is thousands of dollars burned."
], "CRITICAL_ALERT")

# Slide 3: The Problem
pdf.add_content_slide("The Problem: Siloed Crisis Ops", [
    "1. Data Fragmentation: Mechanics, Logistics, and Ops use different systems.",
    "2. Latency: Communication relies on phone calls and emails.",
    "3. Compliance Risk: FAA regulations are often manually checked.",
    "4. Cognitive Overload: Humans panic under immense financial pressure.",
    "5. Zero Traceability: Post-crisis audits are a nightmare."
], "FAILURE_MODES")

# Slide 4: Current Reality
pdf.add_content_slide("Current Reality: The Trapped Dispatcher", [
    "The human dispatcher is the bottleneck, trapped between:",
    "- Maintenance APIs",
    "- Supply Chain Databases",
    "- Crew Scheduling Systems",
    "- Weather & Air Traffic Control",
    "- FAA Compliance Manuals"
], "BOTTLENECK_DETECTED")

# Slide 5: Introducing BandOps
pdf.add_content_slide("Introducing BandOps", [
    "A secure, cyber-physical Multi-Agent Command Center.",
    "Replaces siloed human panic with an orchestrated swarm of AI agents.",
    "Built for high-stakes, highly regulated enterprise environments.",
    "Powered entirely by the Band API Interoperability Mesh."
], "SOLUTION_INITIALIZED")

# Slide 6: Why Band
pdf.add_content_slide("Why Band?", [
    "WITHOUT BAND: Agents exist in isolation. Custom websockets for 6 agents takes months.",
    "WITH BAND: A persistent, zero-trust mesh. Identity verification and state sync out of the box.",
    "Band is the interoperability layer that makes enterprise systems possible."
], "ARCHITECTURE_RATIONALE")

# Slide 7: Architecture
pdf.add_content_slide("Architecture: 7-Stage Signal Flow", [
    "1. Event Trigger (AOG Detected)",
    "2. Mechanic Diagnosis",
    "3. Supply Chain Sourcing",
    "4. Flight Ops Delay Calculation",
    "5. FAA Adversarial Audit",
    "6. Commander Synthesis",
    "7. Immutable Ledger Write"
], "SIGNAL_FLOW")

# Slide 8: Meet the Agents
pdf.add_content_slide("Meet the Agents", [
    "MECHANIC: Diagnoses faults based on MEL.",
    "SUPPLY CHAIN: Sources parts globally.",
    "FLIGHT OPS: Calculates delay costs and swaps.",
    "CREW SCHEDULER: Locates reserve crews and duty times.",
    "COMMANDER: Synthesizes the debate.",
    "FAA COMPLIANCE [VETO POWER]: Adversarial auditor ensuring strict adherence."
], "AGENT_ROSTER")

# Slide 9: Agent Dynamics
pdf.add_content_slide("Agent Dynamics: The Band Room", [
    "[MECHANIC]: Fault confirmed. Need part #X789.",
    "[LOGISTICS]: Found in Seattle. Shipping takes 4 hours.",
    "[FLIGHT OPS]: 4 hours breaches the delay threshold.",
    "[FAA COMPLIANCE]: WARNING - Proposed crew will violate max duty time.",
    "Agents debate collaboratively, resolving conflicts in milliseconds."
], "LIVE_TRANSCRIPT")

# Slide 10: Demo Flow
pdf.add_content_slide("Demo Flow", [
    "1. Inject Chaos (Engine failure in Seattle)",
    "2. War Room activates.",
    "3. Agents spawn via Band SDK.",
    "4. Real-time cost counter ticks up.",
    "5. Debate concludes.",
    "6. Human reviews Commander's synthesis.",
    "7. Approval granted.",
    "8. System writes to ledger."
], "EXECUTION_PATH")

# Slide 11: Chaos Injection
pdf.add_content_slide("Chaos Injection", [
    "BEFORE: Perfect plan formulated.",
    "CHAOS EVENT: Ground stop issued in Seattle due to severe weather.",
    "AFTER: Agents instantly replan. Logistics reroutes part from LAX.",
    "BandOps adapts faster than humanly possible."
], "ADAPTABILITY_TEST")

# Slide 12: Human-in-the-Loop
pdf.add_content_slide("Human-in-the-Loop (HITL)", [
    "PILLAR 1: AI Prepares. The heavy lifting of data synthesis is automated.",
    "PILLAR 2: Humans Approve. Critical decisions are never fully autonomous.",
    "PILLAR 3: Trust Compounds. Operators learn to trust the swarm over time."
], "SAFETY_PROTOCOLS")

# Slide 13: Audit Trail
pdf.add_content_slide("Immutable Audit Trail", [
    "Every message, tool call, and decision is cryptographically signed.",
    "Logged to a write-only database structure.",
    "Provides flawless traceability for FAA regulators.",
    "Zero black boxes."
], "COMPLIANCE_LEDGER")

# Slide 14: Beyond Aviation
pdf.add_content_slide("Beyond Aviation", [
    "1. Hospitals (ER Triage & Resource Allocation)",
    "2. Energy Grids (Disaster Response)",
    "3. Manufacturing (Supply Chain Shocks)",
    "4. Cybersecurity (Incident Response Rooms)",
    "5. Finance (Fraud Command Centers)",
    "6. Defense (Tactical Ops)",
    "7. Maritime (Port Logistics)"
], "EXPANSION_DOMAINS")

# Slide 15: Differentiators
pdf.add_content_slide("Differentiators", [
    "MOST PROJECTS: Toy chatbots, single framework, zero compliance, black box.",
    "BANDOPS: High stakes, cross-framework (Band), strict compliance, auditable.",
    "We built a true enterprise application, not just a wrapper."
], "COMPETITIVE_ANALYSIS")

# Slide 16: Why Judges Care
pdf.add_content_slide("Why Judges Care", [
    "Demonstrates exactly why Band is necessary for orchestration.",
    "Tackles a real, multi-billion dollar enterprise problem.",
    "Beautiful cyber-physical UI.",
    "Proves that autonomous agents can exist safely in regulated spaces."
], "EVALUATION_CRITERIA")

# Slide 17: Closing
pdf.add_page()
pdf.set_text_color(255, 175, 50)
pdf.set_font("helvetica", "B", 48)
pdf.ln(60)
pdf.cell(0, 20, "BandOps", ln=True, align="C")
pdf.set_text_color(255, 255, 255)
pdf.set_font("helvetica", "", 20)
pdf.cell(0, 15, "The Future of Crisis Operations", ln=True, align="C")
pdf.set_text_color(200, 50, 50)
pdf.set_font("courier", "B", 16)
pdf.cell(0, 15, "END OF TRANSMISSION", ln=True, align="C")

os.makedirs("pitch", exist_ok=True)
pdf.output("pitch/BandOps_Pitch_Deck_17_Slides.pdf")
print("17-Slide PDF generated successfully!")
