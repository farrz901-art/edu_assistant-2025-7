import requests
import json

BASE_URL = "http://localhost:8000/api"

def print_header(title):
    print("\n" + "="*50)
    print(f"  Testing: {title}")
    print("="*50)

def test_assessment_generation():
    """测试教师端 - 考核内容生成"""
    print_header("Teacher - Assessment Generation")
    url = f"{BASE_URL}/ai/generate_assessment/"
    teaching_content = "Python 字典 (Dictionary)是一种无序的键值对集合。键必须是唯一的、不可变类型，例如字符串、数字或元组。请编写一个函数，统计一个字符串中每个字符出现的次数。"
    data = {"teaching_content": teaching_content}
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        result = response.json()
        print("✅  API call successful.")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        is_programming_q = any(q.get('type') == '编程题' for q in result.get('questions', []))
        if is_programming_q:
            print("\n[Validation] ✅  成功生成编程题。")
        else:
            print("\n[Validation] ⚠️  未发现编程题。")

    except requests.exceptions.RequestException as e:
        print(f"❌ API call failed: {e}")

def test_learning_analytics():
    """测试教师端 - 学情数据分析"""
    print_header("Teacher - Learning Analytics")
    url = f"{BASE_URL}/ai/analyze_learning_data/"
    student_practice_history = "[{'question': '什么是字典？', 'student_answer': '一种键值对数据。', 'is_correct': true}]"
    data = {"student_practice_history": student_practice_history}
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        result = response.json()
        print("✅  API call successful.")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        if result.get("knowledge_mastery_summary") and result.get("teaching_suggestions"):
            print("\n[Validation] ✅  成功返回分析总结和教学建议。")
        else:
            print("\n[Validation] ⚠️  返回结果格式不完整。")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API call failed: {e}")

def test_student_assistant():
    """测试学生端 - 在线学习助手"""
    print_header("Student - Learning Assistant (Course Not Found)")
    url = f"{BASE_URL}/ai/ask/"
    data = {"course_id": 999, "question": "这个课程不存在，会发生什么？"}
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 404:
            print("✅  API call successful. Received expected 404 Not Found.")
            print("\n[Validation] ✅  当课程不存在时，接口按预期返回404。")
        else:
            print(f"⚠️  Received unexpected status code: {response.status_code}")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"❌ API call failed: {e}")

def test_practice_evaluation_end_to_end():
    """测试学生端 - 随练题目生成与实时评测 (端到端)"""
    print_header("Student - Practice Generation & Evaluation (End-to-End)")
    
    # Step 1: Generate a practice question to get a valid question_id
    practice_url = f"{BASE_URL}/ai/practice/"
    # 使用一个冷门但明确的主题，以确保AI能够处理
    practice_data = {"topic": "Python的atexit模块", "count": 1}
    question_id = None
    
    try:
        print("  Step 1: Generating a practice question...")
        response = requests.post(practice_url, json=practice_data)
        response.raise_for_status()
        practice_result = response.json()
        questions = practice_result.get("questions")
        
        if not questions or not isinstance(questions, list) or not questions[0].get("id"):
            print("  ❌ Prerequisite failed: Could not generate a valid question with an ID.")
            print(f"  Received: {practice_result}")
            return
        
        question = questions[0]
        question_id = question.get("id")
        print(f"  ✅  Successfully generated question (ID: {question_id})")

    except requests.exceptions.RequestException as e:
        print(f"  ❌ Prerequisite failed: Could not generate question. Error: {e}")
        return

    # Step 2: Evaluate an answer for the generated question
    print("\n  Step 2: Submitting an answer for evaluation...")
    eval_url = f"{BASE_URL}/ai/evaluate/"
    eval_data = {
        "question_id": question_id,
        "answer": "import atexit\n\ndef all_done():\n    print('All done!')\n\natexit.register(all_done)"
    }
    
    try:
        response = requests.post(eval_url, json=eval_data)
        response.raise_for_status()
        eval_result = response.json()
        print("  ✅  API call successful. Evaluation Response:")
        print(json.dumps(eval_result, indent=2, ensure_ascii=False))

        if "score" in eval_result and "feedback" in eval_result:
            print("\n[Validation] ✅  Successfully received evaluation with score and feedback.")
        else:
            print("\n[Validation] ⚠️  Evaluation response is missing 'score' or 'feedback'.")

    except requests.exceptions.RequestException as e:
        print(f"  ❌ API call for evaluation failed: {e}")


if __name__ == "__main__":
    test_assessment_generation()
    test_learning_analytics()
    test_student_assistant()
    test_practice_evaluation_end_to_end()

    # 关于"实时练习评测助手"的分析
    print_header("Analysis: Student - Practice Evaluation")
    print("分析：该功能存在逻辑缺陷。")
    print("原因：随练题目(POST /ai/practice/)生成后直接返回给前端，并未在数据库中创建持久化记录(如存入ExerciseQuestion表)。")
    print("而答案评测(POST /ai/evaluate/)需要一个 'question_id' 来从数据库中查询题目信息。")
    print("由于生成的题目没有ID且不存在于数据库，评测功能将无法找到题目，导致调用失败。")
    print("结论：无法直接测试评测功能，需要先修复后端逻辑。")
    print("="*50) 