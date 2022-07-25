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


def sortly_conversion(sku) -> str:

    from .sortly import sku_dict

    if "sy://" in sku:

        sortly_id = sku.split("/")[-1]

        bddw_sku = sku_dict[sortly_id]

        return bddw_sku

    else:

        return sku
