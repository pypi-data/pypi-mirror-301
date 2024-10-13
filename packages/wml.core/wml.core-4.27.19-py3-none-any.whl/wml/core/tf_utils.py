"""Useful TensorFlow-based util functions. The module requires tensorflow or tensorflow-gpu package."""


from mt.gpu import detect_machine, get_mem_info
from mt import tf  # to monkey-patch tf, if required


__all__ = [
    "is_tx2",
    "num_gpus",
    "tf_major_version",
    "set_gpu_alloc_policy",
]


def is_tx2():
    """Detects if the machine is a TX2 without using TensorFlow.

    Returns
    -------
    bool
        whether or not we are on a TX2

    Notes
    -----
    You can also use :func:`mt.gpu.detect_machine` which is more general.
    """

    return detect_machine() in [
        "arm64-tx2",
        "arm64-j43",
        "arm64-j45",
        "arm64-n45",
        "arm64-o51",
    ]


def num_gpus():
    """Counts the number of GPU devices that we can use.

    Returns
    -------
    int
        the number of GPU devices detected
    """

    return len(get_mem_info()["gpus"])


def tf_major_version():
    """Checks if TensorFlow has been installed and which major version are we on.

    Returns
    -------
    int
        -1 if no TensorFlow is imported. 0 to 2 corresponding to the major version.
    """
    try:
        from mt import tf

        return 2
    except ImportError:
        return -1


def set_gpu_alloc_policy(
    target,
    gpu_max_memory=1024 * 1024 * 1024,
    allow_growth=True,
    logger=None,
):
    """Sets a policy for allocating gpu memory depending on the target. See notes.

    Parameters
    ----------
    target : {'tf2'}
        target session type to set a gpu memory allocation policy. See notes.
    gpu_max_memory : int or None
        maximum memory in bytes to be used by the GPU. If None is specified, we let TF decide.
    allow_growth : bool
        allow GPU allocation to grow dynamically or not
    logger : mt.logg.IndentedLoggerAdapter, optional
        the logger (optional)

    Notes
    -----
    If target is 'tf2', we set the policy defined by `gpu_max_memory` on the current uninitialised
    tf2 config, but we return None. Argument `allow_growth` has no effect in this case.

    Raises
    ------
    ValueError
        if the target is not in the above list
    """

    if target in ["mlkeras", "tf1keras"]:
        raise NotImplementedError(
            f"Target '{target}' no longer supported. Please downgrade wml.core or change to a different target."
        )

    if target == "tf2":
        if tf_major_version() < 2:
            raise ImportError("TensorFlow v2+ is not installed. Please install it.")

        if gpu_max_memory is None:
            if allow_growth:
                import tensorflow.config.experimental as tce

                gpus = tce.list_physical_devices("GPU")
                if gpus:
                    if logger:
                        logger.debug(
                            "Setting allowing growth in TF2 {} gpus.".format(len(gpus))
                        )
                    for gpu in gpus:
                        tce.set_memory_growth(gpu, True)
                else:
                    if logger:
                        logger.warning("There is no GPU to set the TF2 policy.")
            else:
                if logger:
                    logger.warning(
                        "There is nothing to do to set the GPU policy for TF2.".format(
                            target
                        )
                    )
        else:
            mega = 1024 * 1024
            memory_limit = (gpu_max_memory + mega - 1) // mega

            import tensorflow.config.experimental as tce

            gpus = tce.list_physical_devices("GPU")
            if gpus:
                if logger:
                    logger.debug(
                        "Setting in TF2 max gpu memory {} MBs on {} gpus.".format(
                            memory_limit, len(gpus)
                        )
                    )
                for gpu in gpus:
                    tce.set_virtual_device_configuration(
                        gpu, [tce.VirtualDeviceConfiguration(memory_limit=memory_limit)]
                    )
            else:
                if logger:
                    logger.warning("There is no GPU to set the TF2 policy.")

        return None

    raise ValueError(f"Target must be in ['tf2']. Got '{target}'.")
