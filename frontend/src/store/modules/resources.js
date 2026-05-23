import api from "@/api";

export default {
  namespaced: true,
  state: {
    resources: [],
    pagination: {
      current: 1,
      total: 0,
      pageSize: 10
    },
    loading: false
  },
  mutations: {
    SET_RESOURCES(state, { results, count }) {
      state.resources = results;
      state.pagination.total = count;
    },
    SET_LOADING(state, loading) {
      state.loading = loading;
    },
    SET_PAGINATION(state, pagination) {
      state.pagination = { ...state.pagination, ...pagination };
    }
  },
  actions: {
    async fetchResources({ commit, state }, params = {}) {
      commit('SET_LOADING', true);
      try {
        const response = await api.resources.list({
          ...params,
          page: state.pagination.current,
          page_size: state.pagination.pageSize
        });
        commit('SET_RESOURCES', response.data);
      } catch (error) {
        console.error('获取资源失败:', error);
      } finally {
        commit('SET_LOADING', false);
      }
    },
    async uploadResource({ dispatch }, formData) {
      try {
        await api.resources.upload(formData);
        dispatch('fetchResources');
        return true;
      } catch (error) {
        console.error('上传资源失败:', error);
        return false;
      }
    },
    async deleteResource({ dispatch }, id) {
      try {
        await api.resources.delete(id);
        dispatch('fetchResources');
        return true;
      } catch (error) {
        console.error('删除资源失败:', error);
        return false;
      }
    },
    async bulkDeleteResources({ dispatch }, ids) {
      try {
        await api.resources.bulkDelete(ids);
        dispatch('fetchResources');
        return true;
      } catch (error) {
        console.error('批量删除失败:', error);
        return false;
      }
    }
  }
};