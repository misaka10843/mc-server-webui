import asyncio
import json
import re


async def docker(*args, timeout=30):
    process = await asyncio.create_subprocess_exec("docker", *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout)
    except TimeoutError:
        process.kill()
        await process.wait()
        raise RuntimeError("Docker command timed out")
    if process.returncode:
        raise RuntimeError("Docker command failed: " + stderr.decode(errors="replace")[:500])
    return stdout.decode().strip()


async def inspect_container(container):
    raw = await docker("inspect", "--format", "{{json .}}", container)
    details = json.loads(raw)
    state = dict(details["State"])
    state["restart_policy"] = details["HostConfig"]["RestartPolicy"]["Name"]
    state["restart_count"] = details["RestartCount"]
    return details["Id"], state


async def shutdown_host(container, request_shutdown):
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_.-]{0,127}", container):
        raise ValueError("Invalid configured container name")
    container_id, before = await inspect_container(container)
    if before["Status"] != "running" or before["restart_policy"] not in ("no", ""):
        raise RuntimeError("Minecraft container must be running with restart policy disabled")
    await request_shutdown()
    result = await docker("wait", container_id, timeout=300)
    if result != "0":
        raise RuntimeError("Minecraft container did not exit normally")
    checked_id, after = await inspect_container(container_id)
    if checked_id != container_id or after["Status"] != "exited" or after["ExitCode"] != 0 or after["StartedAt"] != before["StartedAt"] or after["restart_policy"] not in ("no", "") or after["restart_count"] != before["restart_count"]:
        raise RuntimeError("Minecraft container state changed during shutdown")
    process = await asyncio.create_subprocess_exec("sudo", "-n", "/usr/local/libexec/mc-server-poweroff", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    try:
        _, stderr = await asyncio.wait_for(process.communicate(), 15)
    except TimeoutError:
        process.kill()
        await process.wait()
        raise RuntimeError("Poweroff helper timed out")
    if process.returncode:
        raise RuntimeError("Poweroff helper failed: " + stderr.decode(errors="replace")[:500])
