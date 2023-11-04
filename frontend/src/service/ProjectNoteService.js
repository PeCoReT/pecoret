export default class ProjectNoteService {
    getNotes(api, projectId, params) {
        let url = '/projects/' + projectId + '/notes/';
        let config = {};
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

    patchNote(api, projectId, id, data) {
        let url = '/projects/' + projectId + '/notes/' + id + '/';
        return api.patch(url, data);
    }
}
