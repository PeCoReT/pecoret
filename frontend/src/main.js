import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { registerPlugins } from '@/plugins';

import PeCoReTAuraPreset from '@/presets/aura';
import PrimeVue from 'primevue/config';

/* primevue services */
import ConfirmationService from 'primevue/confirmationservice';
import ToastService from 'primevue/toastservice';
import DialogService from 'primevue/dialogservice';

import pBreadcrumb from '@/components/Breadcrumb.vue';
import pTabMenu from '@/components/common/TabMenu.vue';

import '@/assets/styles.scss';
import '@/assets/tailwind.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import Form from '@/components/common/forms/Form.vue';
import Field from '@/components/common/forms/Field.vue';
import InlineField from '@/components/common/forms/InlineField.vue';
import InlineFieldGroup from '@/components/common/forms/InlineFieldGroup.vue';
import GenericDataTable from "@/components/common/GenericDataTable.vue";
import ModalDialog from "@/components/common/ModalDialog.vue";

const app = createApp(App);
registerPlugins(app);

app.use(router);
app.use(PrimeVue, {
    theme: {
        preset: PeCoReTAuraPreset,
        options: {
            darkModeSelector: '.app-dark'
        }
    }
});
app.use(ToastService);
app.use(ConfirmationService);
app.use(DialogService);

// COMPONENTS
app.component('pBreadcrumb', pBreadcrumb);
app.component('pTabMenu', pTabMenu);
app.component('GenericDataTable', GenericDataTable);
app.component('ModalDialog', ModalDialog);

// common form components
app.component('Form', Form);
app.component('Field', Field);
app.component('InlineField', InlineField);
app.component('InlineFieldGroup', InlineFieldGroup);

app.mount('#app');
