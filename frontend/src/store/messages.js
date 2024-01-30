import { defineStore } from 'pinia';

export const useMessageStore = defineStore('messageStore', {
    state: () => ({
        messages: []
    }),
    actions: {
        addMessage(message, alertType) {
            let index = this.messages.findIndex((a) => a.message === message);
            if (index === -1) {
                this.messages.push({ message: message, type: alertType });
            }
        },
        deleteMessage(message) {
            let index = this.messages.findIndex((a) => a.message === message.message);
            if (index > -1) {
                this.messages.splice(index, 1);
            }
        }
    }
});
