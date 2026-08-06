# Extraction provenance

The Lean modules were extracted from source commit
`0ddbca6505cb2215457896bb2a0817c38b68802d`, which `MANIFEST.json` records as
its `authority_commit`. Modules already supplied by the pinned `finitegeom`
dependency are excluded, so the package has no duplicate Lean module names.

`MANIFEST.json` also seals the non-Lean evidence under `verification/` as
`support_files`, so the axiom audit and the preserved gate log are
content-addressed alongside the sources they describe.

Every module taken from the authority is sealed at the authority's bytes; no
source text was transformed during extraction.

The import-only gate
`RelativeConicArcs.Gates.ClebschRigidityWithOrderElevenCertificates` is the one
module this package owns outright, so it has no authority counterpart. It is
named for what it audits — the rigidity development together with the
order-eleven certificates — rather than sharing a module name with the gate the
pinned dependency publishes, because two packages defining one module name make
that name ambiguous in every consumer.
