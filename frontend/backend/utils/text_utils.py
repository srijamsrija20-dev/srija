import html
import re


def sanitize_text(text: str) -> str:

    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\u00a0": " ",
        "\ufeff": ""
    }

    for old, new in replacements.items():

        text = text.replace(
            old,
            new
        )

    text = text.replace(
        "\r\n",
        "\n"
    )

    text = text.replace(
        "\r",
        "\n"
    )

    return text.strip()


def split_terms(terms: str):

    return [
        item.strip()
        for item in terms.split(";")
        if item.strip()
    ]


def format_html_preview(text: str):

    safe_text = html.escape(
        sanitize_text(text)
    )

    safe_text = re.sub(
        r"\*\*(.+?)\*\*",
        r"<strong>\1</strong>",
        safe_text
    )

    safe_text = safe_text.replace(
        "\n",
        "<br>"
    )

    return safe_text