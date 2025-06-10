{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      pkgs = import nixpkgs {
        system = "x86_64-linux";
      };
    in
    {
      devShell.x86_64-linux =
        pkgs.mkShell {
          shellHook = ''
          '';

          buildInputs = with pkgs; [
            (python3.withPackages (ps: with ps; [
              pyscard
              (buildPythonPackage rec {
                pname = "ber-tlv";
                version = "0.0.6";

                src = fetchPypi {
                  inherit pname version;
                  sha256 = "sha256-gKvA98qibKn02jwY20k2uuvjOu6cbsrui3GNXdJBSQI=";
                };

                pyproject = true;

                doCheck = true;

                propagatedBuildInputs = [
                  setuptools
                ];
              })
            ]))
          ];
        };
    };
}