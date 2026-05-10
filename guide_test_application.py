# -*- coding: utf-8 -*-
"""
Guide de Test — Application Helmet Detection
Document destine au correcteur pour tester l'application deployee.
"""

import os
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, Image as RLImage, KeepTogether
)
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# Chemins
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
KEITA_DIR = os.path.dirname(PROJECT_DIR)
TEST_DIR = os.path.join(PROJECT_DIR, "test")
OUTPUT = os.path.join(TEST_DIR, "Guide_Test_Application.pdf")

APP_URL = "https://helmet.gdxebec.space/"
API_DOCS_URL = APP_URL.rstrip("/") + "/docs"
LOGO_UCAD = os.path.join(KEITA_DIR, "logo_ucad.png")
P3_IMG = os.path.join(PROJECT_DIR, "parti3-img")
SCR_APP = os.path.join(P3_IMG, "video-screen.png")
SCR_DET_H = os.path.join(P3_IMG, "salif-image-withhelemt.png")
SCR_DET_NH = os.path.join(P3_IMG, "salif-imagewithout-helmet.png")


# Polices
FONTS_DIR = r"C:\Windows\Fonts"
try:
    pdfmetrics.registerFont(TTFont("Arial", os.path.join(FONTS_DIR, "arial.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Bold", os.path.join(FONTS_DIR, "arialbd.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Italic", os.path.join(FONTS_DIR, "ariali.ttf")))
    pdfmetrics.registerFont(TTFont("CourierNew", os.path.join(FONTS_DIR, "cour.ttf")))
    pdfmetrics.registerFont(TTFont("CourierNew-Bold", os.path.join(FONTS_DIR, "courbd.ttf")))
    F = "Arial"; F_BOLD = "Arial-Bold"; F_ITAL = "Arial-Italic"
    F_MONO = "CourierNew"; F_MONOB = "CourierNew-Bold"
except Exception:
    F = "Helvetica"; F_BOLD = "Helvetica-Bold"; F_ITAL = "Helvetica-Oblique"
    F_MONO = "Courier"; F_MONOB = "Courier-Bold"


# Palette harmonisee avec les rapports
PRIMARY = colors.HexColor("#0F172A")
SECONDARY = colors.HexColor("#1E3A8A")
ACCENT = colors.HexColor("#3B82F6")
GOLD = colors.HexColor("#60A5FA")
LIGHT = colors.HexColor("#EFF6FF")
WHITE = colors.white
GRAY = colors.HexColor("#374151")
LGRAY = colors.HexColor("#DBEAFE")
CODE_BG = colors.HexColor("#F8FAFC")
CODE_FG = colors.HexColor("#0F172A")
TGRID = colors.HexColor("#93C5FD")
C_GREEN = colors.HexColor("#10B981")
C_RED = colors.HexColor("#EF4444")

W, H = A4
MARGIN_L = 1.8 * cm
MARGIN_R = 1.8 * cm
AVAIL = W - MARGIN_L - MARGIN_R
chapter_titles = {}


def S(name, **kw):
    return ParagraphStyle(name, **kw)


chap_title_st = S("ct", fontName=F_BOLD, fontSize=18, textColor=WHITE, leading=24, alignment=TA_LEFT)
chap_num_st = S("cn", fontName=F_BOLD, fontSize=9, textColor=GOLD, leading=13, alignment=TA_LEFT)
sec_st = S("s", fontName=F_BOLD, fontSize=13, textColor=SECONDARY, leading=18,
           spaceBefore=14, spaceAfter=4, alignment=TA_LEFT)
body_st = S("b", fontName=F, fontSize=9.5, textColor=GRAY, leading=17, spaceAfter=9,
            alignment=TA_JUSTIFY)
bullet_st = S("bu", fontName=F, fontSize=9.4, textColor=GRAY, leading=16,
              leftIndent=14, firstLineIndent=-10, spaceAfter=5, alignment=TA_LEFT)
note_st = S("n", fontName=F_ITAL, fontSize=8.5, textColor=GRAY, leading=15,
            leftIndent=10, alignment=TA_JUSTIFY)
th_st = S("th", fontName=F_BOLD, fontSize=8, textColor=WHITE, alignment=TA_CENTER)
td_st = S("td", fontName=F, fontSize=8, textColor=GRAY, leading=12, alignment=TA_LEFT)
td_bold_st = S("tdb", fontName=F_BOLD, fontSize=8, textColor=PRIMARY, leading=12, alignment=TA_LEFT)
code_st = S("co", fontName=F_MONO, fontSize=8, textColor=CODE_FG, backColor=CODE_BG,
            leading=13, leftIndent=8, rightIndent=8, alignment=TA_LEFT)
code_title_st = S("cot", fontName=F_MONOB, fontSize=7.5, textColor=WHITE, backColor=PRIMARY,
                  leading=12, leftIndent=8, alignment=TA_LEFT)


class HFCanvas(pdfcanvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_hf(total)
            pdfcanvas.Canvas.showPage(self)
        pdfcanvas.Canvas.save(self)

    def _draw_hf(self, total):
        pg = self._pageNumber
        self.saveState()
        if pg == 1:
            self.setFillColor(PRIMARY)
            self.rect(0, H - 3.4 * cm, W, 3.4 * cm, fill=1, stroke=0)
            self.setFillColor(ACCENT)
            self.rect(0, H - 3.48 * cm, W, 0.08 * cm, fill=1, stroke=0)
            self.setFillColor(ACCENT)
            self.setFont(F_BOLD, 24)
            self.drawString(MARGIN_L, H - 1.6 * cm, "Guide de Test")
            self.setFillColor(GOLD)
            self.setFont(F_BOLD, 10)
            self.drawString(MARGIN_L, H - 2.2 * cm,
                            "Application Helmet Detection — Validation Production")
            self.setFillColor(colors.HexColor("#94A3B8"))
            self.setFont(F_ITAL, 8)
            self.drawString(MARGIN_L, H - 2.75 * cm,
                            "Salif Biaye, N.A. Diagouraga & Moussa Ndoye — ESP/UCAD 2026")
        else:
            self.setFillColor(LGRAY)
            self.rect(0, H - 1.15 * cm, W, 1.15 * cm, fill=1, stroke=0)
            self.setFillColor(SECONDARY)
            self.setFont(F_BOLD, 8)
            self.drawString(MARGIN_L, H - 0.72 * cm, "Guide de Test")
            self.setFillColor(ACCENT)
            self.setFont(F_BOLD, 6.8)
            self.drawString(MARGIN_L + 2.0 * cm, H - 0.72 * cm, "| Helmet Detection")
            chap = chapter_titles.get(pg, "")
            if chap:
                self.setFillColor(colors.HexColor("#4B6280"))
                self.setFont(F, 6.4)
                self.drawRightString(W - MARGIN_R, H - 0.72 * cm, chap[:76])

        self.setFillColor(PRIMARY)
        self.rect(0, 0, W, 0.95 * cm, fill=1, stroke=0)
        self.setFillColor(ACCENT)
        self.rect(0, 0.95 * cm, W, 0.06 * cm, fill=1, stroke=0)
        self.setFillColor(WHITE)
        self.setFont(F_BOLD, 6.2)
        self.drawString(MARGIN_L, 0.36 * cm, "Salif Biaye, N.A. Diagouraga & Moussa Ndoye — ESP/UCAD 2026")
        if pg > 1:
            self.drawRightString(W - MARGIN_R, 0.36 * cm, f"Page {pg}")
        self.restoreState()


def chap_header(num, title, subtitle=""):
    nc = 4.2 * cm
    row = [[Paragraph(f"SECTION {num}", chap_num_st), Paragraph(title, chap_title_st)]]
    t = Table(row, colWidths=[nc, AVAIL - nc])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PRIMARY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LINEBELOW", (0, 0), (-1, -1), 4, ACCENT),
    ]))
    out = [t]
    if subtitle:
        out += [Spacer(1, 0.3 * cm), Paragraph(subtitle, note_st)]
    out.append(Spacer(1, 0.6 * cm))
    return out


