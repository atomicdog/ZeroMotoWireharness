### Zero SR/S Wire Harness

Wiring harness documentation traced from a Zero Motorcycles SR/S (Gen3 FST platform).

**[View diagrams on GitHub Pages](https://atomicdog.github.io/ZeroMotoWireharness/)**

#### Development

Requires [uv](https://docs.astral.sh/uv/) and system `graphviz`.

```bash
make setup   # install dependencies
make build   # generate diagrams → docs/
```

Harness sources are in `harness/`. Diagrams are built by CI and published to the `gh-pages` branch on every push to `master`.
