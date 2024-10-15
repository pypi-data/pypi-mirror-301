from pkgbox.fn import *
from pkgbox import islack
from pkgbox.date_fn import *
from pkgbox import charts
from pkgbox.num_fn import *


dt = date_fn.Cdt()
pysqldf = lambda q: sqldf(q, globals())

remarks = ""
def remark(text):
    global remarks
    if remarks == "":
        remarks = text
    else:
        remarks = f"{remarks}\n{text}"
    sb.glue("remarks", remarks)