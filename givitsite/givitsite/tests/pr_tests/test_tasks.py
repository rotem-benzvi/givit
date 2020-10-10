from background_task.models import Task
from background_task.models import CompletedTask
from background_task import background
from background_task.tasks import tasks
from django.test.testcases import TransactionTestCase
import time
from datetime import timedelta
from django.utils import timezone
from gatherer.tasks import gatherer_task


class TestBackgroundDecorator(TransactionTestCase):
    def test_launch_sync(self):
        # ''' Check launch original function in synchronous mode '''

        @background
        def add(x, y):
            return x + y

        t = Task.objects.count()
        ct = CompletedTask.objects.count()
        answer = add.now(2, 3)
        self.assertEqual(answer, 5)
        self.assertEqual(Task.objects.count(), t, 'Task was created')
        self.assertEqual(CompletedTask.objects.count(),
                         ct, 'Completed task was created')


class RepetitionTestCase(TransactionTestCase):

    def setUp(self):
        @tasks.background()
        def my_task(*args, **kwargs):
            pass
        self.my_task = my_task

    def test_repeat(self):
        repeat_until = timezone.now() + timedelta(weeks=1)
        old_task = self.my_task(
            'test-repeat',
            foo='bar',
            repeat=Task.HOURLY,
            repeat_until=repeat_until,
            verbose_name="Test repeat",
        )
        self.assertEqual(old_task.repeat, Task.HOURLY)
        self.assertEqual(old_task.repeat_until, repeat_until)
        tasks.run_next_task()
        time.sleep(0.5)

        self.assertEqual(Task.objects.filter(
            repeat=Task.HOURLY, verbose_name="Test repeat").count(), 1)
        new_task = Task.objects.get(
            repeat=Task.HOURLY, verbose_name="Test repeat")
        self.assertNotEqual(new_task.id, old_task.id)
        self.assertEqual(new_task.task_name, old_task.task_name)
        self.assertEqual(new_task.params(), old_task.params())
        self.assertEqual(new_task.task_hash, old_task.task_hash)
        self.assertEqual(new_task.verbose_name, old_task.verbose_name)
        self.assertEqual((new_task.run_at - old_task.run_at),
                         timedelta(hours=1))
        self.assertEqual(new_task.repeat_until, old_task.repeat_until)

        all_tasks = Task.objects.get(
            repeat=Task.HOURLY, verbose_name="Test repeat")
        all_tasks.delete()

    def test_repetition_in_future(self):
        repeat_until = timezone.now() + timedelta(weeks=1)
        old_task = self.my_task(
            'test-repetition',
            repeat=Task.HOURLY,
            repeat_until=repeat_until,
            verbose_name="Test repetition in future",
        )
        old_task.run_at = timezone.now() - timedelta(weeks=1)  # task is one week old
        old_task.save()
        tasks.run_next_task()
        time.sleep(0.5)

        self.assertEqual(Task.objects.filter(
            repeat=Task.HOURLY, verbose_name="Test repetition in future").count(), 1)
        new_task = Task.objects.get(
            repeat=Task.HOURLY, verbose_name="Test repetition in future")
        self.assertNotEqual(new_task.id, old_task.id)
        # new task skipped exactly one week of downtime in the past, keeps period
        self.assertEqual((new_task.run_at - old_task.run_at),
                         timedelta(weeks=1, hours=1))
        # new task will be executed in the future
        self.assertTrue(new_task.run_at > timezone.now())
        # new task will be executed in less than one hour
        self.assertTrue((new_task.run_at - timezone.now())
                        <= timedelta(hours=1))

        all_tasks = Task.objects.get(
            repeat=Task.HOURLY, verbose_name="Test repetition in future")
        all_tasks.delete()

    def test_gatherer_task(self):
        repeat_until = timezone.now() + timedelta(weeks=1)
        old_task = gatherer_task(
            repeat=Task.HOURLY,
            repeat_until=repeat_until,
            verbose_name="gatherer_test",
        )
        old_task.run_at = timezone.now() - timedelta(weeks=1)  # task is one week old
        old_task.save()
        tasks.run_next_task()
        time.sleep(0.5)

        self.assertEqual(Task.objects.filter(
            repeat=Task.HOURLY, verbose_name="gatherer_test").count(), 1)
        new_task = Task.objects.get(
            repeat=Task.HOURLY, verbose_name="gatherer_test")
        self.assertNotEqual(new_task.id, old_task.id)
        # new task skipped exactly one week of downtime in the past, keeps period
        self.assertEqual((new_task.run_at - old_task.run_at),
                         timedelta(weeks=1, hours=1))
        # new task will be executed in the future
        self.assertTrue(new_task.run_at > timezone.now())
        # new task will be executed in less than one hour
        self.assertTrue((new_task.run_at - timezone.now())
                        <= timedelta(hours=1))

        all_tasks = Task.objects.get(
            repeat=Task.HOURLY, verbose_name="gatherer_test")
        all_tasks.delete()
