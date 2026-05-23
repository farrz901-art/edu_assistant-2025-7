// frontend/src/api/users.js

import axios from 'axios';

export const userApi = {
    register(userData) {
        // userData 应该包含 username, password, role
        return axios.post('/api/users/register/', userData);
    },
    login(credentials) {
        // credentials 应该包含 username, password
        return axios.post('/api/users/login/', credentials);
    },
// {{ edit_1 }}
//     getProfile() {
//         return axios.get('/api/users/profile/');
//     }
};

