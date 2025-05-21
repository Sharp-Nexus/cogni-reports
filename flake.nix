{
  inputs.nixpkgs.url = "https://flakehub.com/f/NixOS/nixpkgs/0.2411.716632";

  outputs = {
    self,
    nixpkgs,
  }: let
    supportedSystems = ["x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin"];
    forEachSupportedSystem = f:
      nixpkgs.lib.genAttrs supportedSystems (system:
        f {
          pkgs = import nixpkgs {
            inherit system;
            overlays = [self.overlays.default];
          };
        });
  in {
    overlays.default = final: prev: let
      python = final.python312;
      pythonPackages = python.pkgs;

      developmentPackages = with pythonPackages; [
        pip
        virtualenv
      ];

      packages = with pythonPackages; [
        boto3
      ];
    in {
      pythonEnv = python.withPackages (ps: developmentPackages ++ packages);
      pythonLambdaEnv = python.withPackages (ps: packages);
    };

    devShells = forEachSupportedSystem ({pkgs}: {
      default = pkgs.mkShell {
        buildInputs = with pkgs; [
          aws-sam-cli
          awscli2
          direnv
          git
          nix-direnv
          pythonEnv
          python312Packages.python-lsp-server
          zip
          unzip
        ];
        shellHook = ''
          echo "python --version"
          echo "pip --version"
        '';
      };
    });
  };
}
