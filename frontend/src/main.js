import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { registerPlugins } from '@/plugins';

import '@fortawesome/fontawesome-free/css/all.min.css';

import { Card } from '@/components/card';

import { Field, Form, InlineField, InlineFieldGroup } from '@/components/form';


const app = createApp(App);
registerPlugins(app);

app.use(router);


// COMPONENTS
// common form components
app.component('Form', Form);
app.component('Field', Field);
app.component('InlineField', InlineField);
app.component('InlineFieldGroup', InlineFieldGroup);
app.component('Card', Card);

app.mount('#app');
