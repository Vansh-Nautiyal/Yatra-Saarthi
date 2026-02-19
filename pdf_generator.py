from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.platypus import PageBreak
import io


def generate_pdf(itenary, travel_details):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    elements = []
    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    normal_style = styles["Normal"]

    elements.append(Paragraph(
        f"Travel Plan for {travel_details['destination']}",
        title_style
    ))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph(
        f"Duration: {travel_details['duration']} days | "
        f"Budget: INR {travel_details['budget']} | "
        f"People: {travel_details['people']}",
        normal_style
    ))
    elements.append(Spacer(1, 0.5 * inch))

    for day in itenary["days"]:
        elements.append(Paragraph(f"Day {day['day']}", styles["Heading2"]))
        elements.append(Spacer(1, 0.2 * inch))

        for activity in day["activities"]:
            text = f"""
            <b>Time:</b> {activity['time']}<br/>
            <b>Activity:</b> {activity['activity']}<br/>
            <b>Estimated Cost:</b> {activity['estimated_cost']}<br/>
            <b>Food:</b> {activity['food_recommendation']}<br/>
            <b>Transport:</b> {activity['transport_suggestion']}<br/><br/>
            """
            elements.append(Paragraph(text, normal_style))
            elements.append(Spacer(1, 0.2 * inch))

        elements.append(PageBreak())

    doc.build(elements)
    buffer.seek(0)

    return buffer
