def hello_world() -> str:
    """Return a greeting string for the FTP module.

    This function generates a simple "Hello World" message that includes
    the module's full package path.

    Returns:
        str: A greeting string containing the package and module name.

    Example:
        >>> from openbambucommands.ftp import hello
        >>> hello.hello_world()
        'Hello World from openbambucommands.ftp.hello'
    """
    return f"Hello World from {__name__}!"
