export default class ASMonitorService {
    getPrograms(api, params) {
        let url = '/asmonitor/programs/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    createProgram(api, data) {
        let url = '/asmonitor/programs/';
        return api.post(url, data);
    }

    getProgram(api, id) {
        let url = `/asmonitor/programs/${id}/`;
        return api.get(url);
    }

    deleteProgram(api, id) {
        let url = `/asmonitor/programs/${id}/`;
        return api.delete(url);
    }

    getTags(api, params) {
        let url = '/asmonitor/tags/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    deleteTag(api, id) {
        let url = `/asmonitor/tags/${id}/`;
        return api.delete(url);
    }

    createTag(api, data) {
        let url = '/asmonitor/tags/';
        return api.post(url, data);
    }

    getTargets(api, programId, params) {
        let url = `/asmonitor/programs/${programId}/targets/`;
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    createTarget(api, programId, data) {
        let url = `/asmonitor/programs/${programId}/targets/`;
        return api.post(url, data);
    }

    deleteTarget(api, programId, id) {
        let url = `/asmonitor/programs/${programId}/targets/${id}/`;
        return api.delete(url);
    }

    patchTarget(api, programId, id, data) {
        let url = `/asmonitor/programs/${programId}/targets/${id}/`;
        return api.patch(url, data);
    }

    getFindings(api, programId, params) {
        let url = `/asmonitor/programs/${programId}/findings/`;
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    createFinding(api, programId, data) {
        let url = `/asmonitor/programs/${programId}/findings/`;
        return api.post(url, data);
    }

    getFinding(api, programId, id) {
        let url = `/asmonitor/programs/${programId}/findings/${id}/`;
        return api.get(url);
    }

    deleteFinding(api, programId, id) {
        let url = `/asmonitor/programs/${programId}/findings/${id}/`;
        return api.delete(url);
    }

    patchFinding(api, programId, id, data) {
        let url = `/asmonitor/programs/${programId}/findings/${id}/`;
        return api.patch(url, data);
    }

    getGlobalFindings(api, params) {
        let config = {};
        if (params) {
            config['params'] = params;
        }
        let url = '/asmonitor/findings/';
        return api.get(url, config);
    }
}
