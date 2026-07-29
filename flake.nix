{
  description = "FiniteGeom Clebsch Q11 certificates — generated Lean 4 certificate package";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { nixpkgs, ... }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "aarch64-darwin"
      ];
      forAllSystems = nixpkgs.lib.genAttrs systems;
    in {
      devShells = forAllSystems (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          commonPackages = with pkgs; [ elan git curl cacert gmp zlib coreutils ];
          defaultShell = pkgs.mkShell ({
            packages = commonPackages;

            shellHook = ''
              export SSL_CERT_FILE="${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
              export CURL_CA_BUNDLE="$SSL_CERT_FILE"
              export GIT_SSL_CAINFO="$SSL_CERT_FILE"
            '';
          } // pkgs.lib.optionalAttrs pkgs.stdenv.isLinux {
            NIX_LD = pkgs.stdenv.cc.bintools.dynamicLinker;
            NIX_LD_LIBRARY_PATH =
              pkgs.lib.makeLibraryPath (with pkgs; [ stdenv.cc.cc.lib gmp zlib glibc ]);
          });
        in {
          default = defaultShell;
        } // pkgs.lib.optionalAttrs pkgs.stdenv.isLinux {
          fhs = (pkgs.buildFHSEnv {
            name = "finitegeom-clebsch-q11-certificates-lean-fhs";
            targetPkgs = p: with p; [ elan git curl cacert gmp zlib gcc coreutils ];
            profile = ''
              export SSL_CERT_FILE="${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
            '';
            runScript = "bash";
          }).env;
        });
    };
}
