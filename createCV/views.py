from django.shortcuts import render, redirect
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from .forms import PerfilForm, ExperienciaFormSet, EducacionFormSet
from .models import Perfil
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.shortcuts import get_object_or_404
from reportlab.lib.enums import TA_CENTER

def crear_cv(request):
    if request.method == "POST":
        perfil_form = PerfilForm(request.POST, request.FILES)
        
        if perfil_form.is_valid():
            perfil = perfil_form.save(commit=False)
            
            exp_formset = ExperienciaFormSet(request.POST, instance=perfil, prefix='experiencia')
            edu_formset = EducacionFormSet(request.POST, instance=perfil, prefix='educacion')

            if exp_formset.is_valid() and edu_formset.is_valid():
                perfil.save()
                exp_formset.save()
                edu_formset.save()
                return generar_pdf(perfil.id)
        else:
            # Si el formulario del perfil no es válido, volvemos a renderizar
            exp_formset = ExperienciaFormSet(request.POST, prefix='experiencia')
            edu_formset = EducacionFormSet(request.POST, prefix='educacion')

    else:
        perfil_form = PerfilForm()
        exp_formset = ExperienciaFormSet(prefix='experiencia')
        edu_formset = EducacionFormSet(prefix='educacion')

    return render(request, "crear_cv.html", {
        "perfil_form": perfil_form,
        "exp_formset": exp_formset,
        "edu_formset": edu_formset,
    })

def generar_pdf(perfil_id):
    perfil = get_object_or_404(Perfil, id=perfil_id)

    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="CV_{perfil.nombre}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    story = []

    # Estilos personalizados
    styles.add(ParagraphStyle(name='Heading1_Custom', fontSize=24, fontName='Helvetica-Bold',
                              alignment=TA_CENTER, spaceAfter=24))
    styles.add(ParagraphStyle(name='Heading2_Custom', fontSize=14, fontName='Helvetica-Bold',
                              textColor=colors.gray, spaceAfter=12))
    styles.add(ParagraphStyle(name='Normal_Custom', fontSize=10, fontName='Helvetica',
                              leading=12))

    # Encabezado (Nombre y contacto)
    story.append(Paragraph(perfil.nombre, styles['Heading1_Custom']))

    # Contacto y foto en una tabla
    contact_data = [
        [Paragraph(f"<b>INE:</b> {perfil.ine}", styles['Normal_Custom']),
         Image(perfil.imagen.path, width=100, height=100) if perfil.imagen else ''],
        [Paragraph(f"<b>Correo:</b> {perfil.correo}", styles['Normal_Custom']), ''],
        [Paragraph(f"<b>Contacto:</b> {perfil.contacto}", styles['Normal_Custom']), '']
    ]
    contact_table = Table(contact_data, colWidths=[400, 100])
    contact_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (0,-1), 'LEFT'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(contact_table)
    story.append(Spacer(1, 24))

    # Experiencia Laboral
    story.append(Paragraph("Experiencia Laboral", styles['Heading2_Custom']))
    exp_data = [
        [Paragraph("Empresa", styles['Normal_Custom']),
         Paragraph("Puesto", styles['Normal_Custom']),
         Paragraph("Ingreso", styles['Normal_Custom']),
         Paragraph("Salida", styles['Normal_Custom'])]
    ]
    for exp in perfil.experiencias.all():
        exp_data.append([
            Paragraph(exp.empresa, styles['Normal_Custom']),
            Paragraph(exp.puesto, styles['Normal_Custom']),
            Paragraph(str(exp.fecha_ingreso), styles['Normal_Custom']),
            Paragraph(str(exp.fecha_salida or "Presente"), styles['Normal_Custom'])
        ])

    exp_table = Table(exp_data, colWidths=[120, 150, 80, 80])
    exp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0871DA")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
    ]))
    story.append(exp_table)
    story.append(Spacer(1, 24))

    # Formación Académica
    story.append(Paragraph("Formación Académica", styles['Heading2_Custom']))
    edu_data = [
        [Paragraph("Título", styles['Normal_Custom']),
         Paragraph("Institución", styles['Normal_Custom']),
         Paragraph("Ingreso", styles['Normal_Custom']),
         Paragraph("Salida", styles['Normal_Custom'])]
    ]
    for edu in perfil.educacion.all():
        edu_data.append([
            Paragraph(edu.titulo, styles['Normal_Custom']),
            Paragraph(edu.institucion, styles['Normal_Custom']),
            Paragraph(str(edu.fecha_ingreso), styles['Normal_Custom']),
            Paragraph(str(edu.fecha_salida or "Presente"), styles['Normal_Custom'])
        ])

    edu_table = Table(edu_data, colWidths=[150, 150, 80, 80])
    edu_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0871DA')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
    ]))
    story.append(edu_table)

    doc.build(story)
    return response