def sec_title(text):
    return [
        Paragraph(text, sec_st),
        HRFlowable(width="100%", thickness=1, color=ACCENT, spaceBefore=2, spaceAfter=4),
    ]


def body(text):
    return [Paragraph(text, body_st)]


def bullet(text):
    return [Paragraph(f"• {text}", bullet_st)]


def th(text):
    return Paragraph(text, th_st)


def td(text, bold=False):
    return Paragraph(str(text), td_bold_st if bold else td_st)


def make_table(headers, rows, col_widths):
    data = [[th(h) for h in headers]]
    for row in rows:
        data.append([td(c, i == 0) for i, c in enumerate(row)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.4, TGRID),
        ("BOX", (0, 0), (-1, -1), 1, TGRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return [t, Spacer(1, 0.35 * cm)]


def synth_box(lines, positive=True):
    bg = colors.HexColor("#ECFDF5") if positive else colors.HexColor("#FEF2F2")
    border = C_GREEN if positive else C_RED
    rows = [[Paragraph(line, S("sy", fontName=F_BOLD if i == 0 else F,
                               fontSize=8.7, textColor=PRIMARY if i == 0 else GRAY,
                               leading=13, alignment=TA_LEFT))]
            for i, line in enumerate(lines)]
    t = Table(rows, colWidths=[AVAIL])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 1, border),
        ("LINEBEFORE", (0, 0), (0, -1), 4, border),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))
    return [KeepTogether(t), Spacer(1, 0.35 * cm)]


