{
  description = "Fast Task Manager development environment";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python313;
        pythonPackages = python.pkgs;
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python313
            python313Packages.pip
            python313Packages.virtualenv
          ];

          shellHook = ''
            export PYTHONPATH="$PWD/src:$PYTHONPATH"
            
            # Create a virtual environment if it doesn't exist
            if [ ! -d .venv ]; then
              ${python}/bin/python -m venv .venv
            fi
            
            # Activate the virtual environment
            source .venv/bin/activate
            
            # Install dependencies
            pip install -q -e .
            
            echo "✅ Fast Task Manager development shell ready"
            echo "Run the API: uvicorn fast_task_manager.main:app --port 8000"
            echo "Run the GUI: python -c 'from fast_task_manager.gui import run_gui; run_gui()'"
          '';
        };

        packages.default = python.pkgs.buildPythonPackage {
          pname = "fast-task-manager";
          version = "0.1.0";
          src = ./.;
          propagatedBuildInputs = with python.pkgs; [
            fastapi
            uvicorn
            sqlalchemy
            pydantic
            nicegui
            httpx
          ];
        };
      }
    );
}
