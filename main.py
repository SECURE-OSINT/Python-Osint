import argparse
import os
import sys

# Allow local module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.report_generator import build_report, load_input, write_report


def _parse_pipe_fields(raw, expected_parts):
    # FR: Decoupe une chaine "a|b|c" en un nombre fixe de champs.
    # EN: Splits an "a|b|c" string into a fixed number of fields.
    parts = [part.strip() for part in raw.split("|")]
    if len(parts) < expected_parts:
        parts.extend([""] * (expected_parts - len(parts)))
    if len(parts) > expected_parts:
        head = parts[: expected_parts - 1]
        tail = "|".join(parts[expected_parts - 1 :])
        parts = head + [tail]
    return parts


def _coerce_list(value):
    if isinstance(value, list):
        return value
    return []


def _build_data(args):
    # FR: Construit la structure de donnees pour le rapport.
    # EN: Builds the data structure used by the report.
    data = load_input(args.input)
    subject = data.get("subject") if isinstance(data, dict) else {}
    if not isinstance(subject, dict):
        subject = {}

    if args.full_name:
        subject["full_name"] = args.full_name
    if args.email:
        subject["email"] = args.email
    if args.phone:
        subject["phone"] = args.phone
    if args.username:
        subject["username"] = args.username

    data = data if isinstance(data, dict) else {}
    data["subject"] = subject

    findings = _coerce_list(data.get("findings"))
    if args.finding:
        for raw in args.finding:
            category, category_en, details, details_en, source, reliability = _parse_pipe_fields(
                raw, 6
            )
            findings.append(
                {
                    "category": category,
                    "category_en": category_en,
                    "details": details,
                    "details_en": details_en,
                    "source": source,
                    "reliability": reliability,
                }
            )
    data["findings"] = findings

    sources = _coerce_list(data.get("sources"))
    if args.source:
        for raw in args.source:
            label, label_en, url, reliability, notes, notes_en = _parse_pipe_fields(raw, 6)
            sources.append(
                {
                    "label": label,
                    "label_en": label_en,
                    "url": url,
                    "reliability": reliability,
                    "notes": notes,
                    "notes_en": notes_en,
                }
            )
    data["sources"] = sources

    notes = _coerce_list(data.get("notes"))
    if args.note:
        for raw in args.note:
            fr_text, en_text = _parse_pipe_fields(raw, 2)
            notes.append({"fr": fr_text, "en": en_text})
    data["notes"] = notes

    limitations = _coerce_list(data.get("limitations"))
    if args.limitation:
        for raw in args.limitation:
            fr_text, en_text = _parse_pipe_fields(raw, 2)
            limitations.append({"fr": fr_text, "en": en_text})
    data["limitations"] = limitations

    return data


def _parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Generate a slide-style OSINT report from user-provided data."
        )
    )
    parser.add_argument("--input", help="Path to JSON input file.")
    parser.add_argument(
        "--output",
        default="reports/report.html",
        help="Output HTML report path (default: reports/report.html).",
    )
    parser.add_argument("--full-name", help="Subject full name.")
    parser.add_argument("--email", help="Subject email address.")
    parser.add_argument("--phone", help="Subject phone number.")
    parser.add_argument("--username", help="Subject username / handle.")
    parser.add_argument(
        "--finding",
        action="append",
        help=(
            "Add a finding: category|category_en|details|details_en|source|reliability."
        ),
    )
    parser.add_argument(
        "--source",
        action="append",
        help="Add a source: label|label_en|url|reliability|notes|notes_en.",
    )
    parser.add_argument(
        "--note",
        action="append",
        help="Add a note: fr_text|en_text.",
    )
    parser.add_argument(
        "--limitation",
        action="append",
        help="Add a limitation: fr_text|en_text.",
    )
    return parser.parse_args()


def main():
    args = _parse_args()
    data = _build_data(args)
    html = build_report(data)
    write_report(args.output, html)
    print(f"Report written to: {args.output}")
    print("FR: Aucune collecte automatique n a ete effectuee.")
    print("EN: No automated collection was performed.")


if __name__ == "__main__":
    main()
