# thearchitect

## docker

In order to build the docker,

```console
docker build -t thearchitect .
```

In order to use the docker, for a `main.c` to compile available at `/tmp/data/main.c`, in order to get a `main.exe` under `/tmp/data/main.exe`,

```console
docker run --rm -v /tmp/data:/data thearchitect /data/main.c /data/main.exe
```
