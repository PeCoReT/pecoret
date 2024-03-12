import { defineStore } from 'pinia';

export const useASMonitorStore = defineStore('asMonitorStore', {
    state: () => ({
        activeProgram: {}
    }),
    getters: {},
    actions: {
        activateProgram(program) {
            this.activeProgram = program;
        },
        deactivateProgram() {
            this.activeProgram = {};
        }
    }
});
