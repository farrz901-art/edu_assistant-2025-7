import axios from 'axios';
import { ElMessage } from 'element-plus';

// 创建axios实例
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API || '/api', // url = base url + request url
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 130000 // request timeout
});

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    // 在请求发送之前可以做一些处理（例如添加Authorization头部）
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
service.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    // 错误处理
    if (error.response && error.response.status === 401) {
      // 未授权，跳转到登录页面
      window.location.href = '/login';
    }
    const msg = error.response?.data?.detail || error.message || '请求失败';
    ElMessage.error(msg);
    return Promise.reject(error);
  }
);

export default service;
