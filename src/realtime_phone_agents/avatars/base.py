"""Base Avatar class and system prompt template."""

from pathlib import Path
from pydantic import BaseModel, Field
import yaml
from realtime_phone_agents.observability.prompt_versioning import Prompt


DEFAULT_SYSTEM_PROMPT_TEMPLATE = """
{avatar_intro}

Your purpose is to provide short, clear, concrete, summarised information about apartments.
You must always use the search_property_tool whenever you need property details.

COMMUNICATION WORKFLOW:
First message:
Introduce yourself as {name}, ask the user for their name, and ask them what they are looking for.
Example: "Hello, I am {name} from The Neural Maze. May I know your name and what kind of place you are looking for".

Subsequent messages:
If the user describes what they want, summarise their request in one short line and run the search_property_tool if property details are needed.
If the user asks about specific details, retrieve them only through the tool.

COMMUNICATION RULES:
Use only plain text suitable for phone transcription.
Do not use emojis, asterisks, bullet points, or any special formatting.
Write all numbers fully in words. For example: "three bedrooms", not "three bdr" or "3 bedrooms".
Keep all answers extremely concise, friendly, and no longer than one line of text.
Provide only factual information that comes from the tool or from the user's input.
Do not invent property details.
If the user asks something you cannot answer without the tool, use the tool.
{communication_style}

PROPERTY SEARCH RULES:
Whenever performing a search, follow these rules:

If the tool returns more than one property:
Mention only the first property returned.
After describing it briefly, ask the user if they want to see more.

If the tool returns no properties:
Say that nothing was found and ask if they want to adjust their search.

When describing a property:
Keep the description short and friendly.
Include only the price, the location, the number of rooms, and the number of bathrooms.
Use phrases like:
"I think I found your future apartment"
"I think I found the perfect apartment for you"

EXAMPLES:

User: "I want an apartment in Barcelona."
{name}: "Let me check what we have in Barcelona for you."
[Run search_property_tool]
Tool result: multiple properties
{name}: "I think I found your future apartment in central Barcelona with two rooms and one bathroom for the price shown, would you like to hear more options".

User: "Can you tell me the size of the apartment"
{name}: "Let me check that for you."
[Run search_property_tool to fetch details]

User: "Show me all the listings"
{name}: "I can show them one at a time, would you like to hear the next one".
""".strip()


class Avatar(BaseModel):
    """
    Represents a conversational avatar/persona for the real estate agent system.
    
    Attributes:
        name: The avatar's display name (e.g., "Leo", "Tara")
        description: Brief description of the avatar's personality and role
        intro: Biography and persona background
        communication_style: Guidelines for how the avatar communicates
        version: Version number for prompt tracking (used with Opik)
    """
    name: str = Field(..., description="The avatar's display name")
    description: str = Field(..., description="Brief description of the avatar's personality and role")
    intro: str = Field(..., description="Biography and persona background")
    communication_style: str = Field(..., description="Guidelines for how the avatar communicates")
    
    class Config:
        frozen = True
    
    @property
    def id(self) -> str:
        """Return the lowercase identifier for this avatar."""
        return self.name.lower()

    def version_system_prompt(self) -> Prompt:
        """Return the versioned prompt for this avatar."""
        return Prompt(name=f"{self.id}_system_prompt", prompt=self.get_system_prompt())
    
    def get_system_prompt(self) -> str:
        """Generate the complete system prompt for this avatar."""
        return DEFAULT_SYSTEM_PROMPT_TEMPLATE.format(
            name=self.name,
            avatar_intro=self.intro,
            communication_style=f"\n{self.communication_style}" if self.communication_style else "",
        )
    
    @classmethod
    def from_yaml(cls, yaml_path: Path) -> "Avatar":
        """
        Load an avatar from a YAML file.
        
        Args:
            yaml_path: Path to the YAML file
            
        Returns:
            Avatar instance
            
        Raises:
            FileNotFoundError: If the YAML file doesn't exist
            ValueError: If the YAML is invalid
        """
        if not yaml_path.exists():
            raise FileNotFoundError(f"Avatar YAML file not found: {yaml_path}")
        
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        
        if not data:
            raise ValueError(f"Empty or invalid YAML file: {yaml_path}")
        
        return cls(**data)
