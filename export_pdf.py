from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(messages):

    file_name = "AI_Conversation.pdf"


    doc = SimpleDocTemplate(
        file_name
    )


    styles = getSampleStyleSheet()


    content = []


    title = Paragraph(
        "AI Assistant Conversation",
        styles["Title"]
    )

    content.append(title)

    content.append(
        Spacer(1,20)
    )


    for message in messages:

        if message["role"] == "system":
            continue


        role = message["role"].upper()


        text = message["content"]


        para = Paragraph(
            f"<b>{role}</b>: {text}",
            styles["BodyText"]
        )


        content.append(para)

        content.append(
            Spacer(1,12)
        )


    doc.build(
        content
    )


    return file_name