import { defineStore } from 'pinia';

export const useAuthStore = defineStore('authStore', {
    state: () => ({
        authToken: '',
        isAuthenticated: false,
        me: null,
        csrfToken: null,
        groups: {
            isAdmin: false,
            isManagement: false,
            isAdvisoryManagement: false,
            isVendor: false,
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
        setAuthData(responseData) {
            this.csrfToken = responseData.csrf_token;
            if (responseData.user) {
                this.setMe(responseData.user);
                this.isAuthenticated = true;
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
                if (item.name === 'Advisory Management') {
                    this.groups.isAdvisoryManagement = true;
                }
                if (item.name === 'Vendor') {
                    this.groups.isVendor = true;
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
