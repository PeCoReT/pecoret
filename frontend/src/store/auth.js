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
        activeProject: {}
    }),
    getters: {},
    actions: {
        activateProject(project) {
            this.activeProject = project;
        },
        deactivateProject() {
            this.activeProject = {};
        },
        setAuthDataOld(responseData) {
            this.csrfToken = responseData.csrf_token;
            if (responseData.user) {
                this.setMe(responseData.user);
                this.isAuthenticated = true;
            }
        },
        setAuthData(responseData) {
            if (responseData.meta.is_authenticated === false ) {
                this.csrfToken = window.csrftoken;
                return
            }
            // old stuff - authcheck not yet ported to /session
            if (responseData.meta && responseData.meta.is_authenticated !== true) {
                this.setAuthDataOld(responseData);
                return null;
            }
            if (!responseData.data){
                this.setAuthDataOld(responseData)
                return null
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
