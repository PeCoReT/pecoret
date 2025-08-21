// globalApi.js
import ApiService from '@/service/ApiService';

export default {
    install(app) {
        // Add api client as $api to Vue's global properties
        app.config.globalProperties.$api = new ApiService(app);
    }
};
