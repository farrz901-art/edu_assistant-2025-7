# ai_integration/prompt_templates.py
PROMPT_TEMPLATES = {
    "course_design": (
        "你是一位经验丰富的{subject}教师，请根据以下课程大纲设计教学内容：\n"
        "### 大纲:\n{syllabus}\n\n"
        "### 要求:\n"
        "1. 包括知识讲解、实训练习和指导\n"
        "2. 合理分配时间（总课时: {total_hours}小时）\n"
        "3. 使用Markdown格式输出\n"
        "4. 包含实际案例和应用场景"
    ),
    "exam_generation": (
        "根据以下教学内容生成考核题目：\n"
        "### 内容:\n{content}\n\n"
        "### 要求:\n"
        "1. 生成{question_count}道题目，包含{question_types}\n"
        "2. 编程题需提供测试用例\n"
        "3. 每题附带参考答案和解析\n"
        "4. 使用JSON格式输出"
    ),
    "question_answering": (
        "你是一位{subject}助教，请回答学生问题：\n"
        "### 学生问题:\n{question}\n\n"
        "### 课程上下文:\n{context}\n\n"
        "### 要求:\n"
        "1. 回答要简洁明了，不超过200字\n"
        "2. 适当使用示例说明\n"
        "3. 如果问题超出课程范围，礼貌提示"
    )
}
