{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
    packages = with pkgs; [
        python312Full
        virtualenv
        python311Packages.pip
        # nodePackages.pyright
        # ruff-lsp
    ];

    # shellHook = ''
    # '';
}
