export default class AssetService {
    getWebApplications(api, projectId, params) {
        let url = '/projects/' + projectId + '/web-applications/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    createWebApplication(api, projectId, data) {
        let url = '/projects/' + projectId + '/web-applications/';
        return api.post(url, data);
    }

    deleteWebApplication(api, projectId, assetId) {
        let url = '/projects/' + projectId + '/web-applications/' + assetId + '/';
        return api.delete(url);
    }

    getWebApplication(api, projectId, assetId) {
        let url = '/projects/' + projectId + '/web-applications/' + assetId + '/';
        return api.get(url);
    }

    patchWebApplication(api, projectId, assetId, data) {
        let url = '/projects/' + projectId + '/web-applications/' + assetId + '/';
        return api.patch(url, data);
    }

    getHosts(api, projectId, params) {
        let url = '/projects/' + projectId + '/hosts/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    createHost(api, projectId, data) {
        let url = '/projects/' + projectId + '/hosts/';
        return api.post(url, data);
    }

    getHost(api, projectId, assetId) {
        let url = '/projects/' + projectId + '/hosts/' + assetId + '/';
        return api.get(url);
    }

    deleteHost(api, projectId, hostId) {
        let url = '/projects/' + projectId + '/hosts/' + hostId + '/';
        return api.delete(url);
    }

    patchHost(api, projectId, hostId, data) {
        let url = '/projects/' + projectId + '/hosts/' + hostId + '/';
        return api.patch(url, data);
    }

    getServices(api, projectId, params) {
        let url = '/projects/' + projectId + '/services/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    createService(api, projectId, data) {
        let url = '/projects/' + projectId + '/services/';
        return api.post(url, data);
    }

    deleteService(api, projectId, assetId) {
        let url = '/projects/' + projectId + '/services/' + assetId + '/';
        return api.delete(url);
    }

    getService(api, projectId, assetId) {
        let url = '/projects/' + projectId + '/services/' + assetId + '/';
        return api.get(url);
    }

    patchService(api, projectId, assetId, data) {
        let url = '/projects/' + projectId + '/services/' + assetId + '/';
        return api.patch(url, data);
    }

    getMobileApplications(api, projectId, params) {
        let url = '/projects/' + projectId + '/mobile-applications/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    deleteMobileApplication(api, projectId, id) {
        let url = '/projects/' + projectId + '/mobile-applications/' + id + '/';
        return api.delete(url);
    }

    createMobileApplication(api, projectId, data) {
        let url = '/projects/' + projectId + '/mobile-applications/';
        return api.post(url, data);
    }

    getMobileApplication(api, projectId, id) {
        let url = '/projects/' + projectId + '/mobile-applications/' + id + '/';
        return api.get(url);
    }

    patchMobileApplication(api, projectId, id, data) {
        let url = '/projects/' + projectId + '/mobile-applications/' + id + '/';
        return api.patch(url, data);
    }

    getThickClients(api, projectId, params) {
        let url = '/projects/' + projectId + '/thick-clients/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    createThickClient(api, projectId, data) {
        let url = '/projects/' + projectId + '/thick-clients/';
        return api.post(url, data);
    }

    getThickClient(api, projectId, id) {
        let url = '/projects/' + projectId + '/thick-clients/' + id + '/';
        return api.get(url);
    }

    deleteThickClient(api, projectId, id) {
        let url = '/projects/' + projectId + '/thick-clients/' + id + '/';
        return api.delete(url);
    }

    patchThickClient(api, projectId, id, data) {
        let url = '/projects/' + projectId + '/thick-clients/' + id + '/';
        return api.patch(url, data);
    }

    getGenericAssets(api, projectId, params) {
        let url = `/projects/${projectId}/generic-assets/`;
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    deleteGenericAsset(api, projectId, id) {
        let url = `/projects/${projectId}/generic-assets/${id}/`;
        return api.delete(url);
    }

    createGenericAsset(api, projectId, data) {
        let url = `/projects/${projectId}/generic-assets/`;
        return api.post(url, data);
    }

    getGenericAsset(api, projectId, id) {
        let url = `/projects/${projectId}/generic-assets/${id}/`;
        return api.get(url);
    }

    patchGenericAsset(api, projectId, id, data) {
        let url = `/projects/${projectId}/generic-assets/${id}/`;
        return api.patch(url, data);
    }
}
