from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase

from attack_surface.models import Target, Program, ScopeItemCategory, ScopeItem, Service
from attack_surface.models.scoping.item import ScopeResult
from attack_surface.scanning.models import ScanTemplate, ScanBatchRequest, ExclusionRule
from attack_surface.scanning.models.scan_batch import StatusChoices
from attack_surface.scanning.models.scan_template import InputTypeChoices
from attack_surface.scanning.scheduler import scheduler_task
from attack_surface.tests.mixin import AttackSurfaceMixin


class SchedulerTests(AttackSurfaceMixin, APITestCase):
    def setUp(self):
        self.init_mixin()
        self.program = self.create_instance(Program)

        self.template = ScanTemplate.objects.create(
            name="Test Portscan",
            input_type=InputTypeChoices.TARGETS,
            cooldown=timedelta(days=1),
            batch_threshold=5,
            enabled=True,
            trickle_delay=timedelta(minutes=10)
        )

    def test_batch_is_created_and_items_assigned(self):
        scheduler_task()

        batch = ScanBatchRequest.objects.filter(scan_template=self.template).first()
        self.assertIsNotNone(batch)
        self.assertEqual(batch.targets.count(), 3)
        self.assertEqual(batch.status, StatusChoices.STAGING)

    def test_items_within_cooldown_are_excluded(self):
        batch = ScanBatchRequest.objects.create(scan_template=self.template, status=StatusChoices.PENDING)
        batch.targets.add(self.target1)
        batch.targets.add(self.target11)
        batch.targets.add(self.target2)
        batch.batch_end_time = timezone.now()
        batch.save()

        # Run scheduler again — item should be excluded due to cooldown
        scheduler_task()

        # no new batch
        self.assertEqual(ScanBatchRequest.objects.filter(scan_template=self.template).count(), 1)

    def test_excluded_target_is_skipped(self):
        exclusion = ExclusionRule.objects.create(target=self.target1)
        exclusion.scan_templates.add(self.template)

        scheduler_task()
        self.assertFalse(ScanBatchRequest.objects.filter(targets=self.target1).exists())

    def test_excluded_program_is_skipped_children(self):
        exclusion = ExclusionRule.objects.create(program=self.program1)
        exclusion.scan_templates.add(self.template)

        scheduler_task()
        self.assertFalse(ScanBatchRequest.objects.filter(targets=self.target1).exists())

    def test_excluded_target_skipped_with_service(self):
        # test if an excluded target applies to services
        exclusion = ExclusionRule.objects.create(target=self.target1)
        exclusion.scan_templates.add(self.template)
        service = self.create_instance(Service, target=self.target1)
        scheduler_task()
        self.assertFalse(ScanBatchRequest.objects.filter(services=service).exists())

    def test_trickle_promotes_batch(self):
        batch = ScanBatchRequest.objects.create(
            scan_template=self.template,
            status=StatusChoices.STAGING,
            date_last_item_added=timezone.now() - timedelta(minutes=20)
        )
        scheduler_task()
        batch.refresh_from_db()
        self.assertEqual(batch.status, StatusChoices.PENDING)

    def test_scheduler_respects_rate_limit(self):
        # Set the rate limit and batch threshold low to test enforcement
        self.template.rate_limit = 2
        self.template.batch_threshold = 1  # So that each eligible target triggers a new batch
        self.template.save()

        # Add 5 more eligible targets under the same program/scope as existing ones
        for i in range(5):
            t = self.create_instance(Target, program=self.program1, data=f"extra{i}.example10.com")
            ScopeItem.objects.create(
                scope=self.scope1,
                value=t.data,
                category=ScopeItemCategory.DOMAIN,
                results_in=ScopeResult.INCLUDE
            )

        # Run the scheduler — only 2 batches should be created due to the rate limit
        scheduler_task()

        batches = ScanBatchRequest.objects.filter(scan_template=self.template)
        self.assertEqual(batches.count(), 2, "Rate limit should restrict to 2 batches")

        # Each batch should only have one target due to batch threshold = 1
        for batch in batches:
            self.assertEqual(batch.targets.count(), 1, "Each batch should contain exactly one target")

    def test_scheduler_creates_correct_batch_count_based_on_threshold(self):
        # Set a small threshold to force multiple batches
        self.template.batch_threshold = 2
        self.template.cooldown = timedelta(seconds=0)
        self.template.rate_limit = None
        self.template.save()

        # clear items for this one
        Target.objects.all().delete()

        # Add 6 eligible targets in-scope
        for i in range(6):
            target = self.create_instance(Target, program=self.program1, data=f"multi{i}.example10.com")
            ScopeItem.objects.create(
                scope=self.scope1,
                value=target.data,
                category=ScopeItemCategory.DOMAIN,
                results_in=ScopeResult.INCLUDE
            )

        scheduler_task()

        batches = ScanBatchRequest.objects.filter(scan_template=self.template)
        self.assertEqual(batches.count(), 3, "Expected 3 batches for 6 items with threshold 2")

        for batch in batches:
            self.assertEqual(batch.targets.count(), 2, "Each batch should contain exactly 2 targets")

    def test_items_recently_scanned_are_excluded_due_to_cooldown(self):
        self.template.batch_threshold = 10
        self.template.cooldown = timedelta(days=1)
        self.template.save()

        # Create a previous scan batch that includes some targets
        batch = ScanBatchRequest.objects.create(
            scan_template=self.template,
            status=StatusChoices.PENDING,
            batch_end_time=timezone.now() - timedelta(hours=12)
        )
        batch.targets.add(self.target1, self.target2)
        batch.save()

        # Create fresh eligible targets as well
        self.create_instance(Target, program=self.program1, data="fresh1.example10.com")
        self.create_instance(Target, program=self.program1, data="fresh2.example10.com")

        scheduler_task()

        # Only 2 fresh items should be scanned (the other ones are still in cooldown)
        batch = ScanBatchRequest.objects.filter(scan_template=self.template).last()
        self.assertEqual(batch.targets.count(), 2)

    def test_no_eligible_items(self):
        # test that scheduler does not create batches without allowed items
        # Clear all items in scope
        ScopeItem.objects.all().delete()

        # Run the scheduler
        scheduler_task()

        # Assert no batches are created
        self.assertEqual(ScanBatchRequest.objects.filter(scan_template=self.template).count(), 0)

    def test_scheduler_creates_batches_without_rate_limit(self):
        # Set no rate limit
        self.template.rate_limit = None
        self.template.batch_threshold = 2
        self.template.save()

        Target.objects.all().delete()

        # Add 6 eligible targets
        for i in range(6):
            target = self.create_instance(Target, program=self.program1, data=f"no_limit{i}.example10.com")
            ScopeItem.objects.create(
                scope=self.scope1,
                value=target.data,
                category=ScopeItemCategory.DOMAIN,
                results_in=ScopeResult.INCLUDE
            )

        # Run the scheduler
        scheduler_task()

        # Ensure that 3 batches are created (since batch threshold is 2 for 6 items)
        batches = ScanBatchRequest.objects.filter(scan_template=self.template)
        self.assertEqual(batches.count(), 3)
        for batch in batches:
            self.assertEqual(batch.targets.count(), 2)

    def test_items_scanned_exactly_within_cooldown_are_excluded(self):
        self.template.cooldown = timedelta(days=1)
        self.template.save()

        # Create a batch with a target that was scanned exactly 24 hours ago
        batch = ScanBatchRequest.objects.create(
            scan_template=self.template,
            status=StatusChoices.PENDING,
            batch_end_time=timezone.now() - timedelta(days=1)
        )
        batch.targets.add(self.target1)
        batch.save()

        # Add fresh targets
        self.create_instance(Target, program=self.program1, data="fresh1.example10.com")

        # Run scheduler and check batch count
        scheduler_task()
        batch = ScanBatchRequest.objects.filter(scan_template=self.template).last()
        self.assertEqual(batch.targets.count(),
                         1)  # Should only include fresh targets, not the ones within the cooldown

    def test_batch_status_changes_after_trickle_timeout(self):
        # Test that batches are correctly marked as PENDING after the trickle timeout if they aren't filled within the threshold.
        # Set trickle delay to 1 minute
        self.template.trickle_delay = timedelta(minutes=1)
        self.template.save()

        # Create a batch with some targets
        batch = ScanBatchRequest.objects.create(
            scan_template=self.template,
            status=StatusChoices.STAGING,
            date_last_item_added=timezone.now() - timedelta(minutes=2)  # Make it timeout
        )
        batch.targets.add(self.target1)

        # Run the scheduler
        scheduler_task()

        # Verify that the batch status changed to PENDING
        batch.refresh_from_db()
        self.assertEqual(batch.status, StatusChoices.PENDING)

    def test_scheduler_creates_batches_for_multiple_templates(self):
        # Create a second template with different configurations
        template2 = ScanTemplate.objects.create(
            name="Test Webscan",
            input_type=InputTypeChoices.TARGETS,
            cooldown=timedelta(days=1),
            batch_threshold=3,
            enabled=True,
            trickle_delay=timedelta(minutes=5)
        )
        Target.objects.all().delete()
        # Add targets for both templates
        for i in range(6):
            target = self.create_instance(Target, program=self.program1, data=f"multi{i}.example10.com")
            ScopeItem.objects.create(
                scope=self.scope1,
                value=target.data,
                category=ScopeItemCategory.DOMAIN,
                results_in=ScopeResult.INCLUDE
            )

        # Run the scheduler for both templates
        scheduler_task()

        # Ensure both templates create the expected number of batches based on their configurations
        batches_template1 = ScanBatchRequest.objects.filter(scan_template=self.template)
        batches_template2 = ScanBatchRequest.objects.filter(scan_template=template2)

        self.assertEqual(batches_template1.count(), 2)  # Based on template1's batch threshold
        self.assertEqual(batches_template2.count(), 2)  # Based on template2's batch threshold

    def test_djangoql_filter_is_applied(self):
        # Apply a djangoql filter that includes only `match.example.com`
        self.template.conditions = 'data="example10.com"'
        self.template.save()

        scheduler_task()

        batch = ScanBatchRequest.objects.filter(scan_template=self.template).first()
        self.assertIsNotNone(batch)
        self.assertIn(self.target1, batch.targets.all())
        self.assertNotIn(self.target11, batch.targets.all())
