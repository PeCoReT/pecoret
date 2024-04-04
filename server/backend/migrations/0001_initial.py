import advisories.models.advisory
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "ordering": ["username"],
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("role", models.CharField(blank=True, max_length=256)),
                ("username", models.CharField(max_length=256)),
                ("password", models.CharField(blank=True, max_length=256)),
                ("accessible", models.BooleanField(blank=True, null=True)),
                ("compromised", models.BooleanField(blank=True, default=False)),
            ],
            options={
                "ordering": ("-pk",),
            },
        ),
        migrations.CreateModel(
            name="Advisory",
            fields=[
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                (
                    "advisory_id",
                    models.CharField(
                        default=advisories.models.advisory.create_advisory_id,
                        max_length=28,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("date_planned_disclosure", models.DateField()),
                ("date_disclosure", models.DateField(blank=True, null=True)),
                ("product", models.CharField(max_length=128)),
                ("internal_name", models.CharField(default="", max_length=64)),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "Open"), (2, "Fixed"), (3, "Wont Fix")], default=1
                    ),
                ),
                ("affected_versions", models.CharField(max_length=128)),
                (
                    "fixed_version",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
                (
                    "severity",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "Informational"),
                            (1, "Low"),
                            (2, "Medium"),
                            (3, "High"),
                            (4, "Critical"),
                        ]
                    ),
                ),
                ("cve_id", models.CharField(blank=True, max_length=20, null=True)),
                ("is_draft", models.BooleanField(default=True)),
                ("vendor_url", models.URLField()),
                ("vendor_name", models.CharField(max_length=128)),
                ("description", models.TextField(blank=True, null=True)),
                ("recommendation", models.TextField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-advisory_id", "date_updated"],
            },
        ),
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=256)),
                ("street", models.CharField(max_length=256)),
                ("zipcode", models.CharField(max_length=256)),
                ("city", models.CharField(max_length=256)),
                ("country", models.CharField(max_length=256)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="CompanyContact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("first_name", models.CharField(max_length=128)),
                ("last_name", models.CharField(max_length=128)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("phone", models.CharField(max_length=28)),
                ("role", models.CharField(max_length=128)),
                ("pgp_public_key", models.TextField(blank=True, null=True)),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.company",
                    ),
                ),
            ],
            options={
                "ordering": ["first_name", "last_name"],
            },
        ),
        migrations.CreateModel(
            name="CWE",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cwe_id", models.IntegerField(unique=True)),
                ("name", models.CharField(max_length=512)),
                ("description", models.TextField()),
                ("extended_description", models.TextField(blank=True)),
                (
                    "entry_type",
                    models.SmallIntegerField(
                        choices=[(0, "Weakness"), (1, "Category")]
                    ),
                ),
            ],
            options={
                "verbose_name": "CWE",
                "verbose_name_plural": "CWEs",
                "ordering": ["cwe_id"],
            },
        ),
        migrations.CreateModel(
            name="Finding",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                (
                    "severity",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "Informational"),
                            (1, "Low"),
                            (2, "Medium"),
                            (3, "High"),
                            (4, "Critical"),
                        ]
                    ),
                ),
                ("recommendation", models.TextField(blank=True, null=True)),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "Open"), (1, "Fixed"), (2, "Wont Fix")], default=0
                    ),
                ),
                ("imported", models.BooleanField(default=False)),
                ("finding_date", models.DateField(blank=True, default=None, null=True)),
                ("name", models.CharField(max_length=256)),
                ("authenticated_test", models.BooleanField(default=False)),
                ("needs_review", models.BooleanField(default=False)),
                ("exclude_from_report", models.BooleanField(default=False)),
                ("date_retest", models.DateField(blank=True, null=True)),
                ("retest_results", models.TextField(blank=True, null=True)),
                ("cwe_ids", models.ManyToManyField(blank=True, to="backend.cwe")),
            ],
            options={
                "ordering": ["-severity"],
            },
        ),
        migrations.CreateModel(
            name="Host",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                (
                    "accessible",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "Accessible"),
                            (1, "Not Accessible"),
                            (2, "Unknown"),
                        ],
                        default=2,
                    ),
                ),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "environment",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "Unknown"),
                            (1, "Production"),
                            (2, "Testing"),
                            (3, "Development"),
                            (4, "Staging"),
                        ],
                        default=0,
                    ),
                ),
                ("ip", models.GenericIPAddressField()),
                ("dns", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "operating_system",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
            options={
                "ordering": ["-pk"],
            },
        ),
        migrations.CreateModel(
            name="PentestType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=64, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
            ],
            options={
                "ordering": ["-date_created"],
            },
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("name", models.CharField(max_length=254, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "Open"), (1, "Closed")], default=0
                    ),
                ),
                (
                    "test_method",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "White Box"),
                            (1, "Grey Box"),
                            (2, "Black Box"),
                            (3, "Unknown"),
                        ]
                    ),
                ),
                (
                    "year",
                    models.PositiveIntegerField(blank=True, editable=False, null=True),
                ),
                ("require_cvss_base_score", models.BooleanField(default=False)),
                (
                    "language",
                    models.CharField(
                        choices=[("en", "English"), ("de", "German")],
                        default="en",
                        max_length=4,
                    ),
                ),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="backend.company",
                    ),
                ),
                ("pentest_types", models.ManyToManyField(to="backend.pentesttype")),
            ],
            options={
                "ordering": ["-date_created", "-date_updated"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Report",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=128)),
                ("title", models.CharField(default="Pentest Report", max_length=128)),
                (
                    "variant",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "Pentest PDF"), (1, "Vulnerability CSV")]
                    ),
                ),
                ("recommendation", models.TextField(blank=True, null=True)),
                ("evaluation", models.TextField(blank=True, null=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.project",
                    ),
                ),
            ],
            options={
                "ordering": ["-date_created"],
            },
        ),
        migrations.CreateModel(
            name="ReportTemplate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "Active"), (1, "Draft"), (2, "Deactivated")],
                        default=0,
                    ),
                ),
                ("name", models.CharField(max_length=64, unique=True)),
                ("path", models.CharField(max_length=128)),
            ],
            options={
                "ordering": ["-date_created", "name"],
            },
        ),
        migrations.CreateModel(
            name="VulnerabilityCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("category_id", models.CharField(max_length=128, unique=True)),
                ("name", models.CharField(max_length=255)),
                ("name_en", models.CharField(max_length=255, null=True)),
                ("name_de", models.CharField(max_length=255, null=True)),
            ],
            options={
                "verbose_name": "Vulnerability Category",
                "verbose_name_plural": "Vulnerability Categories",
                "ordering": ["category_id"],
            },
        ),
        migrations.CreateModel(
            name="WebApplication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                (
                    "accessible",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "Accessible"),
                            (1, "Not Accessible"),
                            (2, "Unknown"),
                        ],
                        default=2,
                    ),
                ),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "environment",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "Unknown"),
                            (1, "Production"),
                            (2, "Testing"),
                            (3, "Development"),
                            (4, "Staging"),
                        ],
                        default=0,
                    ),
                ),
                ("name", models.CharField(max_length=256)),
                ("base_url", models.URLField()),
                ("version", models.CharField(blank=True, max_length=128, null=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.project",
                    ),
                ),
            ],
            options={
                "verbose_name": "Web Application",
                "verbose_name_plural": "Web Applications",
                "ordering": ["-pk"],
                "unique_together": {("project", "name")},
            },
        ),
        migrations.CreateModel(
            name="VulnerabilityTemplate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "severity",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "Informational"),
                            (1, "Low"),
                            (2, "Medium"),
                            (3, "High"),
                            (4, "Critical"),
                        ]
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=128)),
                ("name_en", models.CharField(max_length=128, null=True)),
                ("name_de", models.CharField(max_length=128, null=True)),
                ("description", models.TextField()),
                ("description_en", models.TextField(null=True)),
                ("description_de", models.TextField(null=True)),
                ("recommendation", models.TextField()),
                ("recommendation_en", models.TextField(null=True)),
                ("recommendation_de", models.TextField(null=True)),
                ("vulnerability_id", models.CharField(max_length=254, unique=True)),
                (
                    "categories",
                    models.ManyToManyField(to="backend.vulnerabilitycategory"),
                ),
                (
                    "cwe",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="backend.cwe",
                    ),
                ),
            ],
            options={
                "verbose_name": "Vulnerability Template",
                "verbose_name_plural": "Vulnerability Templates",
                "ordering": ["-vulnerability_id"],
            },
        ),
        migrations.CreateModel(
            name="UserSettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("show_real_name_in_report", models.BooleanField(default=False)),
                ("notify_before_disclosure_mail", models.BooleanField(default=False)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(blank=True, max_length=256)),
                (
                    "protocol",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "TCP"), (1, "UDP")], default=0
                    ),
                ),
                (
                    "port",
                    models.PositiveSmallIntegerField(
                        null=True,
                        validators=[django.core.validators.MaxValueValidator(65535)],
                    ),
                ),
                ("product", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "state",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "Open"), (1, "Closed"), (2, "Filtered")],
                        default=0,
                        null=True,
                    ),
                ),
                (
                    "host",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="services",
                        to="backend.host",
                    ),
                ),
            ],
            options={
                "ordering": ["host__dns", "host__ip", "port"],
                "unique_together": {("host", "port", "protocol")},
            },
        ),
        migrations.CreateModel(
            name="ReportRelease",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=128)),
                ("raw_source", models.TextField(blank=True, null=True)),
                ("compiled_source", models.BinaryField(blank=True, null=True)),
                (
                    "release_type",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "Draft"), (1, "Final")]
                    ),
                ),
                ("task_id", models.CharField(blank=True, max_length=64, null=True)),
                (
                    "content_type",
                    models.CharField(
                        default="application/octet-stream", max_length=128
                    ),
                ),
                ("file_extension", models.CharField(default="pdf", max_length=12)),
                (
                    "report",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="backend.report"
                    ),
                ),
            ],
            options={
                "ordering": ["-date_created", "-date_updated"],
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="report",
            name="template",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="backend.reporttemplate"
            ),
        ),
        migrations.CreateModel(
            name="ProjectVulnerability",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("vulnerability_id", models.CharField(max_length=254)),
                (
                    "severity",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "Informational"),
                            (1, "Low"),
                            (2, "Medium"),
                            (3, "High"),
                            (4, "Critical"),
                        ]
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=128)),
                ("name_en", models.CharField(max_length=128, null=True)),
                ("name_de", models.CharField(max_length=128, null=True)),
                ("description", models.TextField()),
                ("description_en", models.TextField(null=True)),
                ("description_de", models.TextField(null=True)),
                ("recommendation", models.TextField()),
                ("recommendation_en", models.TextField(null=True)),
                ("recommendation_de", models.TextField(null=True)),
                (
                    "categories",
                    models.ManyToManyField(to="backend.vulnerabilitycategory"),
                ),
                (
                    "cwe",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="backend.cwe",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.project",
                    ),
                ),
                (
                    "template",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="backend.vulnerabilitytemplate",
                    ),
                ),
            ],
            options={
                "verbose_name": "Project Vulnerability",
                "verbose_name_plural": "Project Vulnerabilities",
                "ordering": ["-severity"],
                "unique_together": {
                    ("project", "name"),
                    ("project", "vulnerability_id"),
                },
            },
        ),
        migrations.CreateModel(
            name="ProjectToken",
            fields=[
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("date_expire", models.DateTimeField()),
                (
                    "key",
                    models.CharField(
                        editable=False,
                        max_length=512,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=32)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.project",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Project Token",
                "verbose_name_plural": "Project Tokens",
                "ordering": ["-date_expire"],
            },
        ),
        migrations.CreateModel(
            name="OWASPRiskRating",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "skill_level",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "N/A"),
                            (1, "Security penetration skills"),
                            (3, "Networking and programming skills"),
                            (5, "Advanced computer skills"),
                            (6, "Some technical skills"),
                            (9, "No technical skills"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "motive",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "N/A"),
                            (1, "Low or no reward"),
                            (4, "Possible reward"),
                            (9, "High reward"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "opportunity",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "FUll access or expensive resources required"),
                            (4, "Special access or resources required"),
                            (7, "Some access or resources required"),
                            (9, "No access or resources required"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "size",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "N/A"),
                            (2, "Developers or system administrators"),
                            (4, "Intranet users"),
                            (5, "Partners"),
                            (6, "Authenticated users"),
                            (9, "Anonymous internet users"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "ease_of_discovery",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "N/A"),
                            (1, "Practically impossible"),
                            (3, "Difficult"),
                            (7, "Easy"),
                            (9, "Automated tools available"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "ease_of_exploit",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "N/A"),
                            (1, "Theoretical"),
                            (3, "Difficult"),
                            (7, "Easy"),
                            (9, "Automated tools available"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "awareness",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "N/A"),
                            (1, "Unknown"),
                            (4, "Hidden"),
                            (6, "Obvious"),
                            (9, "Public Knowledge"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "intrusion_detection",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "N/A"),
                            (1, "Active detection in application"),
                            (3, "Logged and reviewed"),
                            (8, "Logged without review"),
                            (9, "Not logged"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "loss_of_confidentiality",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "N/A"),
                            (2, "Minimal non-sensitive data disclosed"),
                            (
                                6,
                                "Minimal critical data or extensive non-sensitive data disclosed",
                            ),
                            (7, "Extensive critical data disclosed"),
                            (9, "All data disclosed"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "loss_of_availability",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "N/A"),
                            (1, "Minimal secondary services interrupted"),
                            (
                                5,
                                "Minimal primary or extensive secondary services interrupted",
                            ),
                            (7, "Extensive primary services interrupted"),
                            (9, "All services completely lost"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "loss_of_integrity",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "N/A"),
                            (1, "Minimal slightly corrupted data"),
                            (3, "Minimal seriously corrupted data"),
                            (5, "Extensive slightly corrupted data"),
                            (7, "Extensive seriously corrupted data"),
                            (9, "All data totally corrupted"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "loss_of_accountability",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "N/A"),
                            (1, "Fully traceable"),
                            (7, "Possibly traceable"),
                            (9, "Completely anonymous"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "financial_damage",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "N/A"),
                            (1, "Less than the cost to fix the vulnerability"),
                            (3, "Minor effect on annual profit"),
                            (7, "Significant effect on annual profit"),
                            (9, "Bankruptcy"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "reputation_damage",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "N/A"),
                            (1, "Minimal damage"),
                            (4, "Loss of major accounts"),
                            (5, "Loss of goodwill"),
                            (9, "Brand damage"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "non_compliance",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "N/A"),
                            (2, "Minor violation"),
                            (5, "Clear violation"),
                            (7, "High profile violation"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "privacy_violation",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "N/A"),
                            (3, "One individual"),
                            (5, "Hundreds of people"),
                            (7, "Thousands of people"),
                            (9, "Millions of people"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "finding",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.finding",
                    ),
                ),
            ],
            options={
                "ordering": ["finding"],
            },
        ),
        migrations.CreateModel(
            name="MobileApplication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                (
                    "accessible",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "Accessible"),
                            (1, "Not Accessible"),
                            (2, "Unknown"),
                        ],
                        default=2,
                    ),
                ),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "environment",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "Unknown"),
                            (1, "Production"),
                            (2, "Testing"),
                            (3, "Development"),
                            (4, "Staging"),
                        ],
                        default=0,
                    ),
                ),
                ("name", models.CharField(max_length=256)),
                ("version", models.CharField(blank=True, max_length=128)),
                (
                    "os",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "Unknown"), (1, "Android"), (2, "iOS")], default=0
                    ),
                ),
                ("certificate_pinning", models.BooleanField(blank=True, null=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.project",
                    ),
                ),
            ],
            options={
                "ordering": ["name", "version"],
                "unique_together": {("project", "name")},
            },
        ),
        migrations.AddField(
            model_name="host",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="backend.project"
            ),
        ),
        migrations.CreateModel(
            name="FindingTimeline",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("is_system_log", models.BooleanField(default=False)),
                ("title", models.CharField(max_length=128)),
                ("text", models.TextField()),
                (
                    "finding",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.finding",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-date_created"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="FindingComment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("comment", models.TextField()),
                (
                    "finding",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.finding",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["date_created"],
            },
        ),
        migrations.AddField(
            model_name="finding",
            name="host",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="backend.host",
            ),
        ),
        migrations.AddField(
            model_name="finding",
            name="mobile_application",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="backend.mobileapplication",
            ),
        ),
        migrations.AddField(
            model_name="finding",
            name="project",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                to="backend.project",
            ),
        ),
        migrations.AddField(
            model_name="finding",
            name="service",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="backend.service",
            ),
        ),
        migrations.AddField(
            model_name="finding",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="finding",
            name="user_account",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="backend.account",
            ),
        ),
        migrations.AddField(
            model_name="finding",
            name="vulnerability",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="backend.projectvulnerability",
            ),
        ),
        migrations.AddField(
            model_name="finding",
            name="web_application",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="backend.webapplication",
            ),
        ),
        migrations.CreateModel(
            name="CVSSBaseScore",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "av",
                    models.PositiveIntegerField(
                        choices=[(0, "N"), (1, "A"), (2, "L"), (3, "P")], null=True
                    ),
                ),
                (
                    "ac",
                    models.PositiveIntegerField(
                        choices=[(0, "L"), (1, "H")], null=True
                    ),
                ),
                (
                    "pr",
                    models.PositiveIntegerField(
                        choices=[(0, "N"), (1, "L"), (2, "H")], null=True
                    ),
                ),
                (
                    "ui",
                    models.PositiveIntegerField(
                        choices=[(0, "N"), (1, "R")], null=True
                    ),
                ),
                (
                    "s",
                    models.PositiveIntegerField(
                        choices=[(0, "U"), (1, "C")], null=True
                    ),
                ),
                (
                    "a",
                    models.PositiveIntegerField(
                        choices=[(0, "N"), (1, "L"), (2, "H")], null=True
                    ),
                ),
                (
                    "i",
                    models.PositiveIntegerField(
                        choices=[(0, "N"), (1, "L"), (2, "H")], null=True
                    ),
                ),
                (
                    "c",
                    models.PositiveIntegerField(
                        choices=[(0, "N"), (1, "L"), (2, "H")], null=True
                    ),
                ),
                (
                    "finding",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.finding",
                    ),
                ),
            ],
            options={
                "ordering": ["finding"],
            },
        ),
        migrations.CreateModel(
            name="CompanyInformation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("text", models.TextField()),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="backend.company",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-date_created", "-date_updated"],
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="company",
            name="report_template",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="backend.reporttemplate"
            ),
        ),
        migrations.CreateModel(
            name="ChangeHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("version", models.FloatField()),
                ("date", models.DateField()),
                ("change", models.CharField(max_length=128)),
                (
                    "report",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="backend.report"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["version"],
            },
        ),
        migrations.CreateModel(
            name="AuthToken",
            fields=[
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("date_expire", models.DateTimeField()),
                (
                    "key",
                    models.CharField(
                        editable=False,
                        max_length=512,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Auth Token",
                "verbose_name_plural": "Auth Tokens",
                "ordering": ["-date_expire"],
            },
        ),
        migrations.CreateModel(
            name="AdvisoryTimeline",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("text", models.CharField(max_length=255)),
                (
                    "advisory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.advisory",
                    ),
                ),
            ],
            options={
                "ordering": ["-date"],
            },
        ),
        migrations.CreateModel(
            name="AdvisoryProof",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=256)),
                ("order", models.PositiveSmallIntegerField(null=True)),
                ("text", models.TextField(blank=True, null=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        max_length=256,
                        null=True,
                        upload_to="",
                    ),
                ),
                (
                    "image_caption",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                (
                    "advisory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.advisory",
                    ),
                ),
            ],
            options={
                "ordering": ["advisory", "order"],
            },
        ),
        migrations.CreateModel(
            name="AdvisoryMembership",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                (
                    "active_until",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                (
                    "role",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "Creator"), (1, "Read Only"), (2, "Vendor")],
                        default=1,
                    ),
                ),
                (
                    "advisory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.advisory",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-date_created"],
            },
        ),
        migrations.CreateModel(
            name="AdvisoryComment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("comment", models.TextField()),
                (
                    "advisory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.advisory",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["date_created"],
            },
        ),
        migrations.AddField(
            model_name="advisory",
            name="vulnerability",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="backend.vulnerabilitytemplate",
            ),
        ),
        migrations.AddField(
            model_name="account",
            name="host",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="backend.host",
            ),
        ),
        migrations.AddField(
            model_name="account",
            name="project",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                to="backend.project",
            ),
        ),
        migrations.AddField(
            model_name="account",
            name="web_application",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="backend.webapplication",
            ),
        ),
        migrations.CreateModel(
            name="Proof",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=256)),
                ("order", models.PositiveSmallIntegerField(null=True)),
                ("text", models.TextField(blank=True, null=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        max_length=256,
                        null=True,
                        upload_to="/dev/null",
                    ),
                ),
                (
                    "image_caption",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                (
                    "finding",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.finding",
                    ),
                ),
            ],
            options={
                "ordering": ["finding", "order"],
                "unique_together": {("finding", "title")},
            },
        ),
        migrations.CreateModel(
            name="ProjectContact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                (
                    "contact",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="backend.companycontact",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.project",
                    ),
                ),
            ],
            options={
                "ordering": ["-date_created", "-date_updated"],
                "unique_together": {("contact", "project")},
            },
        ),
        migrations.CreateModel(
            name="PinnedProject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.project",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-project__name"],
                "unique_together": {("project", "user")},
            },
        ),
        migrations.CreateModel(
            name="Membership",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                (
                    "role",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "Project Leader"),
                            (1, "Contributor"),
                            (2, "Read Only"),
                            (3, "Customer"),
                            (4, "Owner"),
                        ],
                        default=1,
                    ),
                ),
                (
                    "active_until",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                ("display_in_report", models.BooleanField(default=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.project",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-date_created"],
                "unique_together": {("user", "project")},
            },
        ),
        migrations.AddConstraint(
            model_name="host",
            constraint=models.UniqueConstraint(
                fields=("project", "ip"), name="host_ip_unique"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="companycontact",
            unique_together={("first_name", "last_name", "company")},
        ),
        migrations.AlterUniqueTogether(
            name="changehistory",
            unique_together={("report", "version")},
        ),
        migrations.AlterUniqueTogether(
            name="advisorymembership",
            unique_together={("user", "advisory")},
        ),
    ]
