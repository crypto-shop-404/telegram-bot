import aiogram.types
from aiogram import dispatcher
from aiogram import filters

import config
import responses.backup
import tasks
from filters import is_admin
from loader import dp, scheduler
from states import backup_states


@dp.message_handler(filters.Text('💾 Backup'), is_admin.IsUserAdmin())
async def backup(message: aiogram.types.Message):
    await responses.backup.BackupResponse(message)


@dp.message_handler(filters.Text('📀 Manual Backup'), filters.IDFilter(config.BackupSettings().admin_id))
async def backup(_):
    tasks.make_database_backup()
    await tasks.send_database_backup_to_admin(config.BackupSettings().admin_id)


@dp.message_handler(filters.Text('📲 Backup Full Shop'), filters.IDFilter(config.BackupSettings().admin_id))
async def full_backup(_):
    admin_id = config.BackupSettings().admin_id
    tasks.make_database_backup()
    tasks.make_project_backup()
    await tasks.send_database_backup_to_admin(admin_id)
    await tasks.send_project_backup_to_admin(admin_id)


@dp.message_handler(filters.Text('⏰ Manage Cron'), is_admin.IsUserAdmin())
async def manage_backup_schedule(message: aiogram.types.Message):
    await responses.backup.BackupPeriodResponse(message)
    await backup_states.BackupStates.waiting_for_backup_period.set()


@dp.message_handler(is_admin.IsUserAdmin(), state=backup_states.BackupStates.waiting_for_backup_period)
async def backup_period_handler(message: aiogram.types.Message, state: dispatcher.FSMContext):
    backup_periods = {
        '⏱ Every Hour': '0 */1 * * *',
        '⏱ Every Six Hours': '0 */6 * * *',
        '⏱ Every 24 Hours': '0 0 */1 * *'
    }
    backup_period = backup_periods.get(message.text, message.text)
    if tasks.check_period(backup_period):
        await responses.backup.SendingBackupPeriodResponse(message)
        await state.update_data({
            'backup_period': backup_periods.get(message.text, message.text),
            'humanized_backup_period':
                message.text.replace('⏱ ', '').lower() if message.text in backup_periods else ''
        })
        await backup_states.BackupStates.next()
    else:
        await responses.backup.InvalidPeriodResponse(message)


@dp.message_handler(is_admin.IsUserAdmin(),
                    state=backup_states.BackupStates.waiting_for_sending_backup_period)
async def sending_backup_period_handler(message: aiogram.types.Message, state: dispatcher.FSMContext):
    sending_backup_periods = {
        '⏱ Everyday': '0 0 */1 * *',
        '⏱ Every 3 Days': '0 0 */3 * *',
        '⏱ Every Week': '0 0 */7 * *'
    }
    data = await state.get_data()
    backup_period = data['backup_period']
    humanized_backup_period = data['humanized_backup_period']
    await state.finish()
    sending_backup_period = sending_backup_periods.get(message.text, message.text)
    humanized_sending_backup_periods = (
        message.text.replace('⏱ ', '').lower()
        if message.text in sending_backup_periods else ''
    )
    if tasks.check_period(sending_backup_period):
        tasks.reschedule_task(scheduler, 'make_database_backup', sending_backup_period)
        settings = config.TOMLSettings()
        tasks.reschedule_task(scheduler, 'send_database_backup_to_admin', backup_period)
        settings['backup']['backup_period'] = backup_period
        settings['backup']['sending_backup_period'] = sending_backup_period
        settings.save()
        await responses.backup.SuccessBackupSettingResponse(
            message, humanized_backup_period, humanized_sending_backup_periods, config.BACKUP_PATH
        )
    else:
        await responses.backup.InvalidPeriodResponse(message)
