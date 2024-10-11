# MIT License

# Copyright (c) 2024 Soumyo Deep Gupta

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
wrapper module for wrapping commands across a progressbar.
"""

from io import TextIOWrapper
from os import getcwd as pwd
from os.path import join as jPath, isdir, expanduser, expandvars
from pathlib import PurePosixPath
from time import sleep
from datetime import datetime
from types import CodeType
from typing import List, Literal, Union
import requests.adapters
from tqdm import tqdm
import progressbar
import subprocess
import sys
import requests

from .Exceptions import *

class Wrapper:
    """Wrapper Class: Wrap commands/scripts across a progress bar.
    
    `Usage:`
    >>> from wrapper_bar.wrapper import Wrapper
    
    >>> wrapControl = Wrapper()
    >>> wrapControl.decoy() # for demonstration.
    
    `Other Functions include:`
    >>> wrapControl.shellWrapper(<params>) # wrap shell commands into a progress bar.
    >>> wrapControl.pyWrapper(<params>) # wrap python scripts into a progress bar.
    >>> wrapControl.pyShellWrapper(<params>) # wrap inline python codes into a progress bar.
    
    `Parameters:`
    # Wrapper class
    >>> wrapControl = Wrapper(label:str (optional), marker:str (optional))
    # decoy function
    >>> wrapControl.decoy(delay:float (optional), width:float (optional))
    # shellWrapper function
    >>> wrapControl.shellWrapper(shellcommands:list[str], label:str = '' (optional),
                                 delay:float (optional),
                                 width:float (optional), timer:str (optional),
                                 logger:bool (optional), logfile:TextIOWrapper (optional),
                                 logfile_auto_close:bool (optional))
    # pyWrapper function
    >>> wrapControl.pyWrapper(pythonscripts:list[str], label:str = '' (optional),
                                delay:float (optional),
                                width:float (optional), timer:str (optional),
                                logger:bool (optional), logfile:TextIOWrapper (optional),
                                logfile_auto_close:bool (optional))
    # pyShellWrapper function
    >>> wrapControl.pyShellWrapper(pythoncodes: list[str], dependencies: list[str] (optional)
                                   label:str = '' (optional),
                                   timer:str = 'ETA' (optional), delay:float (optional),
                                   width:float (optional))
    
    # timer parameter
    default: 'ETA'
    possible values: ['ETA', 'ElapsedTime']
    
    # pyShellWrapper parameters
    pythoncodes -> list of python codes
    dependencies -> list of dependencies. Suppose 'a = b+c' is among the python codes list.
                    Therefore, b and c's value are dependencies and depencies=['b=10', 'c=115'].

    NOTE: Avoid using any print, return or yield statements to avoid breaking the progress bar.
    
    # How to get the value of 'a' from 'a=b+c' after execution?
    >>> a = wrapControl.pyShellWrapperResults['a']
    
    For Beginners, wrapping commands across a given progress bar might seem
    awfully time consuming. This Module is an effort to provide satisfaction to
    your aesthetic needs for your scripts.
    
    Feel free to check out the code and do any modifications you like under the
    MIT License. ;)
    """
    def __init__(self, marker:str = "▓") -> None:
        """Initialize the Wrapper class"""
        self.marker = marker
    
    def decoy(self, label:str = "", delay: float = 0.1, width:float = 50, timer: Literal['ETA', 'ElapsedTime'] = 'ETA') -> None:
        """Create a decoy progress bar, that does nothing at all.
        
        `steps`:
        >>> wrapControl = Wrapper()
        >>> wrapControl.decoy()
        """
        if timer=='ETA':
            widgets = [label+" ", progressbar.Bar(marker=self.marker), progressbar.AdaptiveETA()]
        else:
            widgets = [label+" ", progressbar.Bar(marker=self.marker), progressbar.Timer()]
            
        try:
            bar = progressbar.ProgressBar(widgets=widgets, maxval=100, term_width=width).start()
            
            for i in range(100):
                sleep(delay)
                bar.update(i)
            
            bar.finish()
        except KeyboardInterrupt:
            pass
    
    def shellWrapper(self, shellcommands: List[str], label:str = "", delay: float = 0.1, width:float = 50, timer: Literal['ETA', 'ElapsedTime'] = 'ETA',
                     logger:bool = False, logfile:Union[TextIOWrapper, None] = None, logfile_auto_close:bool = True) -> None:
        """Wrap shell commands with the progressbar.
        
        `steps`:
        >>> wrapControl.shellWrapper(shellcommands:list[str], label:str = '' (optional),
                                    delay:float (optional),
                                    width:float (optional), timer:str (optional),
                                    logger:bool (optional), logfile:TextIOWrapper (optional),
                                    logfile_auto_close:bool (optional))

        `timer` parameter:
        default: 'ETA'
        possible values: ['ETA', 'ElapsedTime']
        """
        if logger:
            if not logfile:
                logfile = open(jPath(pwd(), '.log'), 'w')
        
        if timer=='ETA':
            widgets = [label+" ", progressbar.Bar(marker=self.marker), progressbar.AdaptiveETA()]
        else:
            widgets = [label+" ", progressbar.Bar(marker=self.marker), progressbar.Timer()]
        
        try:
            bar = progressbar.ProgressBar(widgets=widgets, term_width=width, maxval=100).start()
            
            interval = int(100/(len(shellcommands)+1))
            iterator = 0
            
            for i in range(100):
                if i>=interval and (i==interval or i%interval==0) and iterator<len(shellcommands):
                    logfile.write(f"{datetime.today().strftime('%B %d, %Y')} {datetime.now().strftime('%H hours %M minutes %S seconds')}\n")
                    logfile.write(f"Command Executed: \'{shellcommands[iterator]}\'\n")
                    subprocess.Popen(shellcommands[iterator].split(' '), stderr=logfile, stdout=logfile).wait()
                    logfile.write(f'\nEND\n')
                    iterator += 1
                    bar.update(i)
                else:
                    sleep(delay)
                    bar.update(i)
            
            bar.finish()
        except KeyboardInterrupt:
            pass
        
        if logfile_auto_close and logger and logfile:
            logfile.close()
    
    def pyWrapper(self, pythonscripts: List[str], label:str = "", delay: float = 0.1, width: float = 50, timer: Literal['ETA', 'ElapsedTime'] = 'ETA',
                  logger:bool = False, logfile: Union[TextIOWrapper, None] = None, logfile_auto_close:bool = False) -> None:
        """Wrap Python Scripts with the progressbar.
        
        `steps`:
        >>> wrapControl.pyWrapper(pythonscripts:list[str], label:str = '' (optional),
                                delay:float (optional),
                                width:float (optional), timer:str (optional),
                                logger:bool (optional), logfile:TextIOWrapper (optional),
                                logfile_auto_close:bool (optional))
        
        `timer` parameter:
        default: 'ETA'
        possible values: ['ETA', 'ElapsedTime']
        """
        if logger:
            if not logfile:
                logfile = open(jPath(pwd(), '.log'), 'w')
        
        for i in range(len(pythonscripts)):
            pythonscripts[i] = expandvars(expanduser(pythonscripts[i]))
            if pythonscripts[i].startswith('./'):
                pythonscripts[i] = jPath(pwd(), pythonscripts[i][2:]) # strip the './'
        
        if timer=='ETA':
            widgets = [label+" ", progressbar.Bar(marker=self.marker), progressbar.AdaptiveETA()]
        elif timer=='ElapsedTime':
            widgets = [label+" ", progressbar.Bar(marker=self.marker), progressbar.Timer()]
        else:
            widgets = [label+" ", progressbar.Bar(marker=self.marker), progressbar.AdaptiveETA()]
        
        try:
            bar = progressbar.ProgressBar(widgets=widgets, maxval=100, term_width=width).start()
            
            interval = int(100/(len(pythonscripts)+1))
            iterator = 0
            
            for i in range(100):
                if i>=interval and (i==interval or i%interval==0) and iterator<len(pythonscripts):
                    logfile.write(f"{datetime.today().strftime('%B %d, %Y')} {datetime.now().strftime('%H hours %M minutes %S seconds')}\n")
                    logfile.write(f"Python File Executed: \'{pythonscripts[iterator]}\'\n")
                    subprocess.Popen(['python'].extend(pythonscripts[iterator].split(' ')), stderr=logfile).wait()
                    logfile.write(f"\nEND\n")
                    iterator += 1
                    bar.update(i)
                else:
                    sleep(delay)
                    bar.update(i)
            
            bar.finish()
        except KeyboardInterrupt:
            pass
        
        if logfile_auto_close:
            logfile.close()
    
    def __compile(self, codes:list[str]) -> List[CodeType]:
        compiledcodes: List[CodeType] = []
        for code in codes:
            compiledcode = compile(code, '<string>', 'exec')
            compiledcodes.append(compiledcode)
        
        return compiledcodes
    
    def pyShellWrapper(self, pythoncodes: List[str], dependencies:List[str] = [], label:str = "", delay:float = 0.1, width:float = 50,
                       timer:str = 'ETA') -> None:
        """Wrap inline python codes with a progressbar
        
        `steps`:
        >>> wrapControl.pyShellWrapper(pythoncodes: list[str], dependencies: list[str] (optional)
                                   label:str = '' (optional),
                                   timer:str = 'ETA' (optional), delay:float (optional),
                                   width:float (optional))
    
        `timer` parameter:
        default: 'ETA'
        possible values: ['ETA', 'ElapsedTime']
        
        `pyShellWrapper` parameters:
        pythoncodes -> list of python codes
        dependencies -> list of dependencies. Suppose 'a = b+c' is among the python codes list.
                        Therefore, b and c's value are dependencies and depencies=['b=10', 'c=115'].
        """
        
        codes = []
        self.__pyshellresults = {}
        
        variables=""""""
        for c in dependencies:
            variables += c + "\n"
        
        for x in pythoncodes:
            code = variables + x + "\n"
            codes.append(code)
        
        try:
            compiledcodes = self.__compile(codes=codes)
        except KeyboardInterrupt:
            sys.exit(1)

        
        if timer=='ETA':
            widgets = [label+" ", progressbar.Bar(marker=self.marker), progressbar.AdaptiveETA()]
        elif timer=='ElapsedTime':
            widgets = [label+" ", progressbar.Bar(marker=self.marker), progressbar.Timer()]
        else:
            widgets = [label+" ", progressbar.Bar(marker=self.marker), progressbar.AdaptiveETA()]
        
        try:
            bar = progressbar.ProgressBar(widgets=widgets, maxval=100, term_width=width).start()
            
            interval = int(100/(len(pythoncodes)+1))
            iterator = 0
            
            for i in range(100):
                if i>=interval and (i==interval or i%interval==0) and iterator<len(pythoncodes):
                    exec(compiledcodes[iterator], globals(), self.__pyshellresults)
                    iterator += 1
                    bar.update(i)
                else:
                    sleep(delay)
                    bar.update(i)
            
            bar.finish()
        except KeyboardInterrupt:
            pass
    
    @property
    def pyShellWrapperResults(self) -> dict:
        return self.__pyshellresults

    def downloadWrapper(self, link: str, download_to: str, download_filename: Union[str, None] = None, type: Literal['direct', 'github_release'] = 'direct', github_release: str = 'latest', private_repo: bool = False, github_api_token: Union[str, None] = None, label: Union[str, None] = None, width: int = 70, chunk_size: Union[int, None] = 1024) -> None:
        """
        Wrap downloads with a progressbar.

        `steps`:
        >>> wrapControl.downloadWrapper(link: str, download_to: str, download_filename: str | None (optional), type: str (optional), github_release: str (optional), private_repo: bool (optional), github_api_token: str | None (optional), label: str (optional))

        `type` parameter:
        default: 'direct'
        possible_values: ['direct', 'github_release']

        `github_release` parameter by default is set to 'latest'. If other releases are to be used, use the release tag -> v1.0, v2.3.1, and so on.

        `private_repo` parameter is by default False, if downloading from a private repo release, set it to True.

        `github_api_token` parameter needs to be set if `private_repo` parameter is set to True.

        `download_filename` parameter is optional and by default is None. If no filename is provided, it will be derived from the url's basename.
        This might cause problems in some cases, and therefore, if you are not sure, set a `download_filename`.

        `NOTE:`
        - This feature requires an active internet connection. If not found, it will raise an NoConnection Exception.
        - `download_to` must be a folder, if not it will raise NotADirectory Exception.
        - `download_filename` if not provided might raise DownloadFileNameErr if some exception occurs while deriving it from link. NOTE: you need to provide `download_filename` in case of `github_release`.
        - If `type` is not in the defined range, it will raise typeErr.
        - All Exceptions can be imported from `wrapper_bar.Exceptions`.
        - If downloading an asset from github_release, specify the link to your repository in the `link` parameter. Also, If the repository is private, set the `github_api_token` parameter and set `private_repo` parameter to True.
        
        `Disclaimer`: `Wrapper Bar` in no way will tamper with your repository except downloading your assets!
        """

        # resolve download parameters
        # download to
        download_to = expanduser(expandvars(download_to))
        if download_to.startswith('./') or download_to.startswith('.\\'):
            download_to = jPath(pwd(), download_to[2:])

        if not isdir(download_to):
            raise NotADirectory("provided download_to parameter is not a directory.")
        
        # download_filename
        if download_filename == None or download_filename == "":
            try:
                download_filename = PurePosixPath(link).name
            except Exception as e:
                raise DownloadFileNameErr("Error with deriving download_filename from link, Try setting it manually: {}", e)
        
        download_filename_path = jPath(download_to, download_filename)
        
        # type
        if type not in ['direct', 'github_release']:
            raise typeErr("Type is not in the defined range.")

        # if `github_release`, follow these extra steps
        if type == 'github_release':
            # parse link.
            if link.endswith(".git"):
                repo = PurePosixPath(link).name.split(".")[0]
            else:
                repo = PurePosixPath(link).name
            
            username = PurePosixPath(link).parent.name

            # make api_url
            api_url = "https://api.github.com/repos/{}/{}/releases/{}".format(username, repo, github_release)

            if private_repo:
                if github_api_token == None or github_api_token == "":
                    raise GitHubTokenMissing("for private repos, GitHub API Token is required.")
                else:
                    headers = {
                        "Authorization": f"token {github_api_token}",
                    }

                    resp = requests.get(url=api_url, headers=headers)
            else:
                resp = requests.get(api_url)
            
            # raise errors if any
            try:
                resp.raise_for_status()
            except Exception as e:
                raise ConnectionErr("{}", e)
            
            resp = resp.json()

            asset_url = None

            for asset in resp['assets']:
                if asset['name'] == download_filename:
                    asset_url = asset['browser_download_url']
                    break
            
            if not asset_url:
                raise DownloadFileNotFound(f"{download_filename} is not found in there release: {github_release}.")
        
            link = asset_url
        
        # Download
        response = requests.get(url=link, stream=True) if not private_repo else requests.get(url=link, headers=headers, stream=True)
        total_size = int(response.headers.get('content-length', 0))

        with open(download_filename_path, 'wb+') as file_ref, tqdm(
            desc=label if label != None else download_filename,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}', # Remove the right most time and speed
            ncols=width, # width
        ) as bar:
            # for data in chunks of block_size = 1024
            for data in response.iter_content(chunk_size=chunk_size):
                # write data
                file_ref.write(data)
                # update bar
                bar.update(len(data))