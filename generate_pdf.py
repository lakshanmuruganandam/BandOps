from fpdf import FPDF
import os

class PitchDeck(FPDF):
    def header(self):
        # Dark background
        self.set_fill_color(15, 23, 42)
        self.rect(0, 0, 297, 210, 'F')
        
    def add_content_slide(self, title, items):
        self.add_page()
        self.set_text_color(255, 255, 255)
        self.set_font("helvetica", "B", 24)
        self.cell(0, 20, title, ln=True, align="L")
        self.ln(10)
        self.set_font("helvetica", "", 16)
        self.set_text_color(200, 210, 220)
        for item in items:
            self.multi_cell(0, 10, f"- {item}")
            self.ln(5)

pdf = PitchDeck(orientation="L", unit="mm", format="A4")
pdf.set_auto_page_break(auto=True, margin=15)

# Slide 1: Title
pdf.add_page()
pdf.set_text_color(56, 189, 248)
pdf.set_font("helvetica", "B", 48)
pdf.ln(50)
pdf.cell(0, 20, "BandOps", ln=True, align="C")
pdf.set_text_color(255, 255, 255)
pdf.set_font("helvetica", "", 20)
pdf.cell(0, 15, "Multi-Agent Command Rooms for Regulated Crises", ln=True, align="C")
pdf.set_text_color(148, 163, 184)
pdf.set_font("helvetica", "I", 16)
pdf.cell(0, 15, "Powered by the Band API", ln=True, align="C")

# Slide 2
pdf.add_content_slide("The Problem: Aircraft on Ground (AOG)", [
    "A grounded plane costs airlines $15,000 per minute.",
    "Mechanics, Logistics, Flight Ops, and the FAA are siloed.",
    "Communication is chaotic: emails, phone calls, whiteboards.",
    "Result: Hours of delays, compliance risks, and millions lost."
])

# Slide 3
pdf.add_content_slide("The Solution: BandOps Command Center", [
    "Replaces siloed human panic with an orchestrated swarm of AI agents.",
    "Agents analyze faults, locate parts, and check regulations in seconds.",
    "Human-in-the-loop: Agents recommend, humans approve.",
    "Built for high-stakes, highly regulated enterprise environments."
])

# Slide 4
pdf.add_content_slide("Why Band? (The Interoperability Layer)", [
    "Band provides the persistent room, identity verification, and audit trail.",
    "Framework-agnostic: Allows LangGraph, CrewAI, and Python agents to collaborate.",
    "Provides the zero-trust mesh that makes enterprise-grade systems possible."
])

# Slide 5
pdf.add_content_slide("The War Room Architecture", [
    "1. Line Mechanic diagnoses the fault.",
    "2. Supply Chain sources replacement parts.",
    "3. Flight Ops calculates delay costs.",
    "4. FAA Compliance acts as an adversarial auditor.",
    "5. AOG Commander synthesizes the debate for the human."
])

# Slide 6
pdf.add_content_slide("Immutable Auditability", [
    "In aviation, every single decision must be auditable.",
    "BandOps logs the entire agent debate to an immutable ledger.",
    "Logs the final human approval cryptographically.",
    "Zero black boxes. Full traceability for regulators."
])

os.makedirs("pitch", exist_ok=True)
pdf.output("pitch/BandOps_Pitch_Deck.pdf")
print("PDF generated successfully!")
