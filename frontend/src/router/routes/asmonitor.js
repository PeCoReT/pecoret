const asmonitorRoutes = [
    {
        path: '/attack-surface',
        children: [
            {
                path: '/attack-surface/programs',
                name: 'AttackSurfaceProgramList',
                component: () => import('@/views/pages/attack_surface/ProgramList.vue')
            },
            {
                path: '/attack-surface/programs/:programId',
                name: 'ASMonitorProgramDetail',
                component: () => import('@/views/pages/asmonitor/ProgramDetail.vue')
            },
            {
                path: '/attack-surface/tags',
                name: 'AttackSurfaceTagList',
                component: () => import('@/views/pages/attack_surface/TagList.vue')
            },
            {
                path: '/attack-surface/targets',
                name: 'AttackSurfaceTargetList',
                component: () => import('@/views/pages/attack_surface/TargetList.vue')
            },
            {
                path: '/attack-surface/scan-findings',
                name: 'AttackSurfaceScanFindingList',
                component: () => import('@/views/pages/attack_surface/ScanFindingList.vue')
            },
            {
                path: '/attack-surface/urls',
                name: 'AttackSurfaceURLList',
                component: () => import('@/views/pages/attack_surface/URLList.vue')
            },
            {
                path: '/attack-surface/urls/:urlId',
                name: 'AttackSurfaceURLDetail',
                component: () => import('@/views/pages/attack_surface/URLDetail.vue')
            },
            {
                path: '/attack-surface/scan-findings/:findingId',
                name: 'AttackSurfaceScanFindingDetail',
                component: () => import('@/views/pages/attack_surface/FindingDetail.vue')
            },
            {
                path: '/attack-surface/ports',
                name: 'AttackSurfacePortList',
                component: () => import('@/views/pages/attack_surface/PortList.vue')
            }
        ]
    }
];

export default asmonitorRoutes;
