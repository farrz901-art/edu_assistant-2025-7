<!-- frontend/src/views/Auth/Register.vue -->

<template>
    <div class="auth-container">
        <h1>用户注册</h1>
        <form @submit.prevent="handleSubmit">
            <input v-model="username" type="text" placeholder="用户名" required />
            <input v-model="password" type="password" placeholder="密码" required />
            <select v-model="role" required>
                <option value="student">学生</option>
                <option value="teacher">教师</option>
                <option value="admin">管理员</option>
            </select>
            <button type="submit">注册</button>
        </form>
    </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
    data() {
        return {
            username: '',
            password: '',
            role: 'student', // 默认角色为学生
        };
    },
    methods: {
        ...mapActions(['register']),
        async handleSubmit() {
            const userData = {
                username: this.username,
                password: this.password,
                role: this.role
            };
            try {
                await this.register(userData);
                this.$router.push('/login'); // 注册成功后跳转到登录页面
            } catch (error) {
                console.error("注册失败", error);
            }
        },
    },
};
</script>

<style scoped>
.auth-container {
    max-width: 400px;
    margin: 50px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
}

form {
    display: flex;
    flex-direction: column;
}

input, select, button {
    margin: 10px 0;
    padding: 10px;
    font-size: 14px;
    border-radius: 4px;
    border: 1px solid #ddd;
}

button {
    background-color: #4CAF50;
    color: white;
    cursor: pointer;
}

button:hover {
    background-color: #45a049;
}
</style>
