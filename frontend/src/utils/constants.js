export const severityChoices = [
    { label: 'Critical', value: 'Critical' },
    { label: 'High', value: 'High' },
    { label: 'Medium', value: 'Medium' },
    { label: 'Low', value: 'Low' },
    { label: 'Informational', value: 'Informational' }
];

export const findingStatusChoices = [
    { title: 'Open', value: 'Open' },
    { title: 'Fixed', value: 'Fixed' },
    { title: "Won't Fix", value: 'Wont Fix' }
];

export const serviceProtocolChoices = [
    {
        label: 'TCP',
        value: 'TCP'
    },
    {
        label: 'UDP',
        value: 'UDP'
    }
];

export const vulnerabilityStatusChoices = [
    {
        label: 'Unfixed',
        value: 'Unfixed'
    },
    {
        label: 'Fixed',
        value: 'Fixed'
    },
    {
        label: "Won't fix",
        value: "Won't fix"
    }
];

export const advisoryStatusChoices = [
    {
        label: 'Disclosed',
        value: 'Disclosed'
    },
    {
        label: 'Not Disclosed',
        value: 'Not Disclosed'
    }
];

export const projectVisibilityChoices = [
    {
        label: 'Membery Only',
        value: 'Members Only'
    },
    {
        label: 'Pentesters',
        value: 'Pentesters'
    }
];

export const allowedObjectTypeChoices = [
    {
        label: 'Service',
        value: 'service'
    },
    {
        label: 'URL',
        value: 'url'
    },
    {
        label: 'Target',
        value: 'target'
    }
];

export const InScopeChoices = [
    {
        name: 'In Scope',
        value: 'In Scope'
    },
    {
        name: 'Undefined',
        value: 'Undefined'
    },
    {
        name: 'Out of Scope',
        value: 'Out of Scope'
    }
];

export const DataTypeChoices = [
    {
        name: 'IP',
        value: 'IP'
    },
    {
        name: 'Domain',
        value: 'Domain'
    },
    {
        name: 'Subdomain',
        value: 'Subdomain'
    }
];

export const asFindingProgressStatus = [
    {
        name: 'Draft',
        value: 'Draft'
    },
    {
        name: 'Review Required',
        value: 'Review Required'
    },
    {
        name: 'Final',
        value: 'Final'
    }
];

export const findingComponentStatus = [
    {
        name: 'Vulnerable',
        value: 'Vulnerable'
    },
    {
        name: 'Fixed',
        value: 'Fixed'
    },
    {
        name: 'Wont fix',
        value: 'Wont fix'
    }
];

export const asFindingStatusChoices = [
    {
        name: 'Open',
        value: 'Open'
    },
    {
        name: 'Closed',
        value: 'Closed'
    }
];
