from apscheduler.schedulers.blocking import BlockingScheduler
import hackerNewsTwitterBot

sched = BlockingScheduler()

sched.add_job(hackerNewsTwitterBot.main, 'interval', hours=4)

sched.start()
