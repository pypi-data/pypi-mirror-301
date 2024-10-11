import re
from typing import List, Sequence

from furiosa_llm.parallelize.config import Device


def parse_devices_str(s: str) -> List[Device]:
    """
    Parse a string representation indicating specific devices (e.g., cpu:0,cpu:1,gpu:0)
    :param s: a string representing of devices
    :return: a list of `Device` objects
    """
    devices = []
    for device_str in s.split(","):
        device_str = device_str.strip()
        devices.append(Device(device_str))
    return devices


PE_RANGE_IDX_RE = re.compile(r"(\d)-(\d)")
NUM_PES_PER_NPU = 8


def normalize_devices_into_single_pes(devices: Sequence[Device]) -> List[Device]:
    """
    Normalize devices into single PEs. This function is only for npu devices. Allowed device formats are "npu:0:3", "npu:0:4-7", "npu:0:*".
    :param devices: a list of Device objects
    :return: a list of `Device` objects which are all single PEs, sorted by npu index and pe index.
    """
    ret = []

    for device in devices:
        kind, *rest = device.split(":")

        if len(rest) != 2:
            raise ValueError("Invalid device string: {device}")

        if kind != "npu":
            raise ValueError("Only npu devices can be normalized.")

        npu_idx, pe_idx = rest

        if pe_idx == "*":
            for idx in range(NUM_PES_PER_NPU):
                ret.append(Device(f"npu:{npu_idx}:{idx }"))
        elif PE_RANGE_IDX_RE.match(pe_idx):
            start, end = pe_idx.split("-")
            for idx in range(int(start), int(end) + 1):
                ret.append(Device(f"npu:{npu_idx}:{idx}"))
        elif pe_idx.isdigit():
            ret.append(device)
        else:
            raise ValueError("Invalid device string: {device}")

    # This sorts single pes by its npu index and pe index.
    ret.sort()

    return ret


def fusion_pes(devices: Sequence[Device]) -> Device:
    """Given a list of single pe devices, fuse them into a single fused pe device."""
    num_pes = len(devices)
    if num_pes not in (1, 2, 4):
        raise ValueError("Only 1, 2, 4 PEs can be fused.")

    if num_pes == 1:
        return devices[0]
    devices = sorted(devices)

    # All devices must be sigle pe (in the form of "npu:\d:\d")
    dev_idx = devices[0].idx

    start_pe_idx = int(devices[0].pe_idx)

    if start_pe_idx % num_pes != 0:
        raise ValueError(f"Invalid start pe index for fusion: {start_pe_idx}")

    for device, expected_pe_idx in zip(devices, range(start_pe_idx, start_pe_idx + num_pes)):
        if int(device.pe_idx) != expected_pe_idx:
            raise ValueError(
                "Unexpected pe index. Expected: {expected_pe_idx}, actual: {device.idx}"
            )

    return Device(f"npu:{dev_idx}:{start_pe_idx}-{start_pe_idx + num_pes - 1}")
