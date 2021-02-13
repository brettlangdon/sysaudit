def build(setup_kwargs):
    try:
        from Cython.Build import cythonize

        setup_kwargs["ext_modules"] = cythonize("sysaudit/_csysaudit.pyx")
    except ImportError:
        pass

    return setup_kwargs
