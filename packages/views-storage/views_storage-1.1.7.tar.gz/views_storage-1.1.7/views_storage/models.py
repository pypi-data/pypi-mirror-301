from typing import List
#from pydantic import BaseModel

class Listing():
    """
    A directory listing, separating folders and files.
    """

    folders: List[str]
    files: List[str]
