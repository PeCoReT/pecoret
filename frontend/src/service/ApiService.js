import axios from 'axios';
import { apiURL } from '@/app.config';
import { useAuthStore } from '@/store/auth';
import router from '@/router';
import { useMessageStore } from '@/store/messages';
import endpoints from '@/plugins/apiEndpoints';

class ApiService {
    constructor(app) {
        this.client = axios.create({ baseURL: apiURL, withCredentials: true });

        this.e = endpoints;
        this.authStore = useAuthStore();

        // interceptors for requests - X-CSRFToken
        this.client.interceptors.request.use((request) => {
                    const authStore = useAuthStore();

            request.headers['X-CSRFToken'] = authStore.csrfToken;
            return request;
        });

        this.initResponseInterceptors(app);
    }

    updateCSRFToken(data) {
        this.authStore.setAuthData(data);
        this.client.defaults.headers['X-CSRFToken'] = this.authStore.csrfToken;
    }

    initResponseInterceptors(app) {
        this.client.interceptors.response.use(
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
                    });
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
                    });
                }
                return Promise.reject(error);
            }
        );
    }

    _format(endpoint, values) {
        const template = `${endpoint}`;
        // format a string similar to python.format
        return template.replace(/{(\w+)}/g, (_, key) => values[key] ?? `{${key}}`);
    }

    post(endpoint, urlArgs, data, config) {
        let url = this._format(endpoint, urlArgs);
        return this.client.post(url, data, config);
    }

    get(endpoint, urlArgs, params, config) {
        let url = this._format(endpoint, urlArgs);
        if (!config) {
            config = {};
        }
        if (params) {
            config['params'] = params;
        }
        return this.client.get(url, config);
    }

    patch(endpoint, urlArgs, data) {
        let url = this._format(endpoint, urlArgs);
        return this.client.patch(url, data);
    }

    delete(endpoint, urlArgs) {
        let url = this._format(endpoint, urlArgs);
        return this.client.delete(url);
    }
}

export default ApiService;
