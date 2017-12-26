from apscheduler.schedulers.blocking import BlockingScheduler
import hackerNewsTwitterBot

sched = BlockingScheduler()

sched.add_job(hackerNewsTwitterBot.main, 'interval', hours=1)

sched.start()
