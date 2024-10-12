import os
import sys

from wasmtime import (
    ExitTrap,
    Linker,
    Module,
    Store,
    Trap,
    WasiConfig
)

def main():
    cwd = os.getcwd()

    wasi_config = WasiConfig()
    wasi_config.argv = sys.argv
    wasi_config.inherit_argv()
    wasi_config.inherit_stdin()
    wasi_config.inherit_stdout()
    wasi_config.inherit_stderr()
    wasi_config.preopen_dir(cwd, cwd)

    store = Store()
    store.set_wasi(wasi_config)

    script_relative_dir = os.path.dirname(__file__)
    wasi_binary_name = "lenv-wasip1-0.1.7.wasm"
    wasi_binary_path = os.path.join(script_relative_dir, wasi_binary_name)
    if not os.path.exists(wasi_binary_path):
        print(f"lenv: wasi binary {wasi_binary_path} not found", file=sys.stderr)
        exit(1)
        
    module = Module.from_file(store.engine, wasi_binary_path)

    linker = Linker(store.engine)
    linker.define_wasi()

    instance = linker.instantiate(store, module)
    wasi_start_func = "_start"
    start = instance.exports(store).get(wasi_start_func)

    if start is None:
        print(f"lenv: wasi {wasi_start_func} function not found", file=sys.stderr)
        exit(1)

    try:
        start(store)
    except ExitTrap as e:
        exit(e.code)
    except Trap as e:
        exit(1)

if __name__ == "__main__":
    main()
