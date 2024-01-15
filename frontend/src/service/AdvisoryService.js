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

export const VisibilityChoices = [
    {
        label: 'Members',
        value: 'Members'
    },
    {
        label: 'Team',
        value: 'Team'
    }
];

export default class AdvisoryService {
    getStatusChoices() {
        return AdvisoryStatusChoices;
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

    downloadAdvisoryAsMarkdown(api, advisoryId) {
        let url = '/advisories/' + advisoryId + '/export_markdown/';
        let config = {
            responseType: 'arraybuffer'
        };
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

    getMemberships(api, advisoryId, params) {
        let url = '/advisories/' + advisoryId + '/memberships/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    deleteMembership(api, advisoryId, memberId) {
        let url = '/advisories/' + advisoryId + '/memberships/' + memberId + '/';
        return api.delete(url);
    }

    createMembership(api, advisoryId, data) {
        let url = '/advisories/' + advisoryId + '/memberships/';
        return api.post(url, data);
    }

    getImageAttachments(api, advisoryId, params) {
        let url = '/advisories/' + advisoryId + '/attachments/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    createProof(api, advisoryId, data) {
        let url = '/advisories/' + advisoryId + '/proofs/';
        let config = {};
        if (data.image) {
            config['Content-Type'] = 'multipart/form-data';
        }
        return api.post(url, data, config);
    }

    patchProof(api, advisoryId, proofId, data) {
        let url = '/advisories/' + advisoryId + '/proofs/' + proofId + '/';
        return api.patch(url, data);
    }

    attachmentPatch(api, advisoryId, id, data) {
        let url = '/advisories/' + advisoryId + '/attachments/' + id + '/';
        return api.patch(url, data);
    }

    attachmentCreate(api, advisoryId, data) {
        let url = '/advisories/' + advisoryId + '/attachments/';
        return api.post(url, data);
    }

    getProof(api, advisoryId, proofId) {
        let url = '/advisories/' + advisoryId + '/proofs/' + proofId + '/';
        return api.get(url);
    }

    deleteAttachment(api, advisoryId, id) {
        let url = '/advisories/' + advisoryId + '/attachments/' + id + '/';
        return api.delete(url);
    }

    getLabels(api, params) {
        let url = '/advisory-management/labels/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    createLabel(api, data) {
        let url = '/advisory-management/labels/';
        return api.post(url, data);
    }

    deleteLabel(api, id) {
        let url = '/advisory-management/labels/' + id + '/';
        return api.delete(url);
    }

    patchLabel(api, id, data) {
        let url = '/advisory-management/labels/' + id + '/';
        return api.patch(url, data);
    }

    getInboxStatistics(api) {
        let url = '/advisory-management/inbox/inbox_statistics/';
        return api.get(url);
    }

    getTopSubmitters(api) {
        let url = '/advisory-management/inbox/top_submitters/';
        return api.get(url);
    }

    getTopVulnerabilities(api) {
        let url = '/advisory-management/inbox/top_vulnerabilities/';
        return api.get(url);
    }

    getTopProducts(api) {
        let url = '/advisory-management/inbox/top_products/';
        return api.get(url);
    }

    getTopVendors(api) {
        let url = '/advisory-management/inbox/top_vendors/';
        return api.get(url);
    }
}
