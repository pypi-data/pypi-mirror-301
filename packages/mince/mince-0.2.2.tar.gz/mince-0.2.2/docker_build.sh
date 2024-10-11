
docker build \
    --no-cache \
    --progress=plain \
    --file /home/storm/repos/mince/mince/ops/Dockerfile \
    --build-arg PACKAGE="stables" \
    -t mince-stables \
    "/home/storm/repos/stables"
