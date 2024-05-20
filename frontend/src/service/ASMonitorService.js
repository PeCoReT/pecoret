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

const InScopeChoices = [
    {
        name: 'In Scope',
        value: 'In Scope'
    },
    {
        name: 'Undefined',
        value: 'Undefined'
    },
    {
        name: 'Out of Scope',
        value: 'Out of Scope'
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

    getInScopeChoices() {
        return InScopeChoices;
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
        let url = `/asmonitor/programs/${programId}/targets/`;
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

    getTarget(api, programId, id) {
        let url = `/asmonitor/programs/${programId}/targets/${id}/`;
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
        let url = '/asmonitor/targets/';
        return api.get(url, config);
    }

    getTargetMetas(api, programId, targetId, params) {
        let config = {};
        if (params) {
            config['params'] = params;
        }
        let url = `/asmonitor/programs/${programId}/targets/${targetId}/metas/`;
        return api.get(url, config);
    }

    patchTargetMeta(api, programId, targetId, id, data) {
        let url = `/asmonitor/programs/${programId}/targets/${targetId}/metas/${id}/`;
        return api.patch(url, data);
    }

    createTargetMeta(api, programId, targetId, data) {
        let url = `/asmonitor/programs/${programId}/targets/${targetId}/metas/`;
        return api.post(url, data);
    }

    deleteTargetMeta(api, programId, targetId, id) {
        let url = `/asmonitor/programs/${programId}/targets/${targetId}/metas/${id}/`;
        return api.delete(url);
    }

    getPorts(api, programId, hostId, params) {
        let config = {};
        if (params) {
            config['params'] = params;
        }
        let url = `/asmonitor/programs/${programId}/targets/${hostId}/ports/`;
        return api.get(url, config);
    }

    deletePort(api, programId, hostId, id) {
        let url = `/asmonitor/programs/${programId}/targets/${hostId}/port/${id}/`;
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
        let url = `/asmonitor/programs/${programId}/targets/${hostId}/urls/`;
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
