export const paramMixin = {
    methods: {
        initFromUrl() {
            const query = this.$route.query;

            // Update pagination from query if available
            if (query.page) {
                this.pagination.page = parseInt(query.page, 10) || 1;
            }
            if (query.limit) {
                this.pagination.limit = parseInt(query.limit, 10) || 25;
            }

            // Update filters dynamically
            if (this.filters) {
                for (const [key, filterObj] of Object.entries(this.filters)) {
                    if (query[key] !== undefined) {
                        // Handle array-type query params correctly
                        if (Array.isArray(filterObj.value)) {
                            this.filters[key].value = Array.isArray(query[key]) ? query[key] : [query[key]];
                        } else {
                            this.filters[key].value = query[key];
                        }
                    }
                }
            }
        },
        buildQueryParamsFromState() {
            const params = {};

            if (this.pagination) {
                if (this.pagination.page) params.page = this.pagination.page;
                if (this.pagination.limit) params.limit = this.pagination.limit;
            }

            if (this.filters) {
                for (const [key, filterObj] of Object.entries(this.filters)) {
                    const rawValue = filterObj.value;
                    if (rawValue !== null && rawValue !== '' && (Array.isArray(rawValue) ? rawValue.length : true)) {
                        params[key] = rawValue;
                    }
                }
            }

            return params;
        },
        updateRouteQuery() {
            const newQuery = this.buildQueryParamsFromState();

            this.$router
                .replace({
                    path: this.$route.path,
                    query: newQuery
                })
                .catch((err) => {
                    if (err.name !== 'NavigationDuplicated') {
                        console.error(err);
                    }
                });
        }
    },
    watch: {
        pagination: {
            handler() {
                this.updateRouteQuery();
            },
            deep: true
        },
        filters: {
            handler() {
                this.updateRouteQuery();
            },
            deep: true
        }
    }
};
