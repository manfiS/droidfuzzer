from blessings import Terminal
from datetime import datetime
from os import listdir, getcwd
from subprocess import Popen, PIPE, CalledProcessError
from framework.utilities.process_management import ProcessManagement
import time
t = Terminal()


class DocumentViewerFuzzer(object):

    tag = "Samsung Core Prime Document Viewer Fuzzer "

    @staticmethod
    def run():
        print(t.yellow("[{0}] Starting fuzzer (!)".format(datetime.now())))

        _test_cases = [

            "docx",
            "doc",
            "pdf"
        ]

        for test_case in _test_cases:
            print(t.yellow("[{0}] Available test-case : ".format(datetime.now())) + test_case)
        # Get target test-case
        target = raw_input(t.yellow("[{0}] Select test-case : ".format(datetime.now())))
        # Clear logcat before running test-cases
        ProcessManagement.clear()
        processes = list()

        for test_case in _test_cases:
            if target == test_case:
                for item in listdir("".join([getcwd(), "/test-cases/{0}".format(target)])):
                    print(t.yellow("[{0}] Fuzzing : ".format(datetime.now())) + item)
                    try:
                        # Push the test-case to the device
                        # -----------------------------------------------------------------------------
                        pusher = Popen("".join([getcwd(), "/bin/adb push ",
                                                "{0}/test-cases/{1}/{2}".format(getcwd(), target, item),
                                                " /data/local/tmp"]),
                                       stdout=PIPE,
                                       shell=True)
                        processes.append(pusher)
                        time.sleep(2)
                        viewer = Popen(
                            "".join([getcwd(), "/bin/adb shell su '-c am start ",
                                     "-n com.hancom.office.viewer/com.tf.thinkdroid.write.ni.viewer.WriteViewPlusActivity ",
                                     "-d file:///data/local/tmp/{0}'".format(item)]),
                            stdout=PIPE,
                            shell=True)
                        processes.append(viewer)
                        time.sleep(1)
                        # Add each test-case as a log entry
                        # -------------------------------------------------------------------------------
                        log = Popen(
                            "".join([getcwd(), "/bin/adb shell log -p v -t 'Filename' {0}".format(item)]),
                            stdout=PIPE,
                            shell=True)
                        processes.append(log)
                        time.sleep(1)
                        # Find and write fatal log entries (SIGSEGV)
                        # ----------------------------------------------------------------------------------------
                        fatal = Popen(
                            "".join([getcwd(), "/bin/adb logcat -v time *:F > ",
                                               "logs/samsung_core_prime_document_viewer_{0}_logs".format(target)]),
                            stdout=PIPE,
                            shell=True)
                        processes.append(fatal)
                        time.sleep(1)
                        # Find and write test-case entry logs
                        # ----------------------------------------------------------------------------------------
                        logcat = Popen(
                            "".join([getcwd(), "/bin/adb logcat -v time *:F -s 'Filename' >> ",
                                               "logs/samsung_core_prime_document_viewer_{0}_logs".format(target)]),
                            stdout=PIPE,
                            shell=True)
                        processes.append(logcat)
                        time.sleep(2)
                        # Remove test-case from device
                        # ----------------------------------------------------------------------------------
                        remove = Popen(
                            "".join([getcwd(), "/bin/adb shell su '-c rm /data/local/tmp/{0}'".format(item)]),
                            stdout=PIPE,
                            shell=True)
                        processes.append(remove)
                        time.sleep(2)
                        # Kill target application process
                        # ------------------------------------------------------------------------------
                        Popen(
                            "".join([getcwd(), "/bin/adb shell am force-stop com.hancom.office.viewer"]),
                            shell=True)
                        # Kill all adb processes
                        #
                        ProcessManagement.kill(processes)
                    except CalledProcessError as called_process_error:
                        raise called_process_error



