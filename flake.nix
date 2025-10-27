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
            export QT_QPA_PLATFORM_PLUGIN_PATH="${pkgs.qt5.qtbase.bin}/lib/qt-${pkgs.qt5.qtbase.version}/plugins"
            export QT_PLUGIN_PATH="${pkgs.qt5.qtbase.bin}/lib/qt-${pkgs.qt5.qtbase.version}/plugins"
          '';

          buildInputs = with pkgs; [
            qt5.qtbase
            qt5.qtx11extras
            xorg.libX11
            xorg.libxcb
            (python3.withPackages (ps: with ps; [
              pyscard
              pyqt5
              pyqtgraph
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