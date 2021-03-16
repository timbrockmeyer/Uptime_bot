import datetime
from telegram.ext import Updater, CommandHandler

from connectivity_tracker import ConnectivityTracker

def start_cb(update, context):

    chat_id = update.message["chat"]["id"]
    tracker = ConnectivityTracker()

    feed_dict = {'chat_id':chat_id, 'tracker':tracker}

    context.bot.send_message(chat_id=chat_id, text='Starting notifications')

    # UTC timezone
    t1 = datetime.time(7, 00, 00, 000000)
    t2 = datetime.time(21, 00, 00, 000000)

    context.job_queue.run_daily(send_message, time=t1, days=tuple(range(7)), context=feed_dict)
    context.job_queue.run_daily(send_message, time=t2, days=tuple(range(7)), context=feed_dict)

def stop_cb(update, context):
    chat_id = update.message["chat"]["id"]
    context.job_queue.stop()
    context.bot.send_message(chat_id=chat_id, text='Stopping notifications')

def send_message(context):
    context_dict = context.job.context
    chat_id = context_dict['chat_id']
    tracker = context_dict['tracker']

    # Get up/downtime in seconds and convert to hours, minutes, seconds
    uptime = round(tracker.uptime)
    uptime = datetime.datetime.fromtimestamp(uptime, datetime.timezone.utc)
    downtime = round(tracker.downtime)
    downtime = datetime.datetime.fromtimestamp(downtime, datetime.timezone.utc)

    msg = 'Scheduled status update:\n Uptime:'\
            + uptime.strftime("%H:%M:%S")\
            + '\nDowntime: ' + downtime.strftime("%H:%M:%S")

    context.bot.send_message(chat_id=chat_id, text=msg)

updater = Updater("1528330919:AAEh7J5DALxZ7S78cPPynvXU-5_k8kOrljg")

# Get the dispatcher to register handlers
dp = updater.dispatcher

# Handlers for commands
start_handler = CommandHandler('start', start_cb, pass_job_queue=True)
stop_handler = CommandHandler('stop', stop_cb, pass_job_queue=True)

dp.add_handler(start_handler)
dp.add_handler(stop_handler)

# Start the Bot
updater.start_polling()

updater.idle()
