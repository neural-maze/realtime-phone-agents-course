"""Avatar registry and management functions."""

from pathlib import Path
from typing import Dict, List, Optional
from realtime_phone_agents.avatars.base import Avatar


class AvatarRegistry:
    """
    Central registry for managing avatars.
    
    Automatically discovers and loads avatar definitions from YAML files.
    """
    
    def __init__(self, definitions_dir: Optional[Path] = None):
        """
        Initialize the avatar registry.
        
        Args:
            definitions_dir: Directory containing avatar YAML definitions.
                           If None, uses the default definitions directory.
        """
        self._avatars: Dict[str, Avatar] = {}
        
        if definitions_dir is None:
            definitions_dir = Path(__file__).parent / "definitions"
        
        self.definitions_dir = definitions_dir
        self._load_avatars()
    
    def _load_avatars(self):
        """Load all avatar definitions from YAML files in the definitions directory."""
        if not self.definitions_dir.exists():
            raise FileNotFoundError(
                f"Avatar definitions directory not found: {self.definitions_dir}"
            )
        
        # Load all YAML files in the definitions directory
        yaml_files = list(self.definitions_dir.glob("*.yaml")) + list(self.definitions_dir.glob("*.yml"))
        
        if not yaml_files:
            raise ValueError(
                f"No avatar definition files found in {self.definitions_dir}"
            )
        
        for yaml_file in yaml_files:
            try:
                avatar = Avatar.from_yaml(yaml_file)
                self.register(avatar)
            except Exception as e:
                raise ValueError(f"Failed to load avatar from {yaml_file}: {e}") from e
    
    def register(self, avatar: Avatar) -> None:
        """
        Register a new avatar.
        
        Args:
            avatar: Avatar instance to register
        """
        self._avatars[avatar.id] = avatar
    
    def get(self, avatar_id: str) -> Avatar:
        """
        Get an avatar by ID.
        
        Args:
            avatar_id: ID of the avatar (case-insensitive)
            
        Returns:
            Avatar instance
            
        Raises:
            ValueError: If avatar is not found
        """
        avatar_id_lower = avatar_id.lower()
        if avatar_id_lower not in self._avatars:
            available = ", ".join(self._avatars.keys())
            raise ValueError(
                f"Avatar '{avatar_id}' not found. Available avatars: {available}"
            )
        return self._avatars[avatar_id_lower]
    
    def list_all(self) -> Dict[str, str]:
        """
        List all available avatars with their descriptions.
        
        Returns:
            Dictionary mapping avatar IDs to their descriptions
        """
        return {
            avatar_id: avatar.description 
            for avatar_id, avatar in self._avatars.items()
        }
    
    def get_all(self) -> List[Avatar]:
        """
        Get all registered avatars.
        
        Returns:
            List of all Avatar instances
        """
        return list(self._avatars.values())
    
    @property
    def available_ids(self) -> List[str]:
        """Get list of all available avatar IDs."""
        return list(self._avatars.keys())


# Global registry instance
_registry = AvatarRegistry()


def get_avatar(avatar_id: str) -> Avatar:
    """
    Get an avatar by ID.
    
    Args:
        avatar_id: ID of the avatar (case-insensitive)
        
    Returns:
        Avatar instance
        
    Raises:
        ValueError: If avatar is not found
    """
    return _registry.get(avatar_id)


def list_avatars() -> Dict[str, str]:
    """
    List all available avatars with their descriptions.
    
    Returns:
        Dictionary mapping avatar IDs to their descriptions
    """
    return _registry.list_all()


def get_all_avatars() -> List[Avatar]:
    """
    Get all registered avatars.
    
    Returns:
        List of all Avatar instances
    """
    return _registry.get_all()


def register_avatar(avatar: Avatar) -> None:
    """
    Register a custom avatar.
    
    Args:
        avatar: Avatar instance to register
    """
    _registry.register(avatar)


def register_all_avatars() -> None:
    """Register all avatars from the definitions directory."""
    registry = AvatarRegistry()
    for avatar in registry.get_all():
        register_avatar(avatar)

def version_all_avatars() -> None:
    """Version all avatars from the definitions directory."""
    registry = AvatarRegistry()
    for avatar in registry.get_all():
        avatar.version_system_prompt()
