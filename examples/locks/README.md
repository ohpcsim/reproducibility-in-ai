# Example lock files

The starter project's `environment.yml` with pandas added, locked on four machines on November 8, 2026, with the page's commands. Each machine started with an empty package cache.

| File | Machine | OS | Architecture | conda | Solve (UTC) |
|---|---|---|---|---|---|
| `explicit-linux-64-wsl2.txt` | Windows PC, WSL2 | Ubuntu 24.04.1 on Windows 11 | x86_64 | 26.9.4 | 18:49:55 to 18:50:00 |
| `explicit-linux-64-binder.txt` | mybinder.org session | Ubuntu 24.04.5 | x86_64 | 26.3.2 | 18:49:50 to 18:50:13 |
| `explicit-linux-aarch64-spark.txt` | NVIDIA DGX Spark | Ubuntu 24.04.5 | aarch64 | 26.9.4 | 18:49:57 to 18:50:00 |
| `explicit-osx-arm64-mac.txt` | Mac with Apple M3 Pro | macOS 27.0.1 | arm64 | 26.9.4 | 18:50:02 to 18:50:11 |
| `uv.lock` | All four | | | uv 0.13.7 | 18:50:02 to 18:50:17 |

- Every machine used conda-forge only, with flexible channel priority. The three local machines used Miniforge 26.9.4. Binder used the conda in its image.
- Every machine got the same versions, such as python 3.12.16, numpy 2.5.4 and pandas 3.1.1. The build strings and platform folders differ.
- The Linux locks have 38 packages and the Mac lock has 33. Linux adds `ld_impl`, `libgomp`, `libnsl`, `libstdcxx`, `libuuid`, `libxcrypt` and `zstd`. The Mac adds `libcxx` and `llvm-openmp`.
- 9 packages are `noarch`, so their lines are the same on every platform.
- The WSL2 and Binder locks list the same 38 packages with the same checksums. Only line 4, `# created-by: conda <version>`, differs.
- Both reported `__glibc=2.39`. WSL2 also reported `__cuda=13.3`, but no package here depends on CUDA.
- `uv add pandas` wrote the same `uv.lock`, byte for byte, on all four machines.
