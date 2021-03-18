import datetime
from telegram.ext import Updater, CommandHandler

from connectivity_tracker import ConnectivityTracker

class UptimeBot:

    def __init__(self):

        # Get bot configurations (Token)
        with open('bot.config', 'r') as f:
            lines = f.read().splitlines()
            for line in lines:
                var, value = line.split('=')

                # Parse config variables
                if(var == 'token'): token = value

        # Create the Bot from token
        updater = Updater(token)

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # Create handlers for commands, e.g. /start, /stop, etc.
        start_handler = CommandHandler('start', self.start_cb, pass_job_queue=True)
        stop_handler = CommandHandler('stop', self.stop_cb, pass_job_queue=True)

        # Add handlers to the dispatcher
        dp.add_handler(start_handler)
        dp.add_handler(stop_handler)

        # Create the time tracker
        self.tracker = ConnectivityTracker()

        # Start the Bot
        updater.start_polling()

        # Spin it
        updater.idle()

    def start_cb(self, update, context):

        chat_id = update.message["chat"]["id"]

        # Dict that gets passed onto callbacks via the context
        feed_dict = {'chat_id':chat_id, 'tracker':self.tracker}

        # Times in UTC timezone
        t1 = datetime.time(7, 00, 00, 000000)
        t2 = datetime.time(21, 00, 00, 000000)

        # Add daily status report jobs
        context.job_queue.run_daily(self.status_message, time=t1, days=tuple(range(7)), context=feed_dict)
        context.job_queue.run_daily(self.status_message, time=t2, days=tuple(range(7)), context=feed_dict)

        # Confirm job creation to the user
        context.bot.send_message(chat_id=chat_id, parse_mode="Markdown", text='_Scheduling status reports_')

    def stop_cb(self, update, context):
        chat_id = update.message["chat"]["id"]
        context.job_queue.stop()
        context.bot.send_message(chat_id=chat_id, parse_mode="Markdown", text='_Stopping notifications_')

    def status_message(self, context):
        # Extract additional information passed through the context
        context_dict = context.job.context
        chat_id = context_dict['chat_id']

        # Get up/downtime formatted strings
        uptime, downtime = self.tracker.report()

        # Send status report
        msg = '*Connectivity since last report*\nUptime: '+ uptime\
                + '\nDowntime: ' + downtime
        context.bot.send_message(chat_id=chat_id, parse_mode="Markdown", text=msg)

        # Reset timers
        self.tracker.reset()

if __name__ == '__main__':
    UptimeBot()
