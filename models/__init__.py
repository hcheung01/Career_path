from models.base_model import BaseModel
from models.skill import Skill
from models.profile import Profile
from models.job import Job
from models.user import User
from models.job_db import Job_db

"""CNC - dictionary = { Class Name (string) : Class Type }"""

from models.engine import db_storage
CNC = db_storage.DBStorage.CNC
storage = db_storage.DBStorage()
storage.reload()