def code_block(filename, lines):
    rows = [[Paragraph(f"$  {filename}", code_title_st)]]
    for line in lines:
        rows.append([Paragraph(line.replace(" ", "\u00a0").replace("<", "&lt;").replace(">", "&gt;"), code_st)])
    t = Table(rows, colWidths=[AVAIL])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
        ("TOPPADDING", (0, 0), (0, 0), 7),
        ("BOTTOMPADDING", (0, 0), (0, 0), 5),
        ("TOPPADDING", (0, 1), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("LINEBELOW", (0, 0), (0, 0), 1, ACCENT),
        ("BOX", (0, 0), (-1, -1), 1, SECONDARY),
    ]))
    return [KeepTogether(t), Spacer(1, 0.25 * cm)]


def screen_box(path, caption, max_w=14 * cm, max_h=7.2 * cm):
    cap_st = S("sc", fontName=F_ITAL, fontSize=8.5, textColor=SECONDARY,
               alignment=TA_CENTER, leading=12)
    if not os.path.exists(path):
        return []
    img = RLImage(path)
    ratio = img.imageWidth / img.imageHeight
    w = min(max_w, AVAIL - 0.6 * cm)
    h = w / ratio
    if h > max_h:
        h = max_h
        w = h * ratio
    img.drawWidth, img.drawHeight = w, h
    box = Table([[img], [Paragraph(caption, cap_st)]], colWidths=[w + 0.35 * cm])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.8, TGRID),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return [KeepTogether(box), Spacer(1, 0.3 * cm)]


