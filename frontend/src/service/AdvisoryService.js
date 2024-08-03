export const AdvisoryStatusChoices = [
    {
        label: 'Disclosed',
        value: 'Disclosed'
    },
    {
        label: 'Not Disclosed',
        value: 'Not Disclosed'
    }
];

export const VulnerabilityStatusChoices = [
    {
        label: 'Unfixed',
        value: 'Unfixed'
    },
    {
        label: 'Fixed',
        value: 'Fixed'
    },
    {
        label: "Won't fix",
        value: "Won't fix"
    }
];


export default class AdvisoryService {
    getStatusChoices() {
        return AdvisoryStatusChoices;
    }

    getVulnerabilityStatusChoices(){
        return VulnerabilityStatusChoices;
    }

    getAdvisories(api, params) {
        let url = '/advisories/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    createAdvisory(api, data) {
        let url = '/advisories/';
        return api.post(url, data);
    }

    getAdvisory(api, advisoryId) {
        let url = '/advisories/' + advisoryId + '/';
        return api.get(url);
    }

    patchAdvisory(api, advisoryId, data) {
        let url = '/advisories/' + advisoryId + '/';
        return api.patch(url, data);
    }

    deleteAdvisory(api, advisoryId) {
        let url = '/advisories/' + advisoryId + '/';
        return api.delete(url);
    }

    downloadAdvisoryAsPDF(api, advisoryId, params) {
        let url = '/advisories/' + advisoryId + '/export_pdf/';
        let config = {
            responseType: 'arraybuffer'
        };
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    getInbox(api, params) {
        let url = '/advisory-management/inbox/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    getTimeline(api, advisoryId) {
        let url = '/advisories/' + advisoryId + '/timelines/';
        let config = {
            params: {
                limit: 100
            }
        };
        return api.get(url, config);
    }

    createTimeline(api, advisoryId, data) {
        let url = '/advisories/' + advisoryId + '/timelines/';
        return api.post(url, data);
    }

    deleteTimeline(api, advisoryId, id) {
        let url = '/advisories/' + advisoryId + '/timelines/' + id + '/';
        return api.delete(url);
    }

    getComments(api, advisoryId) {
        let url = '/advisories/' + advisoryId + '/comments/';
        return api.get(url);
    }

    createComment(api, advisoryId, data) {
        let url = '/advisories/' + advisoryId + '/comments/';
        return api.post(url, data);
    }

    patchComment(api, advisoryId, commentId, data) {
        let url = '/advisories/' + advisoryId + '/comments/' + commentId + '/';
        return api.patch(url, data);
    }


    getImageAttachments(api, advisoryId, params) {
        let url = '/advisories/' + advisoryId + '/attachments/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    attachmentCreate(api, advisoryId, data) {
        let url = '/advisories/' + advisoryId + '/attachments/';
        return api.post(url, data);
    }

    deleteAttachment(api, advisoryId, id) {
        let url = '/advisories/' + advisoryId + '/attachments/' + id + '/';
        return api.delete(url);
    }

    getLabels(api, params) {
        let url = '/advisory-labels/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    createLabel(api, data) {
        let url = '/advisory-labels/';
        return api.post(url, data);
    }

    deleteLabel(api, id) {
        let url = `/advisory-labels/${id}/`;
        return api.delete(url);
    }

    patchLabel(api, id, data) {
        let url = `/advisory-labels/${id}/`;
        return api.patch(url, data);
    }

    getBaseInformationStatistics(api) {
        let url = '/advisories/statistics/base-information/';
        return api.get(url);
    }

    getTopSubmittersStatistic(api) {
        let url = '/advisories/statistics/top-submitters/';
        return api.get(url);
    }

    getTopVulnerabilitiesStatistics(api) {
        let url = '/advisories/statistics/top-vulnerabilities/';
        return api.get(url);
    }

    getTopProductsStatistics(api) {
        let url = '/advisories/statistics/top-products/';
        return api.get(url);
    }

    getTopVendorsStatistics(api) {
        let url = '/advisories/statistics/top-vendors/';
        return api.get(url);
    }
}
