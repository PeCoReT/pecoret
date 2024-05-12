const StatusChoices = [
    {
        name: 'Open',
        value: 'Open'
    },
    {
        name: 'Fixed',
        value: 'Fixed'
    },
    {
        name: 'Wont Fix',
        value: 'Wont Fix'
    }
];

const SeverityChoices = [
    {
        name: 'Critical',
        value: 'Critical'
    },
    {
        name: 'High',
        value: 'High'
    },
    {
        name: 'Medium',
        value: 'Medium'
    },
    {
        name: 'Low',
        value: 'Low'
    },
    {
        name: 'Informational',
        value: 'Informational'
    }
];

const ScopeTypeChoices = [
    {
        name: 'IP',
        value: 'IP'
    },
    {
        name: 'Network',
        value: 'Network'
    },
    {
        name: 'Domain',
        value: 'Domain'
    },
    {
        name: 'Wildcard',
        value: 'Wildcard'
    },
    {
        name: 'Subdomain',
        value: 'Subdomain'
    }
];

export default class ASMonitorService {
    getStatusChoices() {
        return StatusChoices;
    }

    getSeverityChoices() {
        return SeverityChoices;
    }

    getScopeTypeChoices() {
        return ScopeTypeChoices;
    }

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

    patchProgram(api, id, data) {
        let url = `/asmonitor/programs/${id}/`;
        return api.patch(url, data);
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
        let url = `/asmonitor/programs/${programId}/hosts/`;
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    patchTag(api, id, data) {
        let url = `/asmonitor/tags/${id}/`;
        return api.patch(url, data);
    }

    createTarget(api, programId, data) {
        let url = `/asmonitor/programs/${programId}/hosts/`;
        return api.post(url, data);
    }

    deleteTarget(api, programId, id) {
        let url = `/asmonitor/programs/${programId}/hosts/${id}/`;
        return api.delete(url);
    }

    patchTarget(api, programId, id, data) {
        let url = `/asmonitor/programs/${programId}/hosts/${id}/`;
        return api.patch(url, data);
    }

    getTarget(api, programId, id) {
        let url = `/asmonitor/programs/${programId}/hosts/${id}/`;
        return api.get(url);
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

    getFindingsByDateStats(api, programId) {
        let url = `/asmonitor/programs/${programId}/stats_findings_by_date/`;
        return api.get(url);
    }

    getGlobalTargets(api, params) {
        let config = {};
        if (params) {
            config['params'] = params;
        }
        let url = '/asmonitor/hosts/';
        return api.get(url, config);
    }

    getTargetMetas(api, programId, targetId, params) {
        let config = {};
        if (params) {
            config['params'] = params;
        }
        let url = `/asmonitor/programs/${programId}/hosts/${targetId}/metas/`;
        return api.get(url, config);
    }

    patchTargetMeta(api, programId, targetId, id, data) {
        let url = `/asmonitor/programs/${programId}/hosts/${targetId}/metas/${id}/`;
        return api.patch(url, data);
    }

    createTargetMeta(api, programId, targetId, data) {
        let url = `/asmonitor/programs/${programId}/hosts/${targetId}/metas/`;
        return api.post(url, data);
    }

    deleteTargetMeta(api, programId, targetId, id) {
        let url = `/asmonitor/programs/${programId}/hosts/${targetId}/metas/${id}/`;
        return api.delete(url);
    }

    getHostnames(api, programId, hostId, params) {
        let config = {};
        if (params) {
            config['params'] = params;
        }
        let url = `/asmonitor/programs/${programId}/hosts/${hostId}/hostnames/`;
        return api.get(url, config);
    }

    deleteHostname(api, programId, hostId, id) {
        let url = `/asmonitor/programs/${programId}/hosts/${hostId}/hostnames/${id}/`;
        return api.delete(url);
    }

    getPorts(api, programId, hostId, params) {
        let config = {};
        if (params) {
            config['params'] = params;
        }
        let url = `/asmonitor/programs/${programId}/hosts/${hostId}/ports/`;
        return api.get(url, config);
    }

    deletePort(api, programId, hostId, id) {
        let url = `/asmonitor/programs/${programId}/hosts/${hostId}/port/${id}/`;
        return api.delete(url);
    }

    getGlobalURLs(api, params) {
        let config = {};
        if (params) {
            config['params'] = params;
        }
        let url = `/asmonitor/urls/`;
        return api.get(url, config);
    }

    getURLs(api, programId, hostId, params) {
        let config = {};
        if (params) {
            config['params'] = params;
        }
        let url = `/asmonitor/programs/${programId}/hosts/${hostId}/urls/`;
        return api.get(url, config);
    }

    getScopes(api, programId, params) {
        let config = {};
        if (params) {
            config['params'] = params;
        }
        let url = `/asmonitor/programs/${programId}/scopes/`;
        return api.get(url, config);
    }

    deleteScope(api, programId, id) {
        let url = `/asmonitor/programs/${programId}/scopes/${id}/`;
        return api.delete(url);
    }

    createScope(api, programId, data) {
        let url = `/asmonitor/programs/${programId}/scopes/`;
        return api.post(url, data);
    }
}
