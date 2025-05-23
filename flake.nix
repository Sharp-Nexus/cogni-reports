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
        ruff
        virtualenv
      ];

      packages = with pythonPackages; [
        boto3
        pg8000
      ];
    in {
      pythonEnv = python.withPackages (ps: developmentPackages ++ packages);
      pythonLambdaEnv = python.withPackages (ps: packages);
    };

    packages = forEachSupportedSystem({pkgs}: {
      default = pkgs.stdenvNoCC.mkDerivation {
        name = "callsim-reports-lambda";
        src = ./.;

        buildInputs = with pkgs; [rsync zip];

        buildPhase = ''
          mkdir -p lambda
          rsync -av \
            --include='*/' \
            --include='*.py' \
            --exclude='*/tests/' \
            --exclude='*' \
            ${self}/ lambda/

          rsync -av ${pkgs.pythonLambdaEnv}/lib/python3.12/site-packages/ lambda/

          mkdir -p $out/dist
          (cd lambda && zip -r $out/dist/lambda.zip . \
            -x '**/__pycache__/*' '**/*.pyc')
        '';
      };
    });

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
          rsync
        ];
        shellHook = ''
          echo "python --version"
          echo "pip --version"
        '';
      };
    });
  };
}
