// src/utils/users.js
// 假设这里是从本地存储中获取令牌
export const getToken = () => {
  return localStorage.getItem('token');
};

// 可以添加更多认证相关的函数，例如设置令牌、移除令牌等
export const setToken = (token) => {
  localStorage.setItem('token', token);
};

export const removeToken = () => {
  localStorage.removeItem('token');
};