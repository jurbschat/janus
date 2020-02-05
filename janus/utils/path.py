"""
This is part of the janus package.
"""

__author__ = "Jan Meyer"
__email__ = "jan.meyer@desy.de"
__copyright__ = "(c)2019 DESY, FS-BMX, FS-Petra-D, P11"
__license__ = "GPL"


import os
import json
import time
from unidecode import unidecode
from PyQt5.QtCore import QObject
from ..core import Object, pyqtSignal


class Path(Object, QObject):
    """Helper that will create pathes by exchanging keywords in a template
    with real folder names. The returned path is sanatized to consist of ASCII
    characters only, even without special characters other then - and _. As the
    keywords are replaced one after another, having keywords in substituted
    pathes may cause problems. Also features run numbering.
    """
    ROOT_RAMDISK = "ramdisk"
    ROOT_BEAMLINE = "beamline"
    ROOT_CENTRAL = "central"
    DATA_TYPE_RAW = "raw"
    DATA_TYPE_PROCESSED = "processed"
    DATA_TYPE_SCRATCH = "scratch"
    DATA_TYPE_SHARED = "shared"

    value_changed = pyqtSignal(str, name="valueChanged")

    def __init__(self):
        """Construct a new Path instance."""
        QObject.__init__(self)
        Object.__init__(self)
        self.beamtime = ""
        self.user = ""
        self.sample = "default"
        self.number = 1
        self.number_check = ""

    def set_beamtime_dir(self, name):
        """Set the folder name which will replace the beamtime keyword.
        
        :param name: The folder name. Although it should be working, giving 
            subfolders should be avoided.
        :type name: str
        """
        name = self.sanatize(name)
        if name != self.beamtime:
            self.beamtime = name
            self.value_changed.emit("beamtime")
        self.janus.utils["logger"].debug("Path.set_beamtime_dir() " +
                "set to \"" + self.beamtime + "\"")

    def set_user_dir(self, name):
        """Set the folder names which will replace the user keyword.
        
        :param name: The folder names. Giving subfolders is expected and okay.
        :type name: str
        """
        name = self.sanatize(name)
        if name != self.user:
            self.user = name
            self.value_changed.emit("user")
        self.janus.utils["logger"].debug("Path.set_user_dir() " +
                "set to \"" + self.user + "\"")

    def set_sample_dir(self, name):
        """Set the folder name which will replace the sample keyword.
        
        :param name: The folder name. In case of subfolders only the deepest
            layer will be used. Everything preceeding is stripped away.
        :type name: str
        """
        name = self.sanatize(name)
        if os.path.sep in name:
            parts = name.split(os.path.sep)
            name = parts.pop()
        if name != self.sample:
            self.sample = name
            self.value_changed.emit("sample")
        self.janus.utils["logger"].debug("Path.set_sample_dir() " +
                "set to \"" + self.sample + "\"")

    def set_user_and_sample_dir(self, name):
        """Set the folder names which will replace the user and sample keywords.
        
        The last subfolder is set as sample directory, the others will be
        used to set the user directory.
        
        :param name: The folder names. Giving subfolders is expected and okay.
        :type name: str
        """
        name = str(name) #name might be a QString
        parts = name.split(os.path.sep)
        self.set_sample_dir(parts.pop())
        self.set_user_dir(os.path.sep.join(parts))

    def set_run_number(self, number):
        """Set the current run number.
        
        The number is just set, without any tests.
        
        :param number: The new run number.
        :type number: int
        """
        if self.number != number:
            self.number = number
            self.value_changed.emit("number")
        self.janus.utils["logger"].debug("Path.set_run_number() " +
                "set to \"" + str(self.number) + "\"")

    def set_run_number_check(self, template):
        """Set a template to check whether an acq-run has been started.
        
        The template will be compiled by get_path. If the resulting file or 
        folder exists for a specific run numer, it is assumed that an
        acquisition run with this number has been carried out already.
        
        :param template: A pseudo path which keywords will be replaced.
        :type template: str
        """
        number = self.get_run_number()
        if self.number_check != template:
            self.number_check = template
        if number != self.get_run_number():
            self.value_changed.emit("number")
        self.janus.utils["logger"].debug("Path.set_run_number_check() " +
                "set to \"" + self.number_check + "\"")

    def get_path(self, template, force=False, number=None):
        """Create a path by exchanging keywords in the template.

        The following keywords are recognised and will be exchanged against
        real folder names:
            - ramdisk   mount point of a local high speed buffer (/rd)
            - beamline  mount point of a remote filesystem (/gpfs)
            - central   mount point of the central storage (/asap3)
            - beamtime  folder exclusivly meant for a beamtime (current) 
            - raw       subfolder for immutable data of a beamtime
            - processed subfolder for mutable data of a beamtime
            - scratch   subfolder for temporarly needed data
            - shared    subfolder for common files needed with the data
            - user      user defined folder hierarchy
            - sample    identifier for the sample itself
            - number    run number for multiple acq-runs of the same sample
            
        :param template: A pseudo path which keywords will be replaced.
        :type template: str
        :param force: If set, the path will be created if not existing yet.
        :type force: bool
        :param number: Will overload the current run number if set.
        :type number: int
        :return: The created path or None, if force is set and failed.
        :rtype: str or None
        """
        substitutes = {
            "ramdisk": self.ROOT_RAMDISK,
            "beamline": self.ROOT_BEAMLINE,
            "central": self.ROOT_CENTRAL,
            "beamtime": self.beamtime,
            "raw": self.DATA_TYPE_RAW,
            "processed": self.DATA_TYPE_PROCESSED,
            "scratch": self.DATA_TYPE_SCRATCH,
            "shared": self.DATA_TYPE_SHARED,
            "user": self.user,
            "sample": self.sample,
            "number": "{:03d}".format(self.number)
        }
        if type(number) == int:
            substitutes["number"] = "{:03d}".format(number)
        path = str(template) #template might be a QString
        for key, value in substitutes.items():
            path = path.replace(key, value)
        while path.find(os.path.sep + os.path.sep) >= 0:
            path = path.replace(os.path.sep + os.path.sep, os.path.sep)
        if force:
            dirs = path.split(os.path.sep)
            current_dir = ""
            for d in dirs:
                current_dir += os.path.sep + d
                if not os.access(current_dir, os.F_OK):
                    try:
                        os.mkdir(current_dir)
                    except:
                        return None
        return path

    def get_relative_path(self, template1, template2):
        """Return a relative path to point from template2 to template1.
        
        The templates are both compiled using get_path.
        
        :param template1: A pseudo path which keywords will be replaced.
        :type template1: str
        :param template2: A pseudo path which keywords will be replaced.
        :type template2: str
        :return: The created path.
        :rtype: str
        """
        path1 = self.get_path(template1)
        path2 = self.get_path(template2)
        parts1 = path1.split(os.path.sep)
        parts2 = path2.split(os.path.sep)
        same = 0
        while same < len(parts1) and same < len(parts2) and \
                parts1[same] == parts2[same]:
            same += 1
        relative = (len(parts2) - (same + 1)) * (".." + os.path.sep)
        relative += os.path.sep.join(parts1[same:])
        return relative

    def get_filename(self, template="sample_number"):
        """Create a filename by exchanging keywords in the template.
        
        Same as get_path but preceeding folders are stripped away.
        
        :param template: A pseudo path which keywords will be replaced.
        :type template: str
        :return: The created filename.
        :rtype: str
        """
        return self.get_path(template).split(os.path.sep).pop()

    def get_run_number(self, last=False):
        """Returns the first run number which is not found in the filesystem.
        
        Checks whether the path defined through the template set by 
        set_run_number_check exists for numbers from 1 up. The first number
        not found is returned.
        
        :param last: If set, the last number found is returned.
        :type last: bool
        :return: The first number not found or the last number found. 0 if none.
        :rtype: int
        """
        if self.number_check.find("number") < 0:
            if last:
                return 0
            return 1
        last_existing = 0
        for n in range(1, 1000):
            check_path = self.get_path(self.number_check, number=n)
            if os.access(check_path, os.F_OK):
                last_existing = n
            elif not last:
                return n
            else:
                return last_existing
        return 0

    def inc_run_number(self):
        """Set the current run number to the next number not found.
        
        Finds the first non existing run usinf get_run_number and sets the
        current run number accordingly.
        """
        self.set_run_number(self.get_run_number())

    def sanatize(self, name):
        """Return the given name converted to a reduced ASCII set only.
        
        Uses the unidecode module to convert special and non latin characters
        to ASCII only representations. The result will only consist of
        [0-9,A-Z,a-z,-,_].
        
        :param name: The string to be sanatized.
        :type name: str
        """
        sanatized = ""
        allowed = os.path.sep + \
            "0123456789-ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz"
        name = unidecode(str(name))
        name = name.replace(".", "_")
        name = name.replace(" ", "_")
        for c in name:
            if c in allowed:
                sanatized += c
        return sanatized


