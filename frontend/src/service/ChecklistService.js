export default class ChecklistService {
    getChecklists(api, params) {
        let url = '/checks/checklists/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    deleteAssetChecklist(api, projectId, checkId) {
        let url = '/projects/' + projectId + '/checklists/' + checkId + '/';
        return api.delete(url);
    }

    createAssetChecklist(api, projectId, data) {
        let url = '/projects/' + projectId + '/checklists/';
        return api.post(url, data);
    }

    getAssetChecklists(api, projectId, params) {
        let url = '/projects/' + projectId + '/checklists/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    getAssetCategories(api, projectId, params) {
        let url = '/projects/' + projectId + '/checklist-categories/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    getAssetItems(api, projectId, params) {
        let url = '/projects/' + projectId + '/checklist-items/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    patchAssetItem(api, projectId, itemId, data) {
        let url = '/projects/' + projectId + '/checklist-items/' + itemId + '/';
        return api.patch(url, data);
    }

    getItems(api, params) {
        let url = '/checks/items/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    getCategories(api, params) {
        let url = '/checks/categories/';
        let config = {};
        if (params) {
            config['params'] = params;
        }
        return api.get(url, config);
    }

    deleteCategory(api, id) {
        let url = `/checks/categories/${id}/`;
        return api.delete(url);
    }

    createChecklist(api, data) {
        let url = '/checks/checklists/';
        return api.post(url, data);
    }

    deleteChecklist(api, id) {
        let url = `/checks/checklists/${id}/`;
        return api.delete(url);
    }

    getChecklist(api, id) {
        let url = `/checks/checklists/${id}/`;
        return api.get(url);
    }

    patchChecklist(api, id, data) {
        let url = `/checks/checklists/${id}/`;
        return api.patch(url, data);
    }

    getCategory(api, id) {
        let url = `/checks/categories/${id}/`;
        return api.get(url);
    }

    patchItem(api, id, data) {
        let url = `/checks/items/${id}/`;
        return api.patch(url, data);
    }

    deleteItem(api, id) {
        let url = `/checks/items/${id}/`;
        return api.delete(url);
    }

    createItem(api, data) {
        let url = `/checks/items/`;
        return api.post(url, data);
    }

    createCategory(api, data) {
        let url = '/checks/categories/';
        return api.post(url, data);
    }
}
