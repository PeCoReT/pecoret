<script>
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from '@/components/ui/alert-dialog';
import { getCurrentInstance} from "vue";

export default {
    name: 'ConfirmDialog',
    components: {
        AlertDialog,
        AlertDialogAction,
        AlertDialogCancel,
        AlertDialogContent,
        AlertDialogDescription,
        AlertDialogFooter,
        AlertDialogHeader,
        AlertDialogTitle,
        AlertDialogTrigger
    },
    data() {
        return {
            visible: false,
            message: null,
        }
    },
    mounted() {
      const app = getCurrentInstance().appContext.app;
      app.config.globalProperties.$showConfirmDialog = this.show
    },
    methods: {
        show(options) {
            this.visible = true;
            this.title = options.title || 'Confirm';
            this.message = options.message || 'This action can not be reversed!'
            this.acceptCallback = options.accept || (() => {});
            this.rejectCallback = options.reject || (() => {})
        },
        accept() {
            if(this.acceptCallback) this.acceptCallback();
            this.visible = false;
        },
        reject() {
            if (this.rejectCallback) this.rejectCallback();
            this.visible = false
        },
    }
};
</script>

<template>
    <AlertDialog v-model:open="visible">
        <AlertDialogContent>
            <AlertDialogHeader>
                <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
                <AlertDialogDescription> {{ message }} </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogFooter>
                <AlertDialogCancel @click="reject">Cancel</AlertDialogCancel>
                <AlertDialogAction @click="accept">Continue</AlertDialogAction>
            </AlertDialogFooter>
        </AlertDialogContent>
    </AlertDialog>
</template>