class P11DataFolders(Object):
    """Helper to check if access to folders on the beamline filesystem is 
    possible and retrieve informations on them.
    """
    PATH_BEAMTIME = "/gpfs/current"
    PATH_COMMISSIONING = "/gpfs/commissioning"
    PATH_FALLBACK = "/gpfs/local"

    def is_beamtime_open(self):
        """Check if beamtime folder is open on the beamline file system.
        
        :return: If /gpfs/current/raw is writeable and existing.
        :rtype: bool
        """
        return os.access(self.PATH_BEAMTIME + "/raw", os.F_OK | os.W_OK)

    def is_commissioning_open(self):
        """Check if commisioning folder is open on the beamline file system.
        
        :return: If /gpfs/commisioning/raw is writeable and existing.
        :rtype: bool
        """
        return os.access(self.PATH_COMMISSIONING + "/raw", os.F_OK | os.W_OK)

    def is_fallback_open(self):
        """Check if local folder is open on the beamline file system.
        
        :return: If /gpfs/local/raw is writeable and existing.
        :rtype: bool
        """
        return os.access(self.PATH_FALLBACK + "/raw", os.F_OK | os.W_OK)

    def beamtime_info(self):
        """Return info on the currently opened beamtime.
        
        :return: Metadata from the DOOR database.
        :rtype: dict
        """
        if not self.is_beamtime_open():
            return None
        file_name = ""
        for entry in os.scandir(self.PATH_BEAMTIME):
            if entry.is_file() and entry.name.startswith("beamtime-metadata"):
                file_name = entry.path
        if not file_name:
            return None
        else:
            return self._info(file_name)

    def commissioning_info(self):
        """Return info on the currently opened commissioning folder.
        
        :return: Metadata like commissioning tag.
        :rtype: dict
        """
        if not self.is_commissioning_open():
            return None
        file_name = ""
        for entry in os.scandir(self.PATH_COMMISSIONING):
            if entry.is_file() and entry.name.startswith("commissioning-metadata"):
                file_name = entry.path
        if not file_name:
            return None
        else:
            return self._info(file_name)

    def _info(self, filename):
        """Helper to retrieve metadata from txt files.
        
        :return: Metadata
        :rtype: dict
        """
        try:
            file_handle = open(filename)
            data = file_handle.read()
            file_handle.read()
        except:
            return None
        start = data.find("{")
        stop = data.rfind("}")
        if start >= 0 and stop >= 0:
            try:
                return json.JSONDecoder().decode(data[start:stop + 1])
            except:
                return None
        return None


