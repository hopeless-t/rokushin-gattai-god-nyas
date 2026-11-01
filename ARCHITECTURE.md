# Public architecture / 公開アーキテクチャ

Only the public boundary is described here.

```text
opaque parts
    |
    v
  GATTAI
    |
    v
result + receipt
```

At least one production capability is described publicly as a **0B model**.

The names, roles, number, topology, and production composition policy of the internal parts are intentionally outside the public specification.

## Public invariants

1. Parts are opaque at the public boundary.
2. Composition produces a result and a minimal receipt.
3. The public shell must not claim to reproduce production composition.
4. Internal component names and roles are not part of the public API.
