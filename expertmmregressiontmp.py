def get_module_contents():
    results = None
    import inspect
    import PIL
    tmp_tuples = inspect.getmembers(PIL, inspect.isroutine)
    results = list()
    for function_tuple in tmp_tuples:
        results.append(function_tuple[0])
    return results

