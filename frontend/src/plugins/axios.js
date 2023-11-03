import axios from 'axios';
import router from '@/router';
import { useAuthStore } from '@/store/auth';
import { useMessageStore } from '@/store/messages';
import { apiURL } from '@/app.config';

const api = axios.create({ baseURL: apiURL, withCredentials: true });

export function loadApi(app) {
    api.interceptors.request.use(function (request) {
        const authStore = useAuthStore();
        request.headers['X-CSRFToken'] = authStore.csrfToken;
        return request;
    });

    api.interceptors.response.use(
        function (response) {
            return response;
        },
        function (error) {
            if (error.response.status === 401) {
                app.config.globalProperties.$toast.add({
                    severity: 'error',
                    summary: 'Unauthorized',
                    life: 3000,
                    detail: error.response.data.detail
                });
                router.push({ name: 'Login' });
            }
            if (error.response.status === 403) {
                if (error.response.data.detail === 'Authentication credentials were not provided.') {
                    router.push({ name: 'Login' });
                }
                app.config.globalProperties.$toast.add({
                    severity: 'error',
                    summary: 'Unauthenticated',
                    life: 3000,
                    detail: error.response.data.detail
                });
                const messageStore = useMessageStore();
                messageStore.addMessage(error.response.data.detail, 'error');
            }
            if (error.response.status === 400) {
                app.config.globalProperties.$toast.add({
                    severity: 'error',
                    summary: 'Error',
                    life: 3000,
                    detail: error.response.data
                });
            }
            return Promise.reject(error);
        }
    );

    api.interceptors.request.use(function (request) {
        const authStore = useAuthStore();
        request.headers['X-CSRFToken'] = authStore.csrfToken;
        return request;
    });

    app.config.globalProperties.$api = api;
}

export { api };
