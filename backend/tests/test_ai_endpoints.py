import json
import pytest
from django.urls import reverse

@pytest.mark.django_db
@pytest.mark.parametrize("url,name,payload_key", [
    ("ai:design-course", "design_course", "syllabus"),
])
def test_course_design(client, url, name, payload_key):
    payload = {
        "syllabus": "测试大纲",
        "knowledge_base_docs": "知识库文档",
    }
    resp = client.post(f"/api/{name.replace('_', '/')}/", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 200
    data = resp.json()
    assert "designed_content" in data 