# finitegeom-clebsch-q11-certificates

Generated and finite-checking Lean 4 modules for the order-11 portion of the
Clebsch rigidity formalization. This repository is a downstream companion to
[`finitegeom`](https://github.com/tavisrudd/finitegeom), pinned at commit
`85dfde9e13e6c3d004e0e659fb83c1a4761902d0`.

The package contains 121 Lean modules not supplied by the pinned dependency.
They encode and check the order-sixty action, its point orbits, the code–arc
dictionary, exact decoder tables, and the order-11 rigidity consequences.
Human-scale chord-defect, small-field, and eight-packet orientation arguments
remain in `finitegeom`.  The final commutant theorems use the explicit
classical conjugate `3+3'` Schur--Galois interface recorded by the Paper I
trust manifest; golden equivariance and integral descent are kernel checked.

The import-only boundary is
`RelativeConicArcs.Gates.ClebschRigidityTrust`. Its rigidity conclusion uses
the ten-point Brianchon bound and equality classification from R. H. Dye,
“Hexagons, conics, A5 and PSL2(K),” *Journal of the London Mathematical
Society* (2) 44 (1991), Section 2.2 and Theorem 1(ii), page 275,
<https://doi.org/10.1112/jlms/s2-44.2.270>.
`MANIFEST.json` content-addresses every Lean module and the generator.

## Build

```sh
nix develop
lake update
lake exe cache get
lake build ClebschQ11Certificates
```

The pinned `finitegeom` commit must be available from its public Git remote.
The aggregate Paper I gate is
`RelativeConicArcs.Gates.ClebschRigidityTrust`.  Its target diagnostics are
recorded in
`verification/clebsch_rigidity_trust/axiom-audit.txt`; the audit includes the
`#print axioms` result for every paper-facing terminal imported by the gate.

## Verify generated orbit data

```sh
python3 scripts/generate-q11-a5-point-action.py --check
```

The expected output is:

```text
verified groups 5--59 after exact groups 0--4 cross-check
```

The generator has SHA-256
`a387e80997c5dacdc50787243a91734663a0f49015fe3ac5c19c2a4d1fefb330`.

## License

Apache License 2.0; see `LICENSE`.
