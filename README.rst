SchedPy
=======

.. image:: https://badge.fury.io/py/schedpy.svg
    :target: https://badge.fury.io/py/schedpy

.. image:: https://img.shields.io/badge/Gitter-Join_chat-brightgreen.svg
    :target: https://gitter.im/schedpy/community

.. image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/schedpy/schedpy/master?filepath=schedpy.ipynb

**SchedPy** is an opensource **Advanced Cron or Job Scheduler** written in Python.
It has multiple functionalities for scheduling a Job, you can activate the Scheduler
for a specific time period given a time period window, which may be recurring every second,
hour or so. For example: activate scheduler every 5 hours for the first two weeks of the
quarter could be written as:

>>> def test():
...     print("Scheduler on!")
>>> schedule.first(2).weeks.of(3).months.every(5).hours.do(test)

In the above example, the active period is the first two weeks, given 3 months window and
the scheduler is triggered or recurring every 5 hours.

SchedPy API
===========

>>> schedule.___1___(2).___3___.of(4).___5___.every(6).___7___.on(8).at(9).do(10)

1. first/last
2. value (default: 1)
3. days/weeks/months
4. value (default: 1)
5. weeks/months
6. value (default: 1)
7. minute/hour/day
8. days (monday, tuesday..) # todo
9. time (24 hour clock "22:00") # todo
10. Job/Function to run

Example
=======
Let's play with some simple examples:

>>> from schedpy import schedule
>>> from datetime import date, timedelta
>>> def test():
...     print("Scheduler on!")
...
>>> schedule.first().days.of().days.every().days.do(test)
2020-01-14 2020-01-14
Scheduler on!
.
.
>>> schedule.first().days.of().days.every().seconds.do(test)
2020-01-14 2020-01-14
Scheduler on!
Scheduler on!
Scheduler on!
.
.

In the first example, we have scheduled for every day starting from the day
we run the code. In the second example, we have scheduled for every second from
the day we run the code. One can also set scheduler configs as to which day and date
the scheduler should start from. for example:

>>> schedule.set_configs("mon", date(2019, 1 ,15))
Start day set to: 0/Monday
Start date set to: 2019-01-15

References
==========

* https://github.com/dbader/schedule