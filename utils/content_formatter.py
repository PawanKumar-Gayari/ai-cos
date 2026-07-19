"""
Content formatting utilities.
"""

import markdown


class ContentFormatter:

    """
    Convert AI markdown content
    into clean HTML.
    """

    @staticmethod
    def to_html(content):

        """
        Markdown -> HTML
        """

        if not content:
            return ""

        return markdown.markdown(
            content,
            extensions=[
                "tables",
                "fenced_code",
                "toc",
            ],
        )

    @staticmethod
    def clean_markdown(content):

        """
        Cleanup malformed AI markdown.
        """

        if not content:
            return ""

        content = content.replace(
            "\r\n",
            "\n"
        )

        content = content.replace(
            "\r",
            "\n"
        )

        while "\n\n\n" in content:

            content = content.replace(
                "\n\n\n",
                "\n\n"
            )

        return content.strip()