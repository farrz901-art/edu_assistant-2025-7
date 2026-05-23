<template>
    <div class="home-container">
        <h1>欢迎来到教育助手平台！</h1>
        <p>请选择您的身份进入系统：</p>
        <div class="role-buttons">
            <router-link to="/admin" class="btn admin-btn">我是管理员</router-link>
            <router-link to="/teacher" class="btn teacher-btn">我是教师</router-link>
            <router-link to="/student" class="btn student-btn">我是学生</router-link>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Home'
}
</script>

<style scoped>
.home-container {
    max-width: 600px;
    margin: 50px auto;
    padding: 30px;
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    text-align: center;
    background-color: #fff;
    font-family: 'Arial', sans-serif;
}

h1 {
    color: #333;
    font-size: 2.5em;
    margin-bottom: 20px;
}

p {
    color: #666;
    font-size: 1.2em;
    margin-bottom: 30px;
}

.role-buttons {
    display: flex;
    justify-content: space-around;
    gap: 20px;
    margin-top: 30px;
}

.btn {
    display: inline-block;
    padding: 15px 25px;
    font-size: 1.1em;
    font-weight: bold;
    text-decoration: none;
    color: white;
    border-radius: 8px;
    transition: background-color 0.3s ease, transform 0.2s ease;
    min-width: 150px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.btn:hover {
    transform: translateY(-3px);
}

.admin-btn {
    background-color: #f44336; /* Red */
}
.admin-btn:hover {
    background-color: #d32f2f;
}

.teacher-btn {
    background-color: #2196f3; /* Blue */
}
.teacher-btn:hover {
    background-color: #1976d2;
}

.student-btn {
    background-color: #4CAF50; /* Green */
}
.student-btn:hover {
    background-color: #388e3c;
}
</style>
