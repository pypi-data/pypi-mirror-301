import os

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\","/"):
    from Orange.widgets.orangecontrib.AAIT.utils.tools import first_time_check
else:
    from orangecontrib.AAIT.utils.tools import first_time_check