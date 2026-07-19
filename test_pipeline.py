import json
import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from apps.keywords.services.pipeline_service import (
    KeywordPipelineService,
)

service = KeywordPipelineService()

queries = [
    "ssc gd answer key pdf",
    "ugc net result 2026",
    "gate chemistry syllabus",
    "reet admit card",
    "iit jam chemistry",
]

for query in queries:
    print("\n" + "=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    result = service.run(query)

    print(json.dumps(result, indent=2, default=str))
