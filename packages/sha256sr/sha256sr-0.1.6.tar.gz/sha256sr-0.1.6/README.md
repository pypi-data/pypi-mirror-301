# Overview
The implementation of secure random generator based on SHA256.
# Build
```
sh build.sh
```
# Use Guide
```
from sha256sr.secure_random import SecureRandom
seed = "this is an example of secure random generator based on sha256"
sr = SecureRandom(seed.encode())
gaussian = sr.next_gaussian()
rand_d = sr.next_float64()
```