def cover_page(elements):
    elements.append(Spacer(1, 0.3 * cm))
    if os.path.exists(LOGO_UCAD):
        logo = RLImage(LOGO_UCAD, width=2.1 * cm, height=2.1 * cm)
        lt = Table([[logo]], colWidths=[AVAIL])
        lt.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")]))
        elements.append(lt)
    elements.append(Spacer(1, 0.25 * cm))
    elements.append(Paragraph("UNIVERSITE CHEIKH ANTA DIOP DE DAKAR",
                              S("u", fontName=F_BOLD, fontSize=12, textColor=PRIMARY, alignment=TA_CENTER)))
    elements.append(Paragraph("Ecole Superieure Polytechnique — ESP",
                              S("e", fontName=F_BOLD, fontSize=10, textColor=SECONDARY, alignment=TA_CENTER)))
    elements.append(Spacer(1, 0.35 * cm))
    elements.append(HRFlowable(width="80%", thickness=1, color=TGRID, spaceAfter=0.4 * cm))
    elements.append(Paragraph("Guide de Test",
                              S("t1", fontName=F_BOLD, fontSize=28, textColor=PRIMARY,
                                alignment=TA_CENTER, leading=34)))
    elements.append(Paragraph("Application Helmet Detection",
                              S("t2", fontName=F_BOLD, fontSize=20, textColor=SECONDARY,
                                alignment=TA_CENTER, leading=26)))
    elements.append(Paragraph("Validation de la version deployee en production",
                              S("t3", fontName=F_BOLD, fontSize=10, textColor=ACCENT,
                                alignment=TA_CENTER, leading=15)))
    elements.append(Spacer(1, 0.45 * cm))

    link_box = Table([
        [Paragraph("Lien Production", th_st)],
        [Paragraph(f'<link href="{APP_URL}"><font color="blue"><u>{APP_URL}</u></font></link>',
                   S("ln", fontName=F_BOLD, fontSize=11, textColor=SECONDARY, alignment=TA_CENTER, leading=16))],
        [Paragraph("Documentation API", th_st)],
        [Paragraph(f'<link href="{API_DOCS_URL}"><font color="blue"><u>{API_DOCS_URL}</u></font></link>',
                   S("ln2", fontName=F, fontSize=9.5, textColor=SECONDARY, alignment=TA_CENTER, leading=14))],
    ], colWidths=[AVAIL - 3 * cm])
    link_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("BACKGROUND", (0, 1), (-1, 1), LIGHT),
        ("BACKGROUND", (0, 2), (-1, 2), ACCENT),
        ("BACKGROUND", (0, 3), (-1, 3), LIGHT),
        ("BOX", (0, 0), (-1, -1), 1, TGRID),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    wrap = Table([[link_box]], colWidths=[AVAIL])
    wrap.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    elements.append(wrap)
    elements.append(Spacer(1, 0.45 * cm))

    meta = [
        ["Document :", "Guide de test utilisateur et validation fonctionnelle"],
        ["Contenu :", "Images de test, videos, API, webcam et checklist"],
        ["Dossier :", "projet/test"],
        ["Date :", date.today().strftime("%d/%m/%Y")],
    ]
    mt = Table([[td(a, True), td(b)] for a, b in meta], colWidths=[3.2 * cm, AVAIL - 3.2 * cm])
    mt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), LIGHT),
        ("GRID", (0, 0), (-1, -1), 0.4, TGRID),
        ("BOX", (0, 0), (-1, -1), 1, TGRID),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(mt)
    elements.append(PageBreak())


def section_context(elements, pt):
    pt[2] = "Section 1 — Objectif et contenu du dossier"
    elements += chap_header("1", "Acces a l'Application",
                            "Mode operatoire destine au correcteur pour tester la version deployee")
    elements += body(
        "Ce document explique comment tester l'application Helmet Detection deja deployee en production. "
        "Le correcteur peut ouvrir le lien ci-dessous, utiliser les images et videos fournies dans le dossier "
        "de test, puis verifier les resultats attendus pour les modes image, video, webcam et API."
    )
    elements += synth_box([
        "Application deployee : https://helmet.gdxebec.space/",
        "Fichiers fournis : salif-avec-casque, salif-sans-casque, video-1.mp4 et video-2.mp4.",
        "Objectif : permettre a un correcteur de reproduire les tests sans configuration locale.",
        "Remarque : les tests video/webcam peuvent etre plus fluides en local que sur le VPS de production.",
        "Pre-requis : navigateur web recent, connexion internet et fichiers de test fournis.",
    ])
    elements += sec_title("1.1  Acces direct")
    elements += code_block("Liens utiles", [
        f"Application : {APP_URL}",
        f"Swagger API : {API_DOCS_URL}",
        "Endpoint sante : https://helmet.gdxebec.space/health",
    ])
    elements += screen_box(SCR_APP, "Interface web de l'application deployee", max_h=6.5 * cm)
    elements.append(PageBreak())


