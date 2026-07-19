from apps.keywords.services.page_analyzer_service import PageAnalyzerService

service = PageAnalyzerService()

urls = [
    "https://www.freejobalert.com/",
    "https://www.freejobalert.com/articles/ssc-gd-answer-key-2025-3011862",
    "https://www.shiksha.com/exams/ssc-gd-constable-exam-answer-key",
    "https://www.careerpower.in/",
]

for url in urls:

    print("\n" + "=" * 80)

    print(f"\nTESTING: {url}")

    result = service.analyze(url)

    print("\nBLOCKED:")
    print(result.get("blocked"))

    print("\nIRRELEVANT:")
    print(result.get("irrelevant"))

    print("\nTITLE:")
    print(result.get("title"))

    print("\nHEADINGS:")
    print(result.get("headings"))

    print("\nWORD COUNT:")
    print(result.get("word_count"))
