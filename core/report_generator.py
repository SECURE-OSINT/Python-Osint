import json
import os
from datetime import datetime, timezone
from html import escape

from fpdf import FPDF

ALLOWED_RELIABILITY = {"low", "medium", "high", "unknown"}


def load_input(path):
    # FR: Charge un fichier JSON fourni par l utilisateur.
    # EN: Loads a user-provided JSON file.
    if not path:
        return {}
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def write_report(path, html):
    # FR: Ecrit le rapport sur disque en creant le dossier si besoin.
    # EN: Writes the report to disk and creates the folder if needed.
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(html)


def write_pdf_report(path, data):
    # FR: Genere un rapport PDF et l ecrit sur disque.
    # EN: Generates a PDF report and writes it to disk.
    pdf = build_pdf(data)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    pdf.output(path)


def build_report(data):
    # FR: Genere un HTML type "slides" a partir des donnees.
    # EN: Builds a slide-like HTML report from the data.
    safe_data = data if isinstance(data, dict) else {}
    subject = safe_data.get("subject") or {}
    findings = _ensure_list(safe_data.get("findings"))
    sources = _ensure_list(safe_data.get("sources"))
    notes = _ensure_list(safe_data.get("notes"))
    limitations = _ensure_list(safe_data.get("limitations"))
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    if not limitations:
        limitations = [
            {
                "fr": "Donnees basees uniquement sur les informations fournies.",
                "en": "Data is based only on provided information.",
            },
            {
                "fr": "Aucune collecte automatique n a ete effectuee.",
                "en": "No automated collection was performed.",
            },
        ]

    slides = [
        _render_slide(
            "Rapport OSINT (donnees fournies) / OSINT Report (provided data)",
            "".join(
                [
                    _render_bilingual_paragraph(
                        "Rapport genere pour un usage autorise et documente.",
                        "Report generated for authorized, documented use.",
                    ),
                    _render_bilingual_paragraph(
                        "Chaque element doit etre confirme par des sources fiables.",
                        "Each element must be confirmed with reliable sources.",
                    ),
                    f"<p class=\"meta\">Generated: {escape(generated_at)}</p>",
                ]
            ),
        ),
        _render_slide(
            "Identifiants / Identifiers",
            _render_subject_block(subject),
        ),
        _render_slide(
            "Notes / Notes",
            _render_notes_block(notes),
        ),
        _render_slide(
            "Constats / Findings",
            _render_findings_table(findings),
        ),
        _render_slide(
            "Sources / Sources",
            _render_sources_table(sources),
        ),
        _render_slide(
            "Limites / Limitations",
            _render_notes_block(limitations),
        ),
    ]

    return _wrap_html("".join(slides))


def build_pdf(data):
    # FR: Construit un rapport PDF avec des pages type slides.
    # EN: Builds a PDF report with slide-like pages.
    safe_data = data if isinstance(data, dict) else {}
    subject = safe_data.get("subject") or {}
    findings = _ensure_list(safe_data.get("findings"))
    sources = _ensure_list(safe_data.get("sources"))
    notes = _ensure_list(safe_data.get("notes"))
    limitations = _ensure_list(safe_data.get("limitations"))
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    if not limitations:
        limitations = [
            {
                "fr": "Donnees basees uniquement sur les informations fournies.",
                "en": "Data is based only on provided information.",
            },
            {
                "fr": "Aucune collecte automatique n a ete effectuee.",
                "en": "No automated collection was performed.",
            },
        ]

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(18, 18, 18)
    pdf.set_auto_page_break(auto=True, margin=18)

    _pdf_add_slide(pdf, "Rapport OSINT (donnees fournies) / OSINT Report (provided data)")
    _pdf_add_bilingual_paragraph(
        pdf,
        "Rapport genere pour un usage autorise et documente.",
        "Report generated for authorized, documented use.",
    )
    _pdf_add_bilingual_paragraph(
        pdf,
        "Chaque element doit etre confirme par des sources fiables.",
        "Each element must be confirmed with reliable sources.",
    )
    _pdf_add_meta(pdf, f"Generated: {generated_at}")

    _pdf_add_slide(pdf, "Identifiants / Identifiers")
    _pdf_add_subject_block(pdf, subject)

    _pdf_add_slide(pdf, "Notes / Notes")
    _pdf_add_notes_block(pdf, notes)

    _pdf_add_slide(pdf, "Constats / Findings")
    _pdf_add_findings_block(pdf, findings)

    _pdf_add_slide(pdf, "Sources / Sources")
    _pdf_add_sources_block(pdf, sources)

    _pdf_add_slide(pdf, "Limites / Limitations")
    _pdf_add_notes_block(pdf, limitations)

    return pdf


