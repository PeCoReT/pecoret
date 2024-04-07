const asmonitorRoutes = [
    {
        path: '/attack-surface',
        children: [
            {
                path: '/attack-surface/programs',
                name: 'ASMonitorProgramList',
                component: () => import('@/views/pages/asmonitor/ProgramList.vue')
            },
            {
                path: '/attack-surface/programs/:programId',
                name: 'ASMonitorProgramDetail',
                component: () => import('@/views/pages/asmonitor/ProgramDetail.vue')
            },
            {
                path: '/attack-surface/tags',
                name: 'ASMonitorTagList',
                component: () => import('@/views/pages/asmonitor/TagList.vue')
            },
            {
                path: '/attack-surface/programs/:programId/targets',
                name: 'ASMonitorTargetList',
                component: () => import('@/views/pages/asmonitor/TargetList.vue')
            },
            {
                path: '/attack-surface/programs/:programId/findings',
                name: 'ASMonitorFindingList',
                component: () => import('@/views/pages/asmonitor/FindingList.vue')
            },
            {
                path: '/attack-surface/programs/:programId/findings/:findingId',
                name: 'ASMonitorFindingDetail',
                component: () => import('@/views/pages/asmonitor/FindingDetail.vue')
            },
            {
                path: '/attack-surface/findings',
                name: 'ASMonitorGlobalFindingList',
                component: () => import('@/views/pages/asmonitor/GlobalFindingList.vue')
            },
            {
                path: '/attack-surface/targets',
                name: 'ASMonitorGlobalTargetList',
                component: () => import('@/views/pages/asmonitor/GlobalTargetList.vue')
            }
        ]
    }
];

export default asmonitorRoutes;
