import { api } from '@/plugins/axios';

export default class ProjectService {
    getProjects(api, params) {
        let url = '/projects/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    getProject(projectId) {
        let url = `/projects/${projectId}/`;
        return api.get(url);
    }

    getProjectMembershipMe(projectId) {
        let url = `/projects/${projectId}/memberships/me`;
        return api.get(url);
    }

    getProjectMemberships(api, projectId, params) {
        let url = `/projects/${projectId}/memberships/`;
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    createProject(api, data) {
        let url = '/projects/';
        return api.post(url, data);
    }

    deleteProject(api, id) {
        let url = `/projects/${id}/`;
        return api.delete(url);
    }

    patchProject(api, projectId, data) {
        let url = `/projects/${projectId}/`;
        return api.patch(url, data);
    }

    pinProject(api, projectId, data) {
        let url = `/projects/${projectId}/pin_project/`;
        if (data === true) {
            return api.post(url, data);
        }
        return api.delete(url);
    }

    getContacts(api, projectId, params) {
        let url = `/projects/${projectId}/contacts/`;
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    createContact(api, projectId, data) {
        let url = `/projects/${projectId}/contacts/`;
        return api.post(url, data);
    }

    deleteContact(api, projectId, contactId) {
        let url = `/projects/${projectId}/contacts/${contactId}/`;
        return api.delete(url);
    }

    getLanguages(api) {
        let url = '/projects/available-languages/';
        return api.get(url);
    }

    getProjectFiles(api, projectId, params) {
        let url = `/projects/${projectId}/files/`;
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    downloadProjectFile(api, projectId, file_id) {
        let url = `/projects/${projectId}/files/${file_id}/download/`;
        let config = {
            responseType: 'arraybuffer'
        };
        return api.get(url, config);
    }

    deleteProjectFile(api, projectId, id) {
        let url = `/projects/${projectId}/files/${id}/`;
        return api.delete(url);
    }

    createProjectFile(api, projectId, data) {
        let url = `/projects/${projectId}/files/`;
        let filedata = new FormData();
        filedata.append('name', data.name);
        filedata.append('file', data.file);
        return api.post(url, filedata);
    }
}
