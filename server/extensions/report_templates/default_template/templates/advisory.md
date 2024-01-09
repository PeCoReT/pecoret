# {{ advisory.vendor_name }} {{ advisory.product }} - {{ advisory.vulnerability.name }}

{% if advisory.vulnerability.cve_id %}
**CVE-ID:** {{ advisoty.vulnerability.cve_id }}
{% else %}
**CVE-ID:** -
{% endif %}

**Vendor:** [{{advisory.vendor_name}}]({{advisory.vendor_url}})

**Affected Product:** {{ advisory.product }}

**Affected Versions:** {{ advisory.affected_versions|safe }}

**Vulnerability:** {{ advisory.vulnerability.name }}

**Status:** {{ advisory.get_status_display() }}

**Severity:** {{ advisory.get_severity_display() }}

**Advisory ID**: {{ advisory.get_advisory_id_display() }}


## Description
{{ advisory.description|safe }}

## Details

{{ advisory.proof_text }}


## Recommendation
{{ advisory.recommendation|safe}}

## Timeline
{% for timeline in advisory.advisorytimeline_set.all() %}
- **{{ timeline.date }}**: {{ timeline.text }}
{% endfor %}