{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    systems.url = "github:nix-systems/default";
    devenv.url = "github:cachix/devenv";
  };

  outputs = { self, nixpkgs, devenv, systems, ... } @ inputs:
    let
      forEachSystem = nixpkgs.lib.genAttrs (import systems);
    in
    {
      devShells = forEachSystem
        (system:
          let
            pkgs = nixpkgs.legacyPackages.${system};
          in
          {
            db = devenv.lib.mkShell {
              inherit inputs pkgs;
              modules = [
                {
                    services.mysql = {
                      enable = true;
                      package = pkgs.mariadb;
                      initialDatabases = [{ name = "slashcox"; }];
                      ensureUsers =[
                        {
                            name = "slashcox";
                            password = "YES";
                            ensurePermissions = {
                                "slashcox.*" = "ALL PRIVILEGES"; 
                            };
                        }
                      ];
                      settings = {
                            mysqld = {
                                max_allowed_packet = "256M";
                                log_warnings = "1";
                        };
                    };
                  };
                  enterShell = ''
                    devenv up
                  '';
                }
              ];
            };
            dev = devenv.lib.mkShell {
              inherit inputs pkgs;
              modules = [
                {
                  # https://devenv.sh/reference/options/
                  packages = with pkgs; [ 
                    git
                    python3Full
                    poetry
                    gnumake
                  ];
                  enterShell = ''
                       make init
                       clear
                       echo "Slashcox Development Environment"
                       echo "Python packages in environment: "
                       poetry show
                       make run
                  '';
                }
              ];
            };
        });
    };
}
