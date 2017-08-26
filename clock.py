from apscheduler.schedulers.blocking import BlockingScheduler
import hackerNewsTwitterBotLOCAL

sched = BlockingScheduler()

sched.add_job(hackerNewsTwitterBotLOCAL.main, 'interval', hours=2)

sched.start()
