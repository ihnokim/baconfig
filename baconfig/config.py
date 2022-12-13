import os
from typing import Optional, Union, Dict, Any
from copy import deepcopy
from .priority import Priority


BACONFIG_PREFIX = "BACONFIG"
BACONFIG_NAME = f"{BACONFIG_PREFIX}_NAME"
BACONFIG_FILEPATH = f"{BACONFIG_PREFIX}_FILEPATH"


class Config:
  class Metadata:
    def __init__(self) -> None:
      self.name: str = BACONFIG_PREFIX
      self.priority: Priority = Priority.ENVVAR
      self.filepath: Optional[str] = None
    
    def to_dict(self) -> Dict:
      return {"name": self.name, "priority": self.priority, "filepath": self.filepath}
  
  _metadata: Metadata = Metadata()
  _config: Dict[str, Dict[str, Any]] = dict()

  @classmethod
  def __init__(cls, *,
               name: str = os.environ.get(BACONFIG_NAME, BACONFIG_PREFIX).upper(),
               priority: Priority = Priority.ENVVAR,
               filepath: Optional[str] = os.environ.get(BACONFIG_FILEPATH, None),
              ) -> None:
    cls.set_name(name=name)
    cls.set_priority(priority=priority)
    cls.set_filepath(filepath=filepath)
    cls.reload()

  @classmethod
  def reload(cls) -> None:
    pass

  @classmethod
  def describe(cls) -> Dict:
    return cls._metadata.to_dict()

  @classmethod
  def set_filepath(cls, filepath: Optional[str] = None) -> None:
    if filepath and not os.path.isfile(filepath):
      raise FileNotFoundError(f"[Errno 2] No such file or directory: '{filepath}'")
    cls._metadata.filepath = filepath
  
  @classmethod
  def get_filepath(cls) -> Optional[str]:
    return cls._metadata.filepath

  @classmethod
  def set_name(cls, name: str) -> None:
    cls._metadata.name = name.upper()

  @classmethod
  def get_name(cls) -> str:
    return cls._metadata.name

  @classmethod
  def set_priority(cls, priority: Priority = Priority.ENVVAR) -> None:
    cls._metadata.priority = priority
    
  @classmethod
  def set_value(cls, section: str, key: str, value: Any) -> None:
    if section not in cls._config:
      cls._config[section] = dict()
    cls._config[section][key] = value
  
  @classmethod
  def unset_value(cls, section: str, key: str) -> None:
    if section in cls._config:
      cls._config[section].pop(key, None)
      if len(cls._config[section]) == 0:
        cls._config.pop(section, None)

  @classmethod
  def get(
          cls,
          section: Optional[str] = None,
          key: Optional[str] = None,
         ) -> Optional[Union[Dict, Any]]:
    if section:
      if section in cls._config:
        if key:
          return cls._config[section].get(key, None)
        else:
          return deepcopy(cls._config[section])
      else:
        return None if key else dict()
    else: 
      return deepcopy(cls._config)


_ = Config()
