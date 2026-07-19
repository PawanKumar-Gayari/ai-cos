"""
SEO validation engine.
"""


class SEOValidator:

    def validate(
        self,
        parsed_content,
        keyword=""
    ):

        # =========================
        # INITIAL SCORE
        # =========================

        score = 0

        checks = []

        # =========================
        # EXTRACT CONTENT
        # =========================

        seo_title = parsed_content.get(
            "seo_title",
            ""
        )

        meta_description = parsed_content.get(
            "meta_description",
            ""
        )

        article = parsed_content.get(
            "article",
            ""
        )

        faq = parsed_content.get(
            "faq",
            ""
        )

        conclusion = parsed_content.get(
            "conclusion",
            ""
        )

        full_content = f"""

        {seo_title}

        {meta_description}

        {article}

        {faq}

        {conclusion}
        """

        # =========================
        # TITLE CHECK
        # =========================

        if seo_title:

            score += 15

            checks.append(
                "SEO title present"
            )

        # =========================
        # META DESCRIPTION CHECK
        # =========================

        if meta_description:

            score += 15

            checks.append(
                "Meta description present"
            )

        # =========================
        # FAQ CHECK
        # =========================

        if faq:

            score += 10

            checks.append(
                "FAQ section present"
            )

        # =========================
        # CONCLUSION CHECK
        # =========================

        if conclusion:

            score += 10

            checks.append(
                "Conclusion present"
            )

        # =========================
        # CONTENT LENGTH CHECK
        # =========================

        word_count = len(
            article.split()
        )

        if word_count >= 1000:

            score += 20

            checks.append(
                "Content length optimized"
            )

        elif word_count >= 500:

            score += 10

            checks.append(
                "Content length acceptable"
            )

        # =========================
        # KEYWORD CHECK
        # =========================

        if keyword:

            keyword_count = (
                full_content.lower().count(
                    keyword.lower()
                )
            )

            if keyword_count >= 5:

                score += 15

                checks.append(
                    "Keyword optimization good"
                )

            elif keyword_count >= 2:

                score += 8

                checks.append(
                    "Keyword optimization average"
                )

        # =========================
        # HEADING CHECK
        # =========================

        heading_checks = [

            "h1",
            "h2",
            "##",
            "#",
        ]

        if any(

            heading.lower()
            in article.lower()

            for heading in heading_checks
        ):

            score += 15

            checks.append(
                "Heading structure present"
            )

        # =========================
        # FINAL SCORE
        # =========================

        score = min(score, 100)

        # =========================
        # RETURN RESULT
        # =========================

        return {

            "seo_score": score,

            "checks": checks,

            "word_count": word_count,

            "keyword_count": (
                full_content.lower().count(
                    keyword.lower()
                )
                if keyword else 0
            ),
        }