import { toRaw } from 'vue';

export const listViewMixin = {
    data() {
        return {
            totalRecords: 0,
            pagination: { page: 1, limit: 20 },
            selection: {}
        };
    },
    methods: {
        sort(ev, callback) {
            let params = { ordering: ev.sortField };
            if (ev.sortOrder === -1) {
                params['ordering'] = `-${ev.sortField}`;
            }
            callback(params);
        },
        onPage(page) {
            this.pagination.page = page;
            this.getItems();
        },
        onSearch(query) {
            this.pagination.page = 1;
            if (this.filters && this.filters.search) {
                this.filters.search.value = query;
                this.getItems();
            } else {
                this.getItems({ search: query });
            }
        },
        async bulkDeleteCallback(key, value) {
            // dummy callback
            console.log(`bulk delete callback triggered! ${key}:${value}`);
            return new Promise(() => {});
        },
        bulkDelete(callback) {
            if (!callback) {
                callback = this.bulkDeleteCallback;
            }
            // wrapper around bulk delete operations. the callback will receive a key, value of the selection object
            this.$confirm.require({
                accept: async () => {
                    let itemsDeleted = 0;
                    let totalLength = Object.entries(this.selection).length;
                    for (const [key, value] of Object.entries(this.selection)) {
                        itemsDeleted++;
                        if (value === true) {
                            await callback(key, value).then(() => {
                                if (itemsDeleted === totalLength) {
                                    this.selection = {};
                                    this.getItems();
                                }
                            });
                        }
                    }
                }
            });
        },
        buildParams(pagination, filters, params = {}) {
            if (pagination) {
                params['limit'] = pagination.limit;
                params['page'] = pagination.page;
            }
            if (filters) {
                for (const key in filters) {
                    if (filters[key].value !== null && filters[key].value !== '') {
                        if (Array.isArray(filters[key].value)) {
                            if (!params[key]) {
                                params[key] = [];
                            }
                            params[key].push(...toRaw(filters[key].value)); // Spread operator to add multiple values
                        } else {
                            params[key] = filters[key].value;
                        }
                    }
                }
            }
            return params;
        }
    }
};
