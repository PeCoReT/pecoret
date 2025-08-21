import { defineStore } from 'pinia';

export const useAuthStore = defineStore('authStore', {
    state: () => ({
        sessionToken: null,
        isAuthenticated: false,
        me: null,
        csrfToken: null,
        groups: {
            isAdmin: false,
            isManagement: false,
            isCustomer: false,
            isPentester: false
        },
        activeProject: {},
        newApiToken: null
    }),
    getters: {},
    actions: {
        setNewApiToken(token) {
            this.newApiToken = token;
        },
        activateProject(project) {
            this.activeProject = project;
        },
        deactivateProject() {
            this.activeProject = {};
        },
        setAuthData(responseData) {
            if (responseData.meta.is_authenticated === false) {
                this.csrfToken = window.csrftoken;
                return;
            }
            this.setMe(responseData.data.user);
            this.isAuthenticated = true;
            this.csrfToken = responseData.data.user.csrf_token;
            if (responseData.meta) {
                this.sessionToken = responseData.meta.session_token;
            }
        },
        unsetMe() {
            this.me = null;
            this.isAuthenticated = false;
        },
        setMe(data) {
            this.me = data;
            this.groups.isAdmin = data.is_superuser;
            data.groups.forEach((item) => {
                if (item.name === 'Management') {
                    this.groups.isManagement = true;
                }
                if (item.name === 'Customer') {
                    this.groups.isCustomer = true;
                }
                if (item.name === 'Pentester') {
                    this.groups.isPentester = true;
                }
            });
        }
    }
});
