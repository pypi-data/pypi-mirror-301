from sample.app import App
from sample.common.logger import Logger
from sample.svc import svc


# --------------------
## mainline
def main():
    svc.log = Logger()

    app = App()
    app.init()
    app.run()


# --------------------
if __name__ == '__main__':
    main()
