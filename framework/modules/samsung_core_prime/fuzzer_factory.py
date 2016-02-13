from framework.modules.samsung_core_prime.document_viewer_fuzzer import DocumentViewerFuzzer
from enum import Enum


class FuzzerFactoryEnum(Enum):

    document_viewer = "document_viewer_fuzzer"


class FuzzerFactory:

    @staticmethod
    def get_fuzzer(f):
        if f == FuzzerFactoryEnum.document_viewer.value:
            return DocumentViewerFuzzer()



