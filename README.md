# finitegeom-clebsch-q11-certificates

Generated and finite-checking Lean 4 modules for the order-11 portion of the
Clebsch rigidity formalization. This repository depends one way on
[`finitegeom`](https://github.com/tavisrudd/finitegeom), pinned at commit
`575cf3e991168fb96eb24c318263c5d0552aa531`.

The package contains the Lean modules not supplied by the pinned dependency.
They encode and check the order-sixty action, its point orbits, the code–arc
dictionary, exact decoder tables, and the order-11 rigidity consequences.
Human-scale chord-defect, small-field, rigidity-spine and eight-packet
orientation arguments remain in `finitegeom`.  The final commutant theorems
are conditional on a proposition-valued statement of the classical conjugate
`3+3'` Schur--Galois splitting, which the gate prints; golden equivariance and
integral descent are kernel checked.

The import-only boundary is
`RelativeConicArcs.Gates.ClebschRigidityWithOrderElevenCertificates`, which
covers the rigidity development together with the order-eleven certificates
that instantiate it.  Nothing in the rigidity chain is assumed from the
literature: the ten-point Brianchon bound and the equality classification are
theorems of the pinned dependency.  They formalize results of R. H. Dye,
“Hexagons, conics, A5 and PSL2(K),” *Journal of the London Mathematical
Society* (2) 44 (1991), Theorems 1 and 3, pages 275–278,
<https://doi.org/10.1112/jlms/s2-44.2.270>, which is where the classical
statements appear.
`MANIFEST.json` content-addresses every Lean module and the generator.

## Build

```sh
nix develop
lake update
lake exe cache get
lake build ClebschQ11Certificates
```

The pinned `finitegeom` commit must be available from its public Git remote.
Building `RelativeConicArcs.Gates.ClebschRigidityWithOrderElevenCertificates`
records its target diagnostics in
`verification/clebsch_rigidity_trust/axiom-audit.txt`; the audit gives the
`#print axioms` result for every terminal the gate imports, both those this
package proves and those it takes from the pinned dependency.

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
