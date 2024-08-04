import {api} from '@/plugins/axios';


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

    getAdvisories(params) {
        let url = '/advisories/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    createAdvisory(data) {
        let url = '/advisories/';
        return api.post(url, data);
    }

    getAdvisory(advisoryId) {
        let url = `/advisories/${advisoryId}/`;
        return api.get(url);
    }

    patchAdvisory(advisoryId, data) {
        let url = `/advisories/${advisoryId}/`;
        return api.patch(url, data);
    }

    deleteAdvisory(advisoryId) {
        let url = `/advisories/${advisoryId}/`;
        return api.delete(url);
    }

    downloadAdvisoryAsPDF(advisoryId, params) {
        let url = `/advisories/${advisoryId}/export_pdf/`;
        let config = {
            responseType: 'arraybuffer'
        };
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    getTimeline(advisoryId) {
        let url = `/advisories/${advisoryId}/timelines/`;
        let config = {
            params: {
                limit: 100
            }
        };
        return api.get(url, config);
    }

    createTimeline(advisoryId, data) {
        let url = `/advisories/${advisoryId}/timelines/`;
        return api.post(url, data);
    }

    deleteTimeline(advisoryId, id) {
        let url = `/advisories/${advisoryId}/timelines/${id}/`;
        return api.delete(url);
    }

    getComments(advisoryId) {
        let url = `/advisories/${advisoryId}/comments/`;
        return api.get(url);
    }

    createComment(advisoryId, data) {
        let url = `/advisories/${advisoryId}/comments/`;
        return api.post(url, data);
    }

    patchComment(advisoryId, commentId, data) {
        let url = `/advisories/${advisoryId}/comments/${commentId}/`;
        return api.patch(url, data);
    }


    getImageAttachments(advisoryId, params) {
        let url = `/advisories/${advisoryId}/attachments/`;
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    attachmentCreate(advisoryId, data) {
        let url = `/advisories/${advisoryId}/attachments/`;
        return api.post(url, data);
    }

    deleteAttachment(advisoryId, id) {
        let url = `/advisories/${advisoryId}/attachments/${id}/`;
        return api.delete(url);
    }

    getLabels(params) {
        let url = '/advisory-labels/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    createLabel(data) {
        let url = '/advisory-labels/';
        return api.post(url, data);
    }

    deleteLabel(id) {
        let url = `/advisory-labels/${id}/`;
        return api.delete(url);
    }

    patchLabel(id, data) {
        let url = `/advisory-labels/${id}/`;
        return api.patch(url, data);
    }

    getBaseInformationStatistics() {
        let url = '/advisories/statistics/base-information/';
        return api.get(url);
    }

    getTopSubmittersStatistic() {
        let url = '/advisories/statistics/top-submitters/';
        return api.get(url);
    }

    getTopVulnerabilitiesStatistics() {
        let url = '/advisories/statistics/top-vulnerabilities/';
        return api.get(url);
    }

    getTopProductsStatistics() {
        let url = '/advisories/statistics/top-products/';
        return api.get(url);
    }

    getTopVendorsStatistics() {
        let url = '/advisories/statistics/top-vendors/';
        return api.get(url);
    }
}