class P11Path(Path):
    """Helper that will create pathes by exchanging keywords in a template
    with real folder names. The returned path is sanatized to consist of ASCII
    characters only, even without special characters other then - and _. As the
    keywords are replaced one after another, having keywords in substituted
    pathes may cause problems. Also features run numbering.
    
    In contrast to the inherited Path class, the beamtime keyword is set through
    set_mode() and the resulting path is modified to point to the data in
    the core filesystem if the central keyword is given.
    """
    ROOT_RAMDISK = "rd"
    ROOT_BEAMLINE = "gpfs"
    ROOT_CENTRAL = "asap3/petra3/gpfs/p11"
    DATA_TYPE_RAW = "raw"
    DATA_TYPE_PROCESSED = "processed"
    DATA_TYPE_SCRATCH = "scratch"
    DATA_TYPE_SCRATCH_BL = "scratch_bl"
    DATA_TYPE_SCRATCH_CC = "scratch_cc"
    DATA_TYPE_SHARED = "shared"
    DATA_MODE_BEAMTIME = "current"
    DATA_MODE_BEAMTIME_BL = "current"
    DATA_MODE_BEAMTIME_CC = "data"
    DATA_MODE_COMMISSIONING = "commissioning"
    DATA_MODE_FALLBACK = "local"
    MODE_BEAMTIME = 0
    MODE_COMMISSIONING = 1
    MODE_FALLBACK = 2

    def __init__(self):
        """Construct a new Path instance."""
        Path.__init__(self)
        self.ROOT_CENTRAL += "/" + time.strftime("%Y")
        self.ROOT_CENTRAL = self.ROOT_CENTRAL.replace("/", os.path.sep)
        self.folders = P11DataFolders()
        self.set_mode(self.MODE_BEAMTIME)

    def set_beamtime_dir(self, name):
        """Overload - does nothing. Beamtime keyword is set through set_mode().
        """
        pass

    def set_mode(self, mode):
        """Set whether it is a regular beamtime, commisioning run or fall back.
        
        If set to a mode were the corresponding folder could not be found,
        mode is incremented.

        :param mode: MODE_BEAMTIME=0, MODE_COMMISSIONING=1, MODE_FALLBACK=2.
        :type mode: int
        """
        if mode == self.MODE_BEAMTIME and self.folders.is_beamtime_open():
            self.mode = mode
            Path.set_beamtime_dir(self, self.DATA_MODE_BEAMTIME)
        elif mode == self.MODE_BEAMTIME:
            mode += 1
        if mode == self.MODE_COMMISSIONING and self.folders.is_commissioning_open():
            self.mode = mode
            Path.set_beamtime_dir(self, self.DATA_MODE_COMMISSIONING)
        elif mode == self.MODE_COMMISSIONING:
            mode += 1
        if mode == self.MODE_FALLBACK:
            self.mode = mode
            Path.set_beamtime_dir(self, self.DATA_MODE_FALLBACK)

    def get_path(self, template, force=False, number=None):
        """Create a path by exchanging keywords in the template.

        The following keywords are recognised and will be exchanged against
        real folder names:
            - ramdisk   mount point of a local high speed buffer (/rd)
            - beamline  mount point of a remote filesystem (/gpfs)
            - central   mount point of the central storage (/asap3)
            - beamtime  folder exclusivly meant for a beamtime (current) 
            - raw       subfolder for immutable data of a beamtime
            - processed subfolder for mutable data of a beamtime
            - scratch   subfolder for temporarly needed data
            - shared    subfolder for common files needed with the data
            - user      user defined folder hierarchy
            - sample    identifier for the sample itself
            - number    run number for multiple acq-runs of the same sample
            
        :param template: A pseudo path which keywords will be replaced.
        :type template: str
        :param force: If set, the path will be created if not existing yet.
        :type force: bool
        :param number: Will overload the current run number if set.
        :type number: int
        :return: The created path or None, if force is set and failed.
        :rtype: str or None
        """
        #there is no such thing as a fall back in the central storage
        if -1 < template.find("central") < 2 and self.mode == self.MODE_FALLBACK:
            return None
        path = Path.get_path(self, template, force=force, number=number)
        #the scratch folder name differs between beamline and central storage
        #as well as the beamline folder name itself
        if -1 < template.find("central") < 2:
            path = path.replace(self.DATA_TYPE_SCRATCH, self.DATA_TYPE_SCRATCH_CC)
            info = self.folders.beamtime_info()
            if "beamtimeId" in info:
                path = path.replace(self.DATA_MODE_BEAMTIME, 
                        self.DATA_MODE_BEAMTIME_CC + os.path.sep + info["beamtimeId"])
            elif path.find(self.DATA_MODE_BEAMTIME) > -1:
                return None
        else:
            path = path.replace(self.DATA_TYPE_SCRATCH, self.DATA_TYPE_SCRATCH_BL)
        return path

