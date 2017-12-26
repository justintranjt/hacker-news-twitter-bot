from apscheduler.schedulers.blocking import BlockingScheduler
import hackerNewsTwitterBot

sched = BlockingScheduler()

sched.add_job(hackerNewsTwitterBot.main, 'interval', minutes=1)

sched.start()
