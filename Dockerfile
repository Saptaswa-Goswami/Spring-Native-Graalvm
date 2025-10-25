# # Stage 1: Build the native image
# FROM ghcr.io/graalvm/native-image-community:25 AS builder

# # Install build dependencies (Native Image is already included in the BUILDER image)
# RUN microdnf install -y unzip zip findutils

# # Set working directory
# WORKDIR /app

# # Copy Gradle wrapper and build files
# COPY gradlew .
# COPY gradle gradle
# COPY build.gradle.kts settings.gradle.kts ./

# # Copy source code
# COPY src src

# # Build the project and generate native image
# # Disable Gradle daemon for both commands
# RUN ./gradlew --no-daemon build -x test
# RUN ./gradlew --no-daemon nativeCompile


# Stage 1: Build the native image
FROM ghcr.io/graalvm/native-image-community:25 AS builder

# Install build dependencies and clean in one layer
RUN microdnf install -y unzip zip findutils && \
    microdnf clean all

WORKDIR /app

# Layer 1: Gradle wrapper (rarely changes)
COPY gradlew .
COPY gradle gradle

# Layer 2: Build configuration (changes occasionally)
COPY build.gradle.kts settings.gradle.kts ./

# Layer 3: Download dependencies (cached until build files change)
RUN ./gradlew --no-daemon dependencies || true

# Layer 4: Source code (changes frequently)
COPY src src

# Layer 5: Build and native compile in single command
RUN ./gradlew --no-daemon build nativeCompile -x test && \
    strip /app/build/native/nativeCompile/simplecurd || true




# Stage 2: Create runtime image
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y curl ca-certificates && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the native executable from builder stage
COPY --from=builder /app/build/native/nativeCompile/simplecurd /app/simplecurd

# Expose port 8080
EXPOSE 8080

# Run the native executable
CMD ["/app/simplecurd"]