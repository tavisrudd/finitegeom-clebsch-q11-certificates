# Extraction provenance

The Lean modules were extracted from source commit
`10d1941a3683d100548436a77d030a69d61347a0`. Modules already supplied by the
pinned `finitegeom` dependency are excluded, so the package has no duplicate
Lean module names.

The only source-text transformation corrects the pinpoint citation in
`RelativeConicArcs.Q11DyeAxioms` and the import-only gate: the ten-point bound
is in Section 2.2, page 275, and the equality classification is Theorem 1(ii)
on the same page. The axiom declarations and theorem statements are unchanged.
