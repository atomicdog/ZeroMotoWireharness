### Zero FST platform Wire Harness

Wiring harness documentation traced from a Zero Motorcycles SR/S (Gen3 FST platform).

**[View diagrams on GitHub Pages](https://atomicdog.github.io/ZeroMotoWireharness/)**

#### Development

Requires [uv](https://docs.astral.sh/uv/) and system `graphviz`. The site is built with [Zensical](https://zensical.org/).

```bash
make setup   # install dependencies
make build   # generate diagrams → docs/harness/, build site → site/
make serve   # build, then preview the site locally
```

Harness sources are in `harness/`. Diagrams and the site are built by CI and published to the `gh-pages` branch on every push to `master`.
