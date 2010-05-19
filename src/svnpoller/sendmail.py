import smtplib
from types import ListType, TupleType, StringType

def sendmail(fromaddr, toaddrs, msg, smtpserver):
    if type(toaddrs) in (ListType, TupleType):
        pass
    elif type(toaddrs) in (StringType,):
        toaddrs = (toaddrs,)
    else:
        raise TypeError, toaddrs

    # Add the From: and To: headers at the start!
    #sendmsg = "From: %s\r\nTo: %s\r\n\r\n%s" % (fromaddr, ", ".join(toaddrs), msg)
    sendmsg = msg

    server = smtplib.SMTP(smtpserver)
    #server.set_debuglevel(1)
    server.sendmail(fromaddr, toaddrs, sendmsg)
    server.quit()