def _wrap_html(slides_html):
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>OSINT Report</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      background: #f2f2f2;
      margin: 0;
      padding: 0;
      color: #1a1a1a;
    }}
    .slide {{
      background: #ffffff;
      width: 960px;
      margin: 32px auto;
      padding: 40px 48px;
      border-radius: 10px;
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
      page-break-after: always;
    }}
    h1, h2 {{
      margin-top: 0;
    }}
    .bilingual .fr {{
      font-weight: 600;
    }}
    .bilingual .en {{
      color: #3d3d3d;
    }}
    .meta {{
      font-size: 12px;
      color: #6b6b6b;
      margin-top: 18px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 12px;
    }}
    th, td {{
      border: 1px solid #dedede;
      padding: 10px 12px;
      text-align: left;
      vertical-align: top;
    }}
    th {{
      background: #f7f7f7;
    }}
    ul {{
      padding-left: 20px;
    }}
    .placeholder {{
      color: #6b6b6b;
    }}
    @media print {{
      body {{
        background: #ffffff;
      }}
      .slide {{
        box-shadow: none;
        margin: 0;
        border-radius: 0;
        width: auto;
        page-break-after: always;
      }}
    }}
  </style>
</head>
<body>
{slides_html}
</body>
</html>"""


def _render_slide(title, content_html):
    return f"""<section class="slide">
  <h1>{escape(title)}</h1>
  {content_html}
