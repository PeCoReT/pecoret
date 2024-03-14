export default class TechnologyService {
    getTechnologies(api, params) {
        let url = '/technologies/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    createTechnology(api, data) {
        let url = '/technologies/';
        return api.post(url, data);
    }

    deleteTechnology(api, id) {
        let url = `/technologies/${id}/`;
        return api.delete(url);
    }

    patchTechnology(api, id, data) {
        let url = `/technologies/${id}/`;
        return api.patch(url, data);
    }
}
