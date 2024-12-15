import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { registerPlugins } from '@/plugins';

import PrimeVue from 'primevue/config';
import ConfirmationService from 'primevue/confirmationservice';
import ToastService from 'primevue/toastservice';
import DialogService from 'primevue/dialogservice';

import pBreadcrumb from '@/components/Breadcrumb.vue';
import pTabMenu from '@/components/common/TabMenu.vue';

import '@/assets/styles.scss';
import '@/assets/tailwind.css';
import '@/assets/index.css';
import '@fortawesome/fontawesome-free/css/all.min.css';

import Form from '@/components/common/forms/Form.vue';
import Field from '@/components/common/forms/Field.vue';
import InlineField from '@/components/common/forms/InlineField.vue';
import InlineFieldGroup from '@/components/common/forms/InlineFieldGroup.vue';
import GenericDataTable from '@/components/common/GenericDataTable.vue';
import ModalDialog from '@/components/common/ModalDialog.vue';
import BaseLayout from '@/layout/base/BaseLayout.vue';
import BaseListLayout from '@/layout/base/BaseListLayout.vue';
import Select from 'primevue/select';

import loadPreset from '@/utils/preset';

import {
    Accordion,
    AccordionTab,
    Button, ButtonGroup,
    Card,
    Checkbox, ColorPicker,
    Column,
    ConfirmDialog,
    DatePicker,
    Dialog, FileUpload, IconField,
    InputGroup, InputIcon, InputNumber,
    InputText, Listbox, Message,
    MultiSelect, Paginator, Password, PickList, SelectButton,
    Skeleton,
    Textarea,
    Toast, ToggleSwitch
} from 'primevue';
import Chart from 'primevue/chart';
import Tooltip from "primevue/tooltip";
import PeCoReTAuraPreset from "@/presets/aura";

const app = createApp(App);
registerPlugins(app);

app.use(router);
app.use(PrimeVue, {
    theme: {
        preset: PeCoReTAuraPreset,
        options: {
            darkModeSelector: '.dark'
        }
    }
});

// update theme based on backend setting
await loadPreset();

app.use(ToastService);
app.use(ConfirmationService);
app.use(DialogService);

app.directive('tooltip', Tooltip);

// COMPONENTS
app.component('pBreadcrumb', pBreadcrumb);
app.component('pTabMenu', pTabMenu);
app.component('GenericDataTable', GenericDataTable);
app.component('ModalDialog', ModalDialog);

// LAYOUT COMPONENTS
app.component('BaseLayout', BaseLayout);
app.component('BaseListLayout', BaseListLayout);

// common form components
app.component('Form', Form);
app.component('Field', Field);
app.component('InlineField', InlineField);
app.component('InlineFieldGroup', InlineFieldGroup);

// primevue stuff
app.component('InputText', InputText);
app.component('Button', Button);
app.component('Toast', Toast);
app.component('ConfirmDialog', ConfirmDialog);
app.component('Select', Select);
app.component('InputGroup', InputGroup);
app.component('DatePicker', DatePicker);
app.component('Column', Column);
app.component('Dialog', Dialog);
app.component('Skeleton', Skeleton);
app.component('Card', Card);
app.component('Chart', Chart);
app.component('Checkbox', Checkbox);
app.component('Textarea', Textarea);
app.component('MultiSelect', MultiSelect);
app.component('ButtonGroup', ButtonGroup);
app.component('ToggleSwitch', ToggleSwitch);
app.component('FileUpload', FileUpload);
app.component('SelectButton', SelectButton);
app.component('Password', Password);
app.component('Listbox', Listbox);
app.component('Paginator', Paginator);
app.component('Message', Message);
app.component('IconField', IconField);
app.component('InputIcon', InputIcon);
app.component('PickList', PickList);
app.component('AccordionTab', AccordionTab);
app.component('Accordion', Accordion);
app.component('InputNumber', InputNumber);
app.component('ColorPicker', ColorPicker);

app.mount('#app');
