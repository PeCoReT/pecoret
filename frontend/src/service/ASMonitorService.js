import { api } from '@/plugins/axios';

const StatusChoices = [
    {
        name: 'Open',
        value: 'Open'
    },
    {
        name: 'Closed',
        value: 'Closed'
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

export const allowedObjectTypeChoices = [
    {
        label: 'Host',
        value: 'host'
    },
    {
        label: 'Service',
        value: 'service'
    },
    {
        label: 'URL',
        value: 'url'
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

const DataTypeChoices = [
    {
        name: 'IP',
        value: 'IP'
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

    getTargets(params) {
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

    getURLs(params) {
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

    createPort(data) {
        let url = `/attack-surface/ports/`;
        return api.post(url, data);
    }

    patchPort(id, data) {
        let url = `/attack-surface/ports/${id}/`;
        return api.patch(url, data);
    }

    deletePort(id) {
        let url = `/attack-surface/ports/${id}/`;
        return api.delete(url);
    }

    searchServices(params) {
        let url = `/attack-surface/services/search/`;
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    patchService(id, data) {
        let url = `/attack-surface/services/${id}/`;
        return api.patch(url, data);
    }

    createService(data) {
        let url = `/attack-surface/services/`;
        return api.post(url, data);
    }

    getServices(params) {
        let url = `/attack-surface/services/`;
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    getHost(id) {
        let url = `/attack-surface/hosts/${id}/`;
        return api.get(url);
    }

    patchHost(id, data) {
        let url = `/attack-surface/hosts/${id}/`;
        return api.patch(url, data);
    }

    deleteHost(id) {
        let url = `/attack-surface/hosts/${id}/`;
        return api.delete(url);
    }

    getHosts(params) {
        let url = `/attack-surface/hosts/`;
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    getScanners(params) {
        let url = `/attack-surface/scanning/scanners/`;
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    getScanTypes(params) {
        let url = `/attack-surface/scanning/scan-types/`;
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    patchScanType(id, data) {
        let url = `/attack-surface/scanning/scan-types/${id}/`;
        return api.patch(url, data);
    }

    deleteScanType(id) {
        let url = `/attack-surface/scanning/scan-types/${id}/`;
        return api.delete(url);
    }

    createScanType(data) {
        let url = `/attack-surface/scanning/scan-types/`;
        return api.post(url, data);
    }

    createScanner(data) {
        let url = `/attack-surface/scanning/scanners/`;
        return api.post(url, data);
    }

    getScans(params) {
        let url = `/attack-surface/scanning/scans/`;
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    getScan(id) {
        let url = `/attack-surface/scanning/scans/${id}/`;
        return api.get(url);
    }

    createScan(data) {
        let url = `/attack-surface/scanning/scans/`;
        return api.post(url, data);
    }

    patchScanner(id, data) {
        let url = `/attack-surface/scanning/scanners/${id}/`;
        return api.patch(url, data);
    }

    deleteScanner(id) {
        let url = `/attack-surface/scanning/scanners/${id}/`;
        return api.delete(url);
    }
}
