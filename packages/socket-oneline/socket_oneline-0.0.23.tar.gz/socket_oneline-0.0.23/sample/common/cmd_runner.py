import subprocess
import threading
import time

from sample.svc import svc


# --------------------
## holds various functions to run OS processes
class CmdRunner:

    # --------------------
    ## run a task in a thread.
    #
    # run_fn has the following expected definition and behavior:
    #     def your_function(self, proc):
    #         # ... do work ...
    #
    #         # return True if you want your function to be called again
    #         # return None or False
    #         return True
    #
    # @param tag         a logging tag
    # @param cmd         the command to execute
    # @param run_fn      the function to run in the background thread
    # @param working_dir the working directory, defaults to '.'
    # @return the thread handle
    def start_task_bg(self, tag, cmd, run_fn, working_dir='.'):
        hthread = threading.Thread(target=self._runner,
                                   args=(tag, cmd, run_fn, working_dir))
        hthread.daemon = True
        hthread.start()
        # wait for thread to start
        time.sleep(0.1)
        return hthread

    # --------------------
    ## starts a long running process
    # it is up to the caller to handle stdout and shutting down
    #
    # @param tag  a logging tag
    # @param cmd  the command to execute
    # @param working_dir the working directory, defaults to '.'
    # @return the Popen process handle
    def start_task(self, tag, cmd, working_dir='.'):
        svc.log.info(f'{tag}:')
        svc.log.info(f'   cmd : {cmd}')
        svc.log.info(f'   dir : {working_dir}')

        proc = self._start_process(cmd, working_dir)
        svc.log.info(f'   pid : {proc.pid}')

        return proc

    # === Private

    # --------------------
    ## create and start a process instance for
    # the given command line and working directory
    #
    # @param cmd         the command to execute
    # @param working_dir the working directory
    # @return the Popen process handle
    def _start_process(self, cmd, working_dir):
        proc = subprocess.Popen(cmd,
                                shell=True,
                                bufsize=0,
                                universal_newlines=True,
                                stdin=None,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                cwd=working_dir,
                                )
        return proc

    # --------------------
    ## the background thread used for running tasks. Instantiates a process and calls run_fn continually
    # until requested to stop
    #
    # @param tag         a logging tag
    # @param cmd         the command to execute
    # @param run_fn      the function to run in the background thread
    # @param working_dir the working directory, defaults to '.'
    # @return None
    def _runner(self, tag, cmd, run_fn, working_dir):
        proc = self.start_task(tag, cmd, working_dir)
        while True:
            ok = run_fn(proc)
            if ok is None or not ok:
                break
            time.sleep(0.1)
        proc.terminate()

    # --------------------
    ## start a bg process, write all output to stdout
    #
    # @param tag         a logging tag
    # @param cmd         the command to execute
    # @param working_dir the working directory, defaults to '.'
    # @return the thread
    def run_process(self, tag, cmd, working_dir=None):
        if working_dir is None:
            working_dir = '.'

        hthread = threading.Thread(target=self._runner2,
                                   args=(tag, cmd, working_dir))
        hthread.daemon = True
        hthread.start()
        # wait for thread to start
        time.sleep(0.1)
        return hthread

    # --------------------
    ## start a process with the given command, write output to stdout
    #
    # @param tag         a logging tag
    # @param cmd         the command to execute
    # @param working_dir the working directory, defaults to '.'
    # @return None
    def _runner2(self, tag, cmd, working_dir):
        proc = self._start_process(cmd, working_dir=working_dir)
        lastline = ''
        lineno = 0
        while True:
            if lastline:
                print(lastline.strip())

            retcode = proc.poll()
            if retcode is not None:
                break
            lastline = proc.stdout.readline()
            lineno += 1

        svc.log.info(f'{tag} rc={proc.returncode}')
