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
            },
            {
                path: '/attack-surface/hosts/:hostId',
                name: 'AttackSurfaceHostDetail',
                component: () => import('@/views/pages/attack_surface/HostDetail.vue')
            },
            {
                path: '/attack-surface/services',
                name: 'AttackSurfaceServiceList',
                component: () => import('@/views/pages/attack_surface/ServiceList.vue')
            },
            {
                path: '/attack-surface',
                name: 'AttackSurfaceSearch',
                component: () => import('@/views/pages/attack_surface/Search.vue')
            },
            {
                path: '/attack-surface/hosts',
                name: 'AttackSurfaceHostList',
                component: () => import('@/views/pages/attack_surface/HostList.vue')
            },
            {
                path: '/attack-surface/scanning/scans',
                name: 'AttackSurfaceScanList',
                component: () => import('@/views/pages/attack_surface/ScanList.vue')
            },
            {
                path: '/attack-surface/scanning/scans/:scanId',
                name: 'AttackSurfaceScanDetail',
                component: () => import('@/views/pages/attack_surface/ScanDetail.vue')
            }
        ]
    }
];

export default asmonitorRoutes;
