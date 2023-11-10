export default class ProjectNoteService {
    getNotes(api, projectId, params) {
        let url = '/projects/' + projectId + '/notes/';
        let config = {
            limit: 300
        };
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    createNote(api, projectId, data) {
        let url = '/projects/' + projectId + '/notes/';
        return api.post(url, data);
    }

    deleteNote(api, projectId, id) {
        let url = '/projects/' + projectId + '/notes/' + id + '/';
        return api.delete(url);
    }

    getNote(api, projectId, id) {
        let url = '/projects/' + projectId + '/notes/' + id + '/';
        return api.get(url);
    }

    patchNote(api, projectId, id, data) {
        let url = '/projects/' + projectId + '/notes/' + id + '/';
        return api.patch(url, data);
    }

    lockNote(api, projectId, id) {
        let url = '/projects/' + projectId + '/notes/' + id + '/lock/';
        return api.post(url, {});
    }

    unlockNote(api, projectId, id) {
        let url = '/projects/' + projectId + '/notes/' + id + '/unlock/';
        return api.delete(url, {});
    }
}