</section>"""


def _render_subject_block(subject):
    rows = [
        ("Nom complet / Full name", _text(subject.get("full_name"))),
        ("Email / Email", _text(subject.get("email"))),
        ("Telephone / Phone", _text(subject.get("phone"))),
        ("Pseudo / Username", _text(subject.get("username"))),
    ]
    visible = [(label, value) for label, value in rows if value]
    if not visible:
        return _render_placeholder("Aucune donnee fournie / No data provided.")
    items = "".join(
        f"<li><strong>{escape(label)}:</strong> {escape(value)}</li>"
        for label, value in visible
    )
    return f"<ul>{items}</ul>"


def _render_findings_table(findings):
    if not findings:
        return _render_placeholder("Aucun constat fourni / No findings provided.")
    rows_html = []
    for item in findings:
        category_fr = _text(item.get("category"))
        category_en = _text(item.get("category_en"))
        details_fr = _text(item.get("details"))
        details_en = _text(item.get("details_en"))
        source = _text(item.get("source"))
        reliability = _normalize_reliability(item.get("reliability"))
        rows_html.append(
            "<tr>"
            f"<td>{_render_bilingual_cell(category_fr, category_en)}</td>"
            f"<td>{_render_bilingual_cell(details_fr, details_en)}</td>"
            f"<td>{escape(source) if source else _render_placeholder_inline()}</td>"
            f"<td>{escape(reliability)}</td>"
            "</tr>"
        )
    header = (
        "<tr>"
        "<th>Categorie / Category</th>"
        "<th>Details / Details</th>"
        "<th>Source / Source</th>"
        "<th>Fiabilite / Reliability</th>"
        "</tr>"
    )
    body = "".join(rows_html)
    return f"<table>{header}{body}</table>"


def _render_sources_table(sources):
    if not sources:
        return _render_placeholder("Aucune source fournie / No sources provided.")
    rows_html = []
    for item in sources:
        label_fr = _text(item.get("label"))
        label_en = _text(item.get("label_en"))
        url = _text(item.get("url"))
        reliability = _normalize_reliability(item.get("reliability"))
        notes_fr = _text(item.get("notes"))
        notes_en = _text(item.get("notes_en"))
        rows_html.append(
            "<tr>"
            f"<td>{_render_bilingual_cell(label_fr, label_en)}</td>"
            f"<td>{escape(url) if url else _render_placeholder_inline()}</td>"
            f"<td>{escape(reliability)}</td>"
            f"<td>{_render_bilingual_cell(notes_fr, notes_en)}</td>"
            "</tr>"
        )
    header = (
        "<tr>"
        "<th>Label / Label</th>"
        "<th>URL / URL</th>"
        "<th>Fiabilite / Reliability</th>"
        "<th>Notes / Notes</th>"
        "</tr>"
    )
    body = "".join(rows_html)
    return f"<table>{header}{body}</table>"


def _render_notes_block(items):
    if not items:
        return _render_placeholder("Aucune note fournie / No notes provided.")
    entries = []
    for item in items:
        fr_text, en_text = _coerce_bilingual_item(item)
        entries.append(
            f"<li class=\"bilingual\">"
            f"<div class=\"fr\">FR: {escape(fr_text)}</div>"
            f"<div class=\"en\">EN: {escape(en_text)}</div>"
            f"</li>"
        )
    return f"<ul>{''.join(entries)}</ul>"


def _render_bilingual_paragraph(fr_text, en_text):
    fr_value = fr_text or ""
    en_value = en_text or ""
    return (
        "<p class=\"bilingual\">"
        f"<span class=\"fr\">FR: {escape(fr_value)}</span><br>"
        f"<span class=\"en\">EN: {escape(en_value)}</span>"
        "</p>"
    )


def _render_bilingual_cell(fr_text, en_text):
    fr_value = fr_text or ""
    en_value = en_text or ""
    if not fr_value and not en_value:
        return _render_placeholder_inline()
    fr_value = fr_value or "information non fournie"
    en_value = en_value or "translation not provided"
    return (
        f"<div class=\"fr\">FR: {escape(fr_value)}</div>"
        f"<div class=\"en\">EN: {escape(en_value)}</div>"
    )


def _render_placeholder(message):
    return f"<p class=\"placeholder\">{escape(message)}</p>"


def _render_placeholder_inline():
    return "<span class=\"placeholder\">n/a</span>"


def _ensure_list(value):
    if isinstance(value, list):
        return value
    return []


def _coerce_bilingual_item(item):
    if isinstance(item, dict):
        fr_text = _text(item.get("fr") or item.get("text"))
        en_text = _text(item.get("en") or item.get("text_en"))
    else:
        fr_text = _text(item)
        en_text = ""
    if not fr_text:
        fr_text = "information non fournie"
    if not en_text:
        en_text = "translation not provided"
    return fr_text, en_text


def _normalize_reliability(value):
    raw = _text(value).lower()
    if raw in ALLOWED_RELIABILITY:
        return raw
    return "unknown"


def _text(value):
    if value is None:
        return ""
    return str(value).strip()


def _pdf_add_slide(pdf, title):
    # FR: Ajoute une nouvelle page avec un titre.
    # EN: Adds a new page with a title.
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    _pdf_set_left(pdf)
    pdf.multi_cell(0, 10, _pdf_safe(title))
    pdf.ln(2)


def _pdf_add_meta(pdf, text):
    # FR: Ajoute une ligne meta plus discrete.
    # EN: Adds a lighter meta line.
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(90, 90, 90)
    _pdf_set_left(pdf)
    pdf.multi_cell(0, 5, _pdf_safe(text))
    pdf.set_text_color(0, 0, 0)


def _pdf_add_bilingual_paragraph(pdf, fr_text, en_text):
    # FR: Ajoute un paragraphe bilingue.
    # EN: Adds a bilingual paragraph.
    pdf.set_font("Helvetica", "", 12)
    _pdf_set_left(pdf)
    pdf.multi_cell(0, 6, _pdf_safe(f"FR: {fr_text}"))
    _pdf_set_left(pdf)
    pdf.multi_cell(0, 6, _pdf_safe(f"EN: {en_text}"))
    pdf.ln(1)


def _pdf_add_subject_block(pdf, subject):
    rows = [
        ("Nom complet / Full name", _text(subject.get("full_name"))),
        ("Email / Email", _text(subject.get("email"))),
        ("Telephone / Phone", _text(subject.get("phone"))),
        ("Pseudo / Username", _text(subject.get("username"))),
    ]
    visible = [(label, value) for label, value in rows if value]
    if not visible:
        _pdf_add_placeholder(pdf, "Aucune donnee fournie / No data provided.")
        return
    for label, value in visible:
        _pdf_add_bullet(pdf, f"{label}: {value}")


def _pdf_add_notes_block(pdf, items):
    if not items:
        _pdf_add_placeholder(pdf, "Aucune note fournie / No notes provided.")
        return
    for item in items:
        fr_text, en_text = _coerce_bilingual_item(item)
        _pdf_add_bullet(pdf, f"FR: {fr_text}")
        _pdf_add_bullet(pdf, f"EN: {en_text}")
        pdf.ln(1)


def _pdf_add_findings_block(pdf, findings):
    if not findings:
        _pdf_add_placeholder(pdf, "Aucun constat fourni / No findings provided.")
        return
    for index, item in enumerate(findings, 1):
        pdf.set_font("Helvetica", "B", 12)
        _pdf_set_left(pdf)
        pdf.multi_cell(0, 6, _pdf_safe(f"{index}. Constat / Finding"))
        category_fr = _text(item.get("category"))
        category_en = _text(item.get("category_en"))
        details_fr = _text(item.get("details"))
        details_en = _text(item.get("details_en"))
        source = _text(item.get("source"))
        reliability = _normalize_reliability(item.get("reliability"))
        _pdf_add_bilingual_pair(pdf, "Categorie / Category", category_fr, category_en)
        _pdf_add_bilingual_pair(pdf, "Details / Details", details_fr, details_en)
        _pdf_add_kv_line(pdf, "Source / Source", source or "n/a")
        _pdf_add_kv_line(pdf, "Fiabilite / Reliability", reliability)
        pdf.ln(2)


def _pdf_add_sources_block(pdf, sources):
    if not sources:
        _pdf_add_placeholder(pdf, "Aucune source fournie / No sources provided.")
        return
    for index, item in enumerate(sources, 1):
        pdf.set_font("Helvetica", "B", 12)
        _pdf_set_left(pdf)
        pdf.multi_cell(0, 6, _pdf_safe(f"{index}. Source"))
        label_fr = _text(item.get("label"))
        label_en = _text(item.get("label_en"))
        url = _text(item.get("url"))
        reliability = _normalize_reliability(item.get("reliability"))
        notes_fr = _text(item.get("notes"))
        notes_en = _text(item.get("notes_en"))
        _pdf_add_bilingual_pair(pdf, "Label / Label", label_fr, label_en)
        _pdf_add_kv_line(pdf, "URL / URL", url or "n/a")
        _pdf_add_kv_line(pdf, "Fiabilite / Reliability", reliability)
        _pdf_add_bilingual_pair(pdf, "Notes / Notes", notes_fr, notes_en)
        pdf.ln(2)


def _pdf_add_bilingual_pair(pdf, label, fr_text, en_text):
    fr_value = fr_text or "information non fournie"
    en_value = en_text or "translation not provided"
    pdf.set_font("Helvetica", "B", 11)
    _pdf_set_left(pdf)
    pdf.multi_cell(0, 6, _pdf_safe(label))
    pdf.set_font("Helvetica", "", 11)
    _pdf_set_left(pdf)
    pdf.multi_cell(0, 6, _pdf_safe(f"FR: {fr_value}"))
    _pdf_set_left(pdf)
    pdf.multi_cell(0, 6, _pdf_safe(f"EN: {en_value}"))


def _pdf_add_kv_line(pdf, label, value):
    pdf.set_font("Helvetica", "", 11)
    _pdf_set_left(pdf)
    pdf.multi_cell(0, 6, _pdf_safe(f"{label}: {value}"))


def _pdf_add_bullet(pdf, text):
    pdf.set_font("Helvetica", "", 12)
    _pdf_set_left(pdf)
    pdf.multi_cell(0, 6, _pdf_safe(f"- {text}"))


def _pdf_add_placeholder(pdf, message):
    pdf.set_font("Helvetica", "", 12)
    _pdf_set_left(pdf)
    pdf.multi_cell(0, 6, _pdf_safe(message))


def _pdf_safe(value):
    # FR: Assure une sortie compatible Latin-1 pour FPDF.
    # EN: Ensures Latin-1 compatible output for FPDF.
    text = _text(value)
    return text.encode("latin-1", "replace").decode("latin-1")


def _pdf_set_left(pdf):
    # FR: Repositionne le curseur a la marge gauche.
    # EN: Resets the cursor to the left margin.
    pdf.set_x(pdf.l_margin)
