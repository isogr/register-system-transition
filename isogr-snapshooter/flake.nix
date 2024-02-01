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
        ];
        packages = with pkgs; [
          bash
          curl
          darkhttpd
          fd
          fzf
          gnused
          jq
          ripgrep
          wget
        ];
      };
    });
}
