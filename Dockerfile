
# Start with a PyTorch base image
FROM pytorch/pytorch:latest

# Install Rust and system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Set the working directory in the container
WORKDIR /usr/src/barnstokkr

# Copy the current directory contents into the container at /usr/src/barnstokkr
COPY . .

# Compile the Rust project
RUN cargo build --release

# Run the binary
CMD ["./target/release/barnstokkr"]

