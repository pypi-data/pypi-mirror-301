from sample.common.logger import Logger
from sample.server import Server
from sample.svc import svc


# --------------------
## mainline
# runs the OnelineServer wrapper
def main():
    svc.log = Logger()

    server = Server()
    server.init()

    server.wait_until_done()
    server.term()


# --------------------
if __name__ == '__main__':
    main()
