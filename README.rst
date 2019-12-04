SchedPy
=======

.. image:: https://img.shields.io/badge/Gitter-Join_chat-brightgreen.svg
    :target: https://gitter.im/schedpy/community

.. image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/schedpy/schedpy/master?filepath=schedpy.ipynb

Advanced Cron or Job Scheduler in Python


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
9. time (24 hour clock "22:00")# todo
10. Job/Function to run

References
==========

https://github.com/dbader/schedule