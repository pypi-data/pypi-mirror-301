
#!/usr/bin/env python3
__package__ = "pydantic_pkgr"

import os
import sys
import platform
from typing import Optional
from pathlib import Path

from pydantic import model_validator, TypeAdapter, computed_field

from .base_types import BinProviderName, PATHStr, BinName, InstallArgs, HostBinPath, bin_abspath
from .semver import SemVer
from .binprovider import BinProvider

OS = platform.system().lower()

NEW_MACOS_DIR = Path('/opt/homebrew/bin')
OLD_MACOS_DIR = Path('/usr/local/bin')
DEFAULT_MACOS_DIR = NEW_MACOS_DIR if platform.machine() == 'arm64' else OLD_MACOS_DIR
DEFAULT_LINUX_DIR = Path('/home/linuxbrew/.linuxbrew/bin')


class BrewProvider(BinProvider):
    name: BinProviderName = "brew"
    INSTALLER_BIN: BinName = "brew"
    
    PATH: PATHStr = f"{DEFAULT_LINUX_DIR}:{NEW_MACOS_DIR}:{OLD_MACOS_DIR}"

    @model_validator(mode="after")
    def load_PATH(self):
        if not self.INSTALLER_BIN_ABSPATH:
            # brew is not availabe on this host
            self.PATH: PATHStr = ""
            return self

        PATHs = set()
        
        if OS == 'darwin' and os.path.isdir(DEFAULT_MACOS_DIR) and os.access(DEFAULT_MACOS_DIR, os.R_OK):
            PATHs.add(str(DEFAULT_MACOS_DIR))
        if OS != 'darwin' and os.path.isdir(DEFAULT_LINUX_DIR) and os.access(DEFAULT_LINUX_DIR, os.R_OK):
            PATHs.add(str(DEFAULT_LINUX_DIR))
        
        if not PATHs:
            # if we cant autodetect the paths, run brew --prefix to get the path manually (very slow)
            PATHs.add(self.exec(bin_name=self.INSTALLER_BIN_ABSPATH, cmd=["--prefix"]).stdout.strip() + "/bin")
        
        self.PATH = TypeAdapter(PATHStr).validate_python(':'.join(PATHs))
        return self

    def default_install_handler(self, bin_name: str, packages: Optional[InstallArgs] = None, **context) -> str:
        packages = packages or self.get_packages(bin_name)

        if not self.INSTALLER_BIN_ABSPATH:
            raise Exception(f"{self.__class__.__name__}.INSTALLER_BIN is not available on this host: {self.INSTALLER_BIN}")

        # print(f'[*] {self.__class__.__name__}: Installing {bin_name}: {self.INSTALLER_BIN_ABSPATH} install {packages}')

        # Attempt 1: Try installing with Pyinfra
        from .binprovider_pyinfra import PYINFRA_INSTALLED, pyinfra_package_install

        if PYINFRA_INSTALLED:
            return pyinfra_package_install((bin_name,), installer_module="operations.brew.packages")

        # Attempt 2: Try installing with Ansible
        from .binprovider_ansible import ANSIBLE_INSTALLED, ansible_package_install

        if ANSIBLE_INSTALLED:
            return ansible_package_install(bin_name, installer_module="community.general.homebrew")

        # Attempt 3: Fallback to installing manually by calling brew in shell
        self.exec(bin_name=self.INSTALLER_BIN_ABSPATH, cmd=["update"])
        proc = self.exec(bin_name=self.INSTALLER_BIN_ABSPATH, cmd=["install", *packages])
        if proc.returncode != 0:
            print(proc.stdout.strip())
            print(proc.stderr.strip())
            raise Exception(f"{self.__class__.__name__} install got returncode {proc.returncode} while installing {packages}: {packages}")

        return proc.stderr.strip() + "\n" + proc.stdout.strip()

    def default_abspath_handler(self, bin_name: BinName | HostBinPath, **context) -> HostBinPath | None:
        # print(f'[*] {self.__class__.__name__}: Getting abspath for {bin_name}...')

        if not self.PATH:
            return None
        
        # not all brew-installed binaries are symlinked into the default bin dir (e.g. curl)
        # because it might conflict with a system binary of the same name (e.g. /usr/bin/curl)
        # so we need to check for the binary in the namespaced opt dir as well
        extra_path = self.PATH.replace('/bin', '/opt/{bin_name}/bin')     # e.g. /opt/homebrew/opt/curl/bin/curl
        
        abspath = bin_abspath(bin_name, PATH=f'{self.PATH}:{extra_path}')
        if abspath:
            return abspath
        
        if not self.INSTALLER_BIN_ABSPATH:
            return None
        
        # fallback to using brew info to get the Cellar bin path
        for package in (self.get_packages(str(bin_name)) or [str(bin_name)]):
            try:
                info_lines = self.exec(bin_name=self.INSTALLER_BIN_ABSPATH, cmd=['info', '--quiet', package], timeout=self._version_timeout, quiet=True).stdout.strip().split('\n')
                # /opt/homebrew/Cellar/curl/8.10.0 (530 files, 4MB)
                cellar_path = [line for line in info_lines if '/Cellar/' in line][0].rsplit(' (', 1)[0]
                abspath = bin_abspath(bin_name, PATH=f'{cellar_path}/bin')
                if abspath:
                    return abspath
            except Exception:
                pass
        return None
        

    def default_version_handler(self, bin_name: BinName, abspath: Optional[HostBinPath]=None, **context) -> SemVer | None:
        # print(f'[*] {self.__class__.__name__}: Getting version for {bin_name}...')
        try:
            version =  self.get_version(bin_name, abspath=abspath, **context)
            if version:
                return version
        except ValueError:
            pass
        
        if not self.INSTALLER_BIN_ABSPATH:
            return None
        
        # fallback to using brew info to get the version
        packages = self.get_packages(str(bin_name)) or [str(bin_name)]
        main_package = packages[0]   # assume first package in list is the main one
        try:
            version_str = self.exec(bin_name=self.INSTALLER_BIN_ABSPATH, cmd=['info', '--quiet', main_package], quiet=True, timeout=self._version_timeout).stdout.strip()
            return SemVer.parse(version_str)
        except Exception:
            return None

if __name__ == "__main__":
    # Usage:
    # ./binprovider_brew.py load yt-dlp
    # ./binprovider_brew.py install pip
    # ./binprovider_brew.py get_version pip
    # ./binprovider_brew.py get_abspath pip
    result = brew = BrewProvider()

    if len(sys.argv) > 1:
        result = func = getattr(brew, sys.argv[1])  # e.g. install

    if len(sys.argv) > 2:
        result = func(sys.argv[2])  # e.g. install ffmpeg

    print(result)
