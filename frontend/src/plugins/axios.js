import axios from 'axios';
import router from '@/router';
import { useAuthStore } from '@/store/auth';
import { useMessageStore } from '@/store/messages';
import { apiURL } from '@/app.config';

let api;

export function loadApi(app) {
    api = axios.create({ baseURL: apiURL, withCredentials: true });
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
            if (!error.response) {
                return Promise.reject(error);
            }
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
            if (error.response.status === 404) {
                app.config.globalProperties.$toast.add({
                    severity: 'error',
                    summary: 'Error',
                    life: 3000,
                    detail: 'Received not found error from server!'
                })
            }
            if (error.response.status === 400) {
                if (typeof error.response.data === 'string') {
                    app.config.globalProperties.$toast.add({
                        severity: 'error',
                        summary: `Error`,
                        life: 3000,
                        detail: error.response.data
                    });
                } else {
                    Object.keys(error.response.data).forEach((key) => {
                        const value = error.response.data[key];
                        const item = Array.isArray(value) ? value[0] : value;
                        app.config.globalProperties.$toast.add({
                            severity: 'error',
                            summary: `Error: ${key}`,
                            life: 3000,
                            detail: item
                        });
                    });
                }
            } else if (error.response.status === 429) {
                app.config.globalProperties.$toast.add({
                    severity: 'error',
                    summary: `Error: Request blocked`,
                    life: 3000,
                    detail: error.response.data.detail
                });
            } else if (error.response.status === 500) {
                app.config.globalProperties.$toast.add({
                    severity: 'error',
                    summary: 'Error: Unknown server error',
                    life: 3000,
                    detail: 'Server returned an unknown error'
                })
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
