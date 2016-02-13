from datetime import datetime
from os import getcwd
from cmd2 import Cmd as DroidFuzzer
from blessings import Terminal
from enum import Enum
import json
t = Terminal()


class CommandEnum(Enum):

    # command line enum types
    # --------------------------------------------------
    config_file_path = "/framework/modules/modules.json"
    available_module = "Available modules"
    module_does_not_exist = "Module does not exist"


class Run(DroidFuzzer):

    def __int__(self):
        DroidFuzzer.__init__(self)

    @staticmethod
    def do_fuzzer(args):
        """
        Usage :
        Description :
        """
        if args == "show":
            with open("".join([getcwd(), CommandEnum.config_file_path.value])) as json_file:
                _data = json_file.read()
                # https://gist.github.com/lsauer/6512956
                _config = json.loads(_data.strip(" '<>()[]\"` ").replace("\'", '\"'))
                for members, member in _config.items():
                    for module in member:
                        for module_name, fuzzers in module.items():
                            for fuzzer in fuzzers:
                                print(t.yellow("[{0}] {1} : ".format(datetime.now(),
                                                                     CommandEnum.available_module.value)) +
                                      "".join([module_name, " : ", fuzzer]))
        elif args.split()[0] == "module":
            try:
                from framework.modules.samsung_core_prime.fuzzer_factory import FuzzerFactory
                _factory_fuzzer = FuzzerFactory.get_fuzzer(args.split()[1])
                if _factory_fuzzer:
                    print(t.yellow("[{0}] Loading : ".format(datetime.now())) + _factory_fuzzer.tag)
                    _factory_fuzzer.run()
                else:
                    print(t.yellow("[{0}] ".format(datetime.now())) +
                          t.white("{0} (!)".format(CommandEnum.module_does_not_exist.value)))
            except ImportError:
                raise
