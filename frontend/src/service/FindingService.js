import { api } from '@/plugins/axios';

export const statusChoices = [
    { title: 'Open', value: 'Open' },
    { title: 'Fixed', value: 'Fixed' },
    { title: "Won't Fix", value: 'Wont Fix' }
];

export default class FindingService {
    getStatusChoices() {
        return statusChoices;
    }

    getFindings(api, projectId, params) {
        let url = '/projects/' + projectId + '/findings/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    createFinding(api, projectId, data) {
        let url = '/projects/' + projectId + '/findings/';
        return api.post(url, data);
    }

    getFinding(projectId, findingId) {
        let url = '/projects/' + projectId + '/findings/' + findingId + '/';
        return api.get(url);
    }

    deleteFinding(api, projectId, findingId) {
        let url = '/projects/' + projectId + '/findings/' + findingId + '/';
        return api.delete(url);
    }

    patchFinding(api, projectId, findingId, data) {
        let url = '/projects/' + projectId + '/findings/' + findingId + '/';
        return api.patch(url, data);
    }

    getComments(projectId, findingId) {
        let url = '/projects/' + projectId + '/findings/' + findingId + '/comments/';
        return api.get(url);
    }

    createComment(api, projectId, findingId, data) {
        let url = '/projects/' + projectId + '/findings/' + findingId + '/comments/';
        return api.post(url, data);
    }

    patchComment(api, projectId, findingId, commentId, data) {
        let url = `/projects/${projectId}/findings/${findingId}/comments/${commentId}/`;
        return api.patch(url, data);
    }

    getTimeline(projectId, findingId) {
        let url = '/projects/' + projectId + '/findings/' + findingId + '/timelines/';
        return api.get(url);
    }

    downloadAsPDF(api, projectId, findingId) {
        let url = '/projects/' + projectId + '/findings/' + findingId + '/export_pdf/';
        let config = {
            responseType: 'arraybuffer'
        };
        return api.get(url, config);
    }

    findingAsAdvisory(api, projectId, findingId, data) {
        let url = '/projects/' + projectId + '/findings/' + findingId + '/as_advisory/';
        return api.post(url, data);
    }

    copyFinding(api, projectId, findingId, data) {
        let url = '/projects/' + projectId + '/findings/' + findingId + '/copy/';
        return api.post(url, data);
    }

    findingImageAttachmentCreate(api, projectId, findingId, data) {
        let url = '/projects/' + projectId + '/findings/' + findingId + '/attachments/';
        let config = {
            'Content-Type': 'multipart/form-data'
        };
        return api.post(url, data, config);
    }

    findingImageAttachmentList(api, projectId, findingId, params) {
        let url = '/projects/' + projectId + '/findings/' + findingId + '/attachments/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    findingImageAttachmentDelete(api, projectId, findingId, id) {
        let url = '/projects/' + projectId + '/findings/' + findingId + '/attachments/' + id + '/';
        return api.delete(url);
    }
}
