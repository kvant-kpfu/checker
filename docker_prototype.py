#!/usr/bin/env python3

import docker, os, tarfile
from tempfile import TemporaryDirectory

PROGRAM = """
with open("input.txt", "r") as i:
    with open("output.txt", "w") as o:
        o.write(i.read() + " given as input")
"""
VERBOSE = True

client = docker.DockerClient.from_env()

def dump(path: str, data: str):
    with open(path, "w") as file:
        file.write(data)

def vprint(s: str):
    if VERBOSE:
        print(s)

def run(base_img: str, exec: str, ext: str, build: list, program: str, input: str) -> str:
    # Print info to the console
    vprint( "==== Running program in Docker ====")
    vprint(f"  Base image:      {base_img}")
    vprint(f"  Exec:            {exec}")
    vprint(f"  Extension:       {ext}")
    vprint(f"  Build commands:  {len(build)}")
    for cmd in build:
        vprint("    " + cmd)
    vprint(f"  Program size:    {len(program)}")
    vprint(f"  Input size:      {len(input)}")
    # Create a temporary directory to build our image in
    with TemporaryDirectory() as base:
        vprint(f"  Base temp dir:   {base}")
        # Construct the Dockerfile
        dockerfile = f"""
        FROM {base_img}:latest
        COPY program.{ext} ./
        COPY input.txt ./
        RUN cd /"""
        # Add build commands
        for build_cmd in build:
            dockerfile += f"\nRUN {build}"
        # Add the execution command
        dockerfile += f"\n\nCMD {exec} ./program.{ext}"
        # Write everything
        dump(f"{base}/program.{ext}", program)
        dump(f"{base}/input.txt", input)
        dump(f"{base}/Dockerfile", dockerfile)

        # Build the image and create a container from it
        vprint(f"Building image (may take a while if \"{base_img}\" has not been downloaded yet)...")
        image, _ = client.images.build(path=base, forcerm=True)
        container = client.containers.run(image.id, detach=True)
        container.wait()
        # Extract the output file out of the container
        # It's enclosed in a tar archive, so we have to extract it
        out, stat = container.get_archive("/output.txt")
        with open(f"{base}/output.tar", "wb") as tar_bin:
            for chunk in out:
                tar_bin.write(chunk)
        # Yeet the container as it's temporary
        container.remove(force=True)
        # Read output data
        return tarfile.open(f"{base}/output.tar")\
                      .extractfile("output.txt")\
                      .read()\
                      .decode("utf8")

print(run("python", "python3", "py", [], PROGRAM, "hello, world!"))