import service from "@/utils/request";

export default {
  list: (params) => service.get('/resources/', { params }),
  detail: (id) => service.get(`/resources/${id}/`),
  create: (data) => service.post('/resources/', data),
  update: (id, data) => service.put(`/resources/${id}/`, data),
  delete: (id) => service.delete(`/resources/${id}/`),
  bulkDelete: (ids) => service.delete('/resources/bulk_delete/', { data: { ids } }),
  download: (id) => service.get(`/resources/${id}/download/`, { responseType: 'blob' }),
  export: (ids) => service.post('/resources/export/', { ids }, { responseType: 'blob' }),
  upload: (formData) => service.post('/resources/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  newVersion: (id, file) => {
    const formData = new FormData();
    formData.append('file', file);
    return service.post(`/resources/${id}/new_version/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  }
};