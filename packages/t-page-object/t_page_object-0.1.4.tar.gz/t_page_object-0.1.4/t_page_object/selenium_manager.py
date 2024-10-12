"""Create a singleton manager to ensure a single instance of Selenium."""
import inspect
from typing import Optional

from RPA.Browser.Selenium import Selenium


class SeleniumManager:
    """Singleton manager to ensure a single instance of Selenium."""

    _portal_instances = {}

    @classmethod
    def get_instance(cls: Selenium) -> Selenium:
        """Get the instance of Selenium for the calling file. If it does not exist, create it."""
        caller_file = cls._find_caller_file()
        if not caller_file:
            raise ValueError("No valid portal found in the stack.")

        if caller_file not in cls._portal_instances:
            cls._portal_instances[caller_file] = Selenium()
        return cls._portal_instances[caller_file]

    @staticmethod
    def _find_caller_file() -> Optional[str]:
        """Find the calling file's name based on specific criteria."""
        stack = inspect.stack()
        for frame_info in stack:
            file = inspect.getfile(frame_info.frame)
            if file:
                file_name = file.split("/")[-1].split(".")[0]
                # Check if the file name starts with 't_' and is not 't_page_object'
                if file_name.startswith("t_") and file_name != "t_page_object":
                    return file_name
        return None
