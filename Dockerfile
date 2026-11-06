FROM rust:1.88-bookworm AS builder
WORKDIR /workspace
COPY rust/kinetics-infra ./rust/kinetics-infra
WORKDIR /workspace/rust/kinetics-infra
RUN cargo build --release --bin kinetics-api --bin kinetics-worker

FROM debian:bookworm-slim AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates libpq5 curl && rm -rf /var/lib/apt/lists/*
RUN useradd --system --uid 10001 --create-home kinetics
COPY --from=builder /workspace/rust/kinetics-infra/target/release/kinetics-api /usr/local/bin/kinetics-api
COPY --from=builder /workspace/rust/kinetics-infra/target/release/kinetics-worker /usr/local/bin/kinetics-worker
USER 10001:10001
EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/kinetics-api"]
