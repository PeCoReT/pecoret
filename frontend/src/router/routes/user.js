const userRoutes = [
    {
        path: '/user/settings',
        name: 'UserProfileSettings',
        component: () => import('@/views/pages/user/UserProfileSettings.vue')
    },
    {
        path: '/user/api-tokens',
        name: 'APITokenList',
        component: () => import('@/views/pages/user/APITokenList.vue')
    },
    {
        path: '/user/api-tokens/create',
        name: 'APITokenCreate',
        component: () => import('@/views/pages/user/APITokenCreate.vue')
    },
    {
        path: '/user/change-email/:uid/:token',
        name: 'UserChangeEmailConfirm',
        component: () => import('@/views/pages/user/UserChangeEmailConfirm.vue')
    },
    {
        path: '/user/webhooks',
        name: 'WebhookList',
        component: () => import('@/views/pages/user/WebhookList.vue')
    },
    {
        path: '/usr/webhooks/:webhookId',
        name: 'WebhookUpdate',
        component: () => import('@/views/pages/user/WebhookUpdate.vue')
    },
    {
        path: '/usr/webhooks/create',
        name: 'WebhookCreate',
        component: () => import('@/views/pages/user/WebhookCreate.vue')
    }
];

export default userRoutes;