def section_tests(elements, pt):
    pt[3] = "Section 2 — Tests fonctionnels"
    elements += chap_header("2", "Tests Fonctionnels",
                            "Validation des modes Image, Video, Webcam et API")

    elements += sec_title("2.1  Test Image — Avec et sans casque")
    for item in [
        "Ouvrir l'application de production dans le navigateur.",
        "Aller dans le mode Image Detection.",
        "Uploader l'image salif-avec-casque puis cliquer sur Run detection.",
        "Verifier l'affichage de l'image annotee, du nombre de detections et du temps d'inference.",
        "Recommencer avec l'image salif-sans-casque pour verifier la detection d'une infraction.",
    ]:
        elements += bullet(item)
    elements += make_table(
        ["Cas", "Resultat attendu"],
        [
            ["Image avec casque", "La detection doit identifier une personne portant un casque."],
            ["Image sans casque", "La detection doit signaler une personne sans casque ou une infraction."],
        ],
        [4.6 * cm, AVAIL - 4.6 * cm],
    )
    elements += screen_box(SCR_DET_H, "Exemple de detection positive : personne avec casque", max_h=5.6 * cm)
    elements += screen_box(SCR_DET_NH, "Exemple de detection negative : personne sans casque", max_h=5.6 * cm)

    elements += sec_title("2.2  Test Video")
    for item in [
        "Ouvrir le mode Video AI Player.",
        "Uploader video-1.mp4 et lancer l'analyse.",
        "Verifier le nombre de frames analysees, le resume des classes et l'aperçu annote.",
        "Recommencer avec video-2.mp4 afin de confirmer la stabilite du traitement.",
    ]:
        elements += bullet(item)
    elements += synth_box([
        "Conseil : privilegier des videos courtes pour une demonstration fluide.",
        "Une video longue augmente naturellement le temps de calcul car plusieurs frames passent dans le modele.",
    ], positive=True)

    elements += sec_title("2.3  Test Webcam et API")
    for item in [
        "Dans le mode Webcam, autoriser l'acces camera lorsque le navigateur le demande.",
        "Cliquer sur Start webcam et verifier que les detections s'affichent sur le flux live.",
        "Ouvrir la documentation API via /docs et tester POST /detect avec une image.",
        "Verifier que la reponse JSON contient detections, count et inference_time_ms.",
    ]:
        elements += bullet(item)
    elements.append(PageBreak())


def section_performance_note(elements, pt):
    pt[4] = "Section 3 — Remarque production"
    elements += chap_header("3", "Remarque Production",
                            "Pourquoi certains tests peuvent etre plus lents sur le lien public")
    elements += synth_box([
        "La version en ligne depend du VPS, du reseau Internet, du reverse proxy, du WebSocket et de l'encodage des frames.",
        "Les modes video et webcam peuvent donc presenter une latence plus visible qu'en local.",
        "Le code source complet est fourni comme livrable pour permettre un test local plus rapide.",
    ], positive=False)
    elements += body(
        "Pour tester l'application dans les conditions les plus directes, le correcteur peut ouvrir un terminal, "
        "entrer dans le dossier du code source fourni, puis lancer Docker Compose. En local, les frames ne transitent "
        "pas par Internet et la reactivite depend principalement des ressources de la machine."
    )
    elements += code_block("Test local depuis le dossier code source", [
        "cd helmet-detection",
        "docker compose up -d",
        "Ouvrir ensuite http://localhost:8081",
    ])
    elements += body(
        "Cette remarque ne remet pas en cause le fonctionnement du modele : elle precise simplement que la production "
        "publique est une demonstration distante, tandis que le livrable code source permet une evaluation locale."
    )
    elements.append(PageBreak())


def section_checklist(elements, pt):
    pt[4] = "Section 3 — Checklist et depannage"
    elements += chap_header("4", "Checklist de Validation",
                            "Points a confirmer avant la demonstration finale")

    elements += make_table(
        ["Point", "Validation attendue"],
        [
            ["Ouverture", "La page de production s'ouvre sans erreur."],
            ["Mode image", "Les deux images retournent une image annotee et une liste de detections."],
            ["Mode video", "Les deux videos produisent un resume exploitable."],
            ["Webcam", "Le flux live demarre apres autorisation du navigateur."],
            ["API", "La documentation /docs est accessible et POST /detect repond."],
            ["Performance", "Le champ inference_time_ms est visible dans les resultats."],
        ],
        [4.0 * cm, AVAIL - 4.0 * cm],
    )

    elements += sec_title("3.1  Depannage rapide")
    elements += make_table(
        ["Symptome", "Cause possible", "Action"],
        [
            ["Page lente au premier acces", "Chargement du modele ou reveil serveur", "Attendre puis recharger la page."],
            ["Upload image refuse", "Format non supporte", "Utiliser JPG, PNG ou WebP."],
            ["Video lente", "Fichier trop long ou trop lourd", "Utiliser une video MP4 courte."],
            ["Webcam bloquee", "Permission navigateur refusee", "Autoriser la camera ou changer de navigateur."],
            ["Erreur API", "Backend temporairement indisponible", "Verifier /health puis reessayer."],
        ],
        [3.9 * cm, 5.1 * cm, AVAIL - 9.0 * cm],
    )
    elements += synth_box([
        "Validation finale : si image, video, webcam et API repondent correctement, la version deployee est fonctionnelle.",
        "Les images et videos fournies permettent de verifier rapidement le comportement attendu de l'application.",
    ])


