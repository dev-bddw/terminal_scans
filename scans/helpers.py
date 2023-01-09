import socket


def is_connected(hostname):
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(hostname)
        # connect to the host -- tells us if the host is actually reachable
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except Exception:
        pass  # we ignore any errors, returning False
    return False


def process_sortly(code: str) -> dict:
    """
    Processes the archaic sortly label code.
    Expects a string like this: sy://o2/m_qrcode_single/S7X1ZT0106
    Returns a scan dictionary w/ bddw native sku and .xx as tracking number
    if it has '.xx'.

    """

    from .sortly import sku_dict

    sortly_id = code.split("/")[-1]

    bddw_sku,tracking_number = sku_dict.get(sortly_id, ('',''))

    return {"item": bddw_sku, "tracking": tracking_number}
