import os
import pathlib
import shutil
import tempfile
import typing

import aiogram
import apscheduler.schedulers.base
from apscheduler import schedulers
from apscheduler.triggers import cron

import config
import loader


def setup_tasks():
    loader.scheduler.start()
    backup_settings = config.BackupSettings()
    add_task(loader.scheduler, make_database_backup, backup_settings.backup_period, 'make_database_backup')
    add_task(
        loader.scheduler, send_database_backup_to_admin, backup_settings.sending_backup_period,
        'send_database_backup_to_admin', backup_settings.admin_id
    )


def check_period(period: str) -> bool:
    try:
        cron.CronTrigger().from_crontab(period)
    except ValueError:
        return False
    return True


def add_task(scheduler: schedulers.base.BaseScheduler, task: typing.Callable,
             period: str, job_id: str, *task_args, **task_kwargs):
    scheduler.add_job(task, cron.CronTrigger().from_crontab(period), task_args, task_kwargs, id=job_id)


def reschedule_task(scheduler: schedulers.base.BaseScheduler, job_id: str, period: str):
    scheduler.reschedule_job(job_id, trigger=cron.CronTrigger().from_crontab(period))


async def send_project_backup_to_admin(admin_id: int):
    backup_dir = config.BACKUP_PATH / 'project'
    file = shutil.make_archive(str(pathlib.Path(tempfile.mkdtemp()) / 'project'), 'zip', backup_dir)
    await loader.bot.send_document(admin_id, aiogram.types.InputFile(file))


async def send_database_backup_to_admin(admin_id: int):
    backups = os.listdir(config.BACKUP_PATH / 'database')
    last_backup_id = int(backups[-1].replace('backup_', ''))
    backup_dir = config.BACKUP_PATH / 'database' / f'backup_{last_backup_id}'
    file = shutil.make_archive(str(pathlib.Path(tempfile.mkdtemp()) / 'database'), 'zip', backup_dir)
    await loader.bot.send_document(admin_id, aiogram.types.InputFile(file))


def make_project_backup():
    os.system(pathlib.Path(os.path.abspath('..')) / 'scripts' / 'backup_project.sh')


def make_database_backup():
    backup_dir = config.BACKUP_PATH / 'database'
    if not backup_dir.exists():
        backup_dir.mkdir()
    backups = os.listdir(backup_dir)
    for backup in backups[:-2]:
        shutil.rmtree(backup_dir / backup)
    last_backup_id = int(backups[-1].replace('backup_', '')) if len(backups) > 0 else 0
    backup_dir = backup_dir / f'backup_{str(last_backup_id + 1)}'
    temp_dir = pathlib.Path(tempfile.mkdtemp())
    shutil.copytree(config.DATA_PATH / 'products', temp_dir / 'products')
    shutil.copy(config.DATA_PATH / 'database.db', temp_dir)
    shutil.move(temp_dir, backup_dir)
