const confirmPlugin = {
    install(app) {
        app.config.globalProperties.$confirm = {
            dialog: null,

            require(options) {
                app.config.globalProperties.$showConfirmDialog(options);
            }
        };
    }
};

export default confirmPlugin;
