import { useToast } from '@/components/ui/toast/use-toast';

export default {
    install(app) {
        const { toast } = useToast();
        app.config.globalProperties.$toaster = toast;
    }
};
