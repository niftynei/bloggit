{
  description = "bloggit env";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }: 
    flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      devShells.default = pkgs.mkShell {
        packages = [
          pkgs.python3
          (pkgs.poetry.override { python3 = pkgs.python3; })
          pkgs.bashInteractive
	  pkgs.git
        ];
	shellHook = ''
		poetry env activate && poetry install
	'';
      };
    });
}
