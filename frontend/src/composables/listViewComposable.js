export function useListViewComposable() {
    function sort(ev, callback) {
        let params = { ordering: ev.sortField };
        if (ev.sortOrder === -1) {
            params['ordering'] = `-${ev.sortField}`;
        }
        callback(params);
    }

    function buildParams(pagination, filters, params) {
        if (!params) {
            params = {};
        }
        if (pagination) {
            params['limit'] = pagination.limit;
            params['page'] = pagination.page;
        }

        if (filters) {
            Object.entries(filters).forEach(([key, { value }]) => {
                params[key] = value;
            });
        }
        return params;
    }

    return { sort, buildParams };
}
