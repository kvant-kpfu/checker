from abc import ABC, abstractmethod
from enum import Enum
from typing import List
import sys, os, tarfile
import docker
from tempfile import TemporaryDirectory
from multiprocessing import Process

from requests.exceptions import HTTPError

# TODO: Set to False in production
VERBOSE = True


def vprint(s: str):
    if VERBOSE:
        print(s)


# Reads a file stripping newlines and spaces
def load(path: str) -> str:
    with open(path, "r") as file:
        return file.read().strip(" \n\r")


# Writes a file
def dump(path: str, data: str):
    with open(path, "w") as file:
        file.write(data)


# Holds configuration options
class Config:
    def __init__(self, time: int = 1000, memory: int = 256 * 1024 * 1024):
        self.time_limit = time
        self.memory = memory


# Holds test case data
class Test:
    def __init__(self, input: str, output: str):
        self.input = input
        self.output = output

    @staticmethod
    def load_multiple(input: List[str], output: List[str]) -> list:
        return [Test(load(i), load(o)) for i, o in zip(input, output)]


class TestResult(Enum):
    OK = "OK"
    WrongAnswer = "Wrong answer"
    TimeLimit = "Time limit exceeded"
    MemoryLimit = "Memory limit exceeded"


class NegativeResultException(Exception):
    def __init__(self, result: TestResult, *args, **kwargs):
        self.result = result
        super().__init__(*args, **kwargs)


# Base class for all types of checkers for every language-environment combination
class AbstractChecker(ABC):
    def __init__(self, tests: List[Test], config=Config()):
        self.tests = tests
        self.config = config

    @abstractmethod
    def check_solution(self, sol):
        pass


def waitForContainer(cont):
    cont.wait()


class DockerChecker(AbstractChecker):
    def __init__(
        self,
        tests: List[Test],
        base_img: str,
        interp: str,
        ext: str,
        build: List[str],
        config=Config(),
    ):
        super().__init__(tests, config=config)
        self.client = docker.DockerClient.from_env()
        self.base_img = base_img
        self.exec = interp
        self.ext = ext
        self.build = build

    def __run(self, program: str, input: str) -> str:
        # Print info to the console
        vprint("==== Running program in Docker ====")
        vprint(f"  Base image:      {self.base_img}")
        vprint(f"  Exec:            {self.exec}")
        vprint(f"  Extension:       {self.ext}")
        vprint(f"  Build commands:  {len(self.build)}")
        for cmd in self.build:
            vprint("    " + cmd)
        vprint(f"  Program size:    {len(program)}")
        vprint(f"  Input size:      {len(input)}")
        # Create a temporary directory to build our image in
        with TemporaryDirectory() as base:
            vprint(f"  Base temp dir:   {base}")
            # Construct the Dockerfile
            dockerfile = f"""
            FROM {self.base_img}:latest
            COPY program{self.ext} ./
            COPY input.txt ./
            RUN cd /"""
            # Add build commands
            for build_cmd in self.build:
                dockerfile += f"\nRUN {build_cmd}"
            # Add the execution command
            dockerfile += (
                f"\n\nCMD cat ./input.txt | {self.exec} ./program{self.ext}"
            )
            # Write everything
            dump(f"{base}/program{self.ext}", program)
            dump(f"{base}/input.txt", input)
            dump(f"{base}/Dockerfile", dockerfile)

            # Build the image and create a container from it
            vprint(
                f' >Building image (may take a while if "{self.base_img}" has '
                "not been downloaded yet)..."
            )
            image, _ = self.client.images.build(path=base, forcerm=True)
            vprint(" >Running container...")
            container = self.client.containers.run(
                image.id, detach=True, mem_limit=self.config.memory
            )
            waiter = Process(target=waitForContainer, args=[container])
            waiter.start()
            waiter.join(timeout=self.config.time_limit / 1000)
            if waiter.exitcode is None:
                waiter.kill()
                raise NegativeResultException(TestResult.TimeLimit)
            # Read the output file from the container
            # It's enclosed in a tar archive, so we have to extract it
            vprint(" >Reading result...")
            try:
                out, stat = container.get_archive("/output.txt")
                with open(f"{base}/output.tar", "wb") as tar_bin:
                    for chunk in out:
                        tar_bin.write(chunk)
                # Yeet the container as it's temporary
                container.remove(force=True)
                # Read output data
                return (
                    tarfile.open(f"{base}/output.tar")
                    .extractfile("output.txt")
                    .read()
                    .decode("utf8")
                )
            except HTTPError:
                out = container.logs().decode("utf-8").strip()
                return out

    def check_solution(self, sol: str) -> List[TestResult]:
        results = []
        program = load(sol)
        for i, test in enumerate(self.tests):
            print(f"Running test #{i + 1}...")
            try:
                output = self.__run(program, test.input)
                if output != test.output:
                    raise NegativeResultException(TestResult.WrongAnswer)
                results.append(TestResult.OK)
            # __run can raise a time or memory limit exception
            except NegativeResultException as ex:
                results.append(ex.result)
        return results


class PythonChecker(DockerChecker):
    def __init__(self, tests, config=Config()):
        super().__init__(tests, "python", "python3", ".py", [], config)


class CppChecker(DockerChecker):
    def __init__(self, tests, config=Config()):
        super().__init__(
            tests,
            "gcc",
            "",
            ".cpp",
            [
                "gcc -o program program.cpp",
                "rm program.cpp",
                "mv program program.cpp",
                "chmod +x program.cpp",
            ],
            config,
        )


class GolangChecker(DockerChecker):
    def __init__(self, tests, config=Config()):
        super().__init__(tests, "golang", "go run", ".go", [], config)


def print_results(results: List[TestResult]):
    passed = results.count(TestResult.OK)
    print(f"{passed}/{len(results)} tests passed:")
    for i, val in enumerate(results):
        print(f"Test {i + 1}: {val.value}")


if __name__ == "__main__":
    ch = PythonChecker(Test.load_multiple(["../input.txt"], ["../output.txt"]))
    print_results(ch.check_solution("../test_sol.py"))
