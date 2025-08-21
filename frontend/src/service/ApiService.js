import axios from 'axios';
import { useAuthStore } from '@/store/auth';
import router from '@/router';
import endpoints from '@/plugins/apiEndpoints';

class ApiService {
    constructor(app) {
        this.client = axios.create({ baseURL: window.API_BASE_URL, withCredentials: true });

        this.e = endpoints;
        this.authStore = useAuthStore();

        // interceptors for requests - X-CSRFToken
        this.client.interceptors.request.use((request) => {
            const authStore = useAuthStore();

            request.headers['X-CSRFToken'] = authStore.csrfToken;
            request.headers['X-Session-Token'] = authStore.sessionToken;
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
                    if (error.response.data.meta && error.response.data.data) {
                        // allauth views may return 401 in /session and logout
                    } else {
                        app.config.globalProperties.$toaster({
                            title: 'Unauthorized',
                            duration: 3000,
                            description: error.response.data.detail
                        });
                    }

                    // TODO: fix me: handle unauth routes but currentRoute.value is always "/"
                    // router.push({ name: 'Login' });
                    return Promise.resolve({
                        status: 401,
                        data: error.response.data
                    });
                }
                if (error.response.status === 403) {
                    if (error.response.data.detail === 'Authentication credentials were not provided.') {
                        router.push({ name: 'Login' });
                    }
                    app.config.globalProperties.$toaster({
                        title: 'Unauthenticated',
                        duration: 3000,
                        description: error.response.data.detail
                    });
                }
                if (error.response.status === 404) {
                    app.config.globalProperties.$toaster({
                        title: 'Error',
                        duration: 3000,
                        description: 'Received not found error from server!'
                    });
                }
                if (error.response.status === 400) {
                    if (typeof error.response.data === 'string') {
                        app.config.globalProperties.$toaster({
                            title: `Error`,
                            duration: 3000,
                            description: error.response.data
                        });
                    } else {
                        Object.keys(error.response.data).forEach((key) => {
                            const value = error.response.data[key];
                            const item = Array.isArray(value) ? value[0] : value;
                            app.config.globalProperties.$toaster({
                                title: `Error: ${key}`,
                                duration: 3000,
                                description: item
                            });
                        });
                    }
                } else if (error.response.status === 429) {
                    app.config.globalProperties.$toaster({
                        title: `Error: Request blocked`,
                        duration: 3000,
                        description: error.response.data.detail
                    });
                } else if (error.response.status === 500) {
                    app.config.globalProperties.$toaster({
                        title: 'Error: Unknown server error',
                        duration: 3000,
                        description: 'Server returned an unknown error'
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