def closing_page(elements):
    elements.append(PageBreak())
    elements.append(Spacer(1, 2.7 * cm))
    elements.append(Paragraph("Guide de Test",
                              S("cl", fontName=F_BOLD, fontSize=30, textColor=PRIMARY,
                                alignment=TA_CENTER, leading=36)))
    elements.append(Paragraph("Helmet Detection — Application deployee",
                              S("cls", fontName=F_BOLD, fontSize=12, textColor=ACCENT,
                                alignment=TA_CENTER, leading=18)))
    elements.append(Spacer(1, 0.3 * cm))
    elements.append(HRFlowable(width="60%", thickness=2, color=ACCENT, spaceAfter=0.5 * cm))
    info_st = S("inf", fontName=F, fontSize=9, textColor=GRAY, alignment=TA_CENTER, leading=16)
    for line in [
        "UCAD — Ecole Superieure Polytechnique (ESP)",
        "Salif Biaye, Ndeye Astou Diagouraga & Moussa Ndoye",
        "DIC3 Informatique & Telecommunications — Mai 2026",
    ]:
        elements.append(Paragraph(line, info_st))
    elements.append(Spacer(1, 0.45 * cm))
    final = Table([[
        Paragraph("Production<br/>Application Web<br/>FastAPI + Docker",
                  S("fc", fontName=F_BOLD, fontSize=9, textColor=WHITE, leading=14, alignment=TA_CENTER)),
        Paragraph("TEST<br/>Image | Video<br/>Webcam | API",
                  S("fx", fontName=F_BOLD, fontSize=11, textColor=ACCENT, leading=15, alignment=TA_CENTER)),
        Paragraph("Lien<br/>helmet.gdxebec.space<br/>Swagger /docs",
                  S("fd", fontName=F_BOLD, fontSize=9, textColor=WHITE, leading=14, alignment=TA_CENTER)),
    ]], colWidths=[AVAIL * 0.40, AVAIL * 0.20, AVAIL * 0.40])
    final.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#064E3B")),
        ("BACKGROUND", (1, 0), (1, 0), PRIMARY),
        ("BACKGROUND", (2, 0), (2, 0), colors.HexColor("#4C1D95")),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(final)
    elements.append(Spacer(1, 0.35 * cm))
    elements.append(Paragraph(
        f'<link href="{APP_URL}"><font color="blue"><u>{APP_URL}</u></font></link>',
        S("fl", fontName=F_BOLD, fontSize=10, textColor=SECONDARY, alignment=TA_CENTER, leading=14)))


def main():
    os.makedirs(TEST_DIR, exist_ok=True)
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=MARGIN_L,
        rightMargin=MARGIN_R,
        topMargin=3.7 * cm,
        bottomMargin=1.8 * cm,
        title="Guide de Test — Helmet Detection",
        author="Salif Biaye, Ndeye Astou Diagouraga & Moussa Ndoye — ESP/UCAD",
    )
    elements = []
    cover_page(elements)
    section_context(elements, chapter_titles)
    section_tests(elements, chapter_titles)
    section_performance_note(elements, chapter_titles)
    section_checklist(elements, chapter_titles)
    closing_page(elements)
    doc.build(elements, canvasmaker=HFCanvas)
    print(f"PDF genere : {OUTPUT}")


if __name__ == "__main__":
    main()
