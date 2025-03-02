from markdown_pdf import MarkdownPdf, Section

pdf = MarkdownPdf(toc_level=2)

#сохранение текста с markdown-разметкой в файле pdf
async def save_pdf(text, user_id):
    pdf.add_section(Section(text, toc=False))
    pdf.save(f"{user_id}.pdf")