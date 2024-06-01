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
        name: 'Subdomain',
        value: 'Subdomain'
    }
];

const DataTypeChoices = [
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

    getDataTypeChoices() {
        return DataTypeChoices;
    }

    getScopeTypeChoices() {
        return ScopeTypeChoices;
    }

    getPrograms(api, params) {
        let url = '/attack-surface/programs/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    createProgram(api, data) {
        let url = '/attack-surface/programs/';
        return api.post(url, data);
    }

    getProgram(api, id) {
        let url = `/attack-surface/programs/${id}/`;
        return api.get(url);
    }

    patchProgram(api, id, data) {
        let url = `/attack-surface/programs/${id}/`;
        return api.patch(url, data);
    }

    deleteProgram(api, id) {
        let url = `/attack-surface/programs/${id}/`;
        return api.delete(url);
    }

    getTags(api, params) {
        let url = '/attack-surface/tags/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    deleteTag(api, id) {
        let url = `/attack-surface/tags/${id}/`;
        return api.delete(url);
    }

    createTag(api, data) {
        let url = '/attack-surface/tags/';
        return api.post(url, data);
    }

    patchTag(api, id, data) {
        let url = `/attack-surface/tags/${id}/`;
        return api.patch(url, data);
    }

    getTargets(api, params) {
        let url = `/attack-surface/targets/`;
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    createTarget(api, data) {
        let url = `/attack-surface/targets/`;
        return api.post(url, data);
    }

    deleteTarget(api, id) {
        let url = `/attack-surface/targets/${id}/`;
        return api.delete(url);
    }

    patchTarget(api, id, data) {
        let url = `/attack-surface/targets/${id}/`;
        return api.patch(url, data);
    }

    getScanFindings(api, params) {
        let url = `/attack-surface/scan-findings/`;
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    deleteScanFinding(api, id) {
        let url = `/attack-surface/scan-findings/${id}/`;
        return api.delete(url);
    }

    createScanFinding(api, data) {
        let url = `/attack-surface/scan-findings/`;
        return api.post(url, data);
    }

    patchScanFinding(api, id, data) {
        let url = `/attack-surface/scan-findings/${id}/`;
        return api.patch(url, data);
    }

    getScanFinding(api, id) {
        let url = `/attack-surface/scan-findings/${id}/`;
        return api.get(url);
    }

    getPorts(api, params) {
        let config = {};
        if (params) {
            config['params'] = params;
        }
        let url = `/attack-surface/ports/`;
        return api.get(url, config);
    }

    deletePort(api, programId, hostId, id) {
        let url = `/asmonitor/programs/${programId}/targets/${hostId}/port/${id}/`;
        return api.delete(url);
    }

    getURLs(api, params) {
        let config = {};
        if (params) {
            config['params'] = params;
        }
        let url = `/attack-surface/urls/`;
        return api.get(url, config);
    }

    getURL(api, pk) {
        let url = `/attack-surface/urls/${pk}/`;
        return api.get(url);
    }

    patchURL(api, pk, data) {
        let url = `/attack-surface/urls/${pk}/`;
        return api.patch(url, data);
    }

    deleteURL(api, id) {
        let url = `/attack-surface/urls/${id}/`;
        return api.delete(url);
    }

    createURL(api, data) {
        let url = `/attack-surface/urls/`;
        return api.post(url, data);
    }
}
