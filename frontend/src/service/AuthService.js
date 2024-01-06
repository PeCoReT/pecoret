import { useAuthStore } from '@/store/auth';

export default class AuthService {
    checkAuth(api) {
        const authStore = useAuthStore();
        let url = '/auth/check/';
        api.get(url).then((response) => {
            authStore.setAuthData(response.data);
        });
    }

    login(api, username, password) {
        const authStore = useAuthStore();
        authStore.unsetMe();
        let url = '/auth/login/';
        let data = { username: username, password: password };
        return api.post(url, data);
    }

    logout(api) {
        const authStore = useAuthStore();
        authStore.unsetMe();
        let url = '/auth/logout/';
        return api.post(url, {});
    }

    resetPassword(api, data) {
        let url = '/users/reset_password/';
        return api.post(url, data);
    }

    activateAccount(api, data) {
        let url = '/users/activation/';
        return api.post(url, data);
    }
}
