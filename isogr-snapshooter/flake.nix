{
  description = "Scraper for geodetic.isotc211.org";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    devshell.url = "github:numtide/devshell/main";
    flake-compat = {
      url = "github:edolstra/flake-compat";
      flake = false;
    };
  };
  outputs =
    { self
    , nixpkgs
    , flake-utils
    , devshell
    , flake-compat
    , ...
    }:
    flake-utils.lib.eachDefaultSystem (system:
    let
      cwd = builtins.toString ./.;
      overlays = map (x: x.overlays.default) [
        devshell
      ];
      pkgs = import nixpkgs { inherit system overlays; };
      python = pkgs.python311.withPackages (pkgs: with pkgs; [
        # beautifulsoup4
        # mypy
        # pylsp-mypy
        # python-lsp-ruff
        # requests
        # ruff-lsp
        # types-beautifulsoup4
        # types-requests
        # typing-extensions
      ]);
    in
    rec {

      # nix develop
      devShell = pkgs.devshell.mkShell {
        env = [
        ];
        commands = [
          {
            name = "serve";
            command = "scripts/serve \"$@\"";
            help = "Serve the site";
            category = "Scraper";
          }
          {
            name = "scrape";
            command = "scripts/scrape \"$@\"";
            help = "Scrape the site's HTML, JSON, static assets, etc.";
            category = "Scraper";
          }
          {
            name = "deploy-patch";
            command = "scripts/deploy-patch \"$@\"";
            help = "Patch base paths for all links before deployment";
            category = "Scraper";
          }
        ];
        packages = with pkgs; [
          bash
          curl
          fd
          fzf
          gnused
          jq
          ripgrep
          wget
        ] ++ [
          python
        ];
      };
    });
}
