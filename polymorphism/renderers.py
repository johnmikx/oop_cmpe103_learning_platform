"""
Polymorphism Example: Renderer Classes
Demonstrates method overriding and interchangeable objects
"""

from abc import ABC, abstractmethod
from typing import Any, List, Dict
import json

class BaseRenderer(ABC):
    """
    Demonstrates POLYMORPHISM - the fourth pillar of OOP
    
    Abstract base class that defines the interface for different renderers
    Different renderers can be used interchangeably (polymorphism)
    """
    
    @abstractmethod
    def render(self, data: Any) -> str:
        """
        Abstract method that must be implemented by all renderers
        Each renderer implements this differently (polymorphism)
        """
        pass
    
    @abstractmethod
    def get_content_type(self) -> str:
        """Abstract method for content type"""
        pass

class HtmlRenderer(BaseRenderer):
    """
    Concrete implementation of BaseRenderer for HTML output
    Demonstrates POLYMORPHISM by implementing abstract methods with HTML-specific logic
    """
    
    def render(self, data: Any) -> str:
        """
        ⬅️ POLYMORPHISM: HTML-specific implementation of render method
        Same method signature but different behavior than other renderers
        """
        if isinstance(data, list):
            return self._render_list(data)
        elif isinstance(data, dict):
            return self._render_dict(data)
        else:
            return f"<p>{str(data)}</p>"
    
    def get_content_type(self) -> str:
        """⬅️ POLYMORPHISM: HTML-specific content type"""
        return "text/html"
    
    def _render_list(self, data: List) -> str:
        """Private method for rendering lists as HTML"""
        html = "<ul>\n"
        for item in data:
            html += f"  <li>{str(item)}</li>\n"
        html += "</ul>"
        return html
    
    def _render_dict(self, data: Dict) -> str:
        """Private method for rendering dictionaries as HTML"""
        html = "<table border='1'>\n"
        for key, value in data.items():
            html += f"  <tr><td><strong>{key}</strong></td><td>{value}</td></tr>\n"
        html += "</table>"
        return html

class JsonRenderer(BaseRenderer):
    """
    Different concrete implementation of BaseRenderer for JSON output
    Demonstrates POLYMORPHISM - same interface, different implementation
    """
    
    def render(self, data: Any) -> str:
        """
        ⬅️ POLYMORPHISM: JSON-specific implementation of render method
        Same method name and signature as HtmlRenderer but completely different behavior
        """
        try:
            # Handle datetime objects and other non-serializable types
            return json.dumps(data, indent=2, default=str)
        except TypeError:
            # Fallback for non-serializable objects
            return json.dumps(str(data), indent=2)
    
    def get_content_type(self) -> str:
        """⬅️ POLYMORPHISM: JSON-specific content type"""
        return "application/json"

class XmlRenderer(BaseRenderer):
    """
    Third implementation demonstrating POLYMORPHISM
    Shows how multiple classes can implement the same interface differently
    """
    
    def render(self, data: Any) -> str:
        """
        ⬅️ POLYMORPHISM: XML-specific implementation
        Yet another different implementation of the same abstract method
        """
        if isinstance(data, list):
            return self._render_list_xml(data)
        elif isinstance(data, dict):
            return self._render_dict_xml(data)
        else:
            return f"<data>{str(data)}</data>"
    
    def get_content_type(self) -> str:
        """⬅️ POLYMORPHISM: XML-specific content type"""
        return "application/xml"
    
    def _render_list_xml(self, data: List) -> str:
        """Private method for XML list rendering"""
        xml = "<items>\n"
        for i, item in enumerate(data):
            xml += f"  <item id='{i}'>{str(item)}</item>\n"
        xml += "</items>"
        return xml
    
    def _render_dict_xml(self, data: Dict) -> str:
        """Private method for XML dictionary rendering"""
        xml = "<object>\n"
        for key, value in data.items():
            xml += f"  <{key}>{str(value)}</{key}>\n"
        xml += "</object>"
        return xml

class RendererFactory:
    """
    Factory class demonstrating POLYMORPHISM in practice
    Shows how different renderer objects can be used interchangeably
    """
    
    @staticmethod
    def get_renderer(format_type: str) -> BaseRenderer:
        """
        ⬅️ POLYMORPHISM: Factory method that returns different renderer types
        All returned objects implement the same interface (BaseRenderer)
        """
        if format_type.lower() == "html":
            return HtmlRenderer()
        elif format_type.lower() == "json":
            return JsonRenderer()
        elif format_type.lower() == "xml":
            return XmlRenderer()
        else:
            raise ValueError(f"Unsupported format: {format_type}")

def demonstrate_polymorphism():
    """
    Function demonstrating POLYMORPHISM in action
    Shows how different objects can be used interchangeably
    """
    # Sample data to render
    sample_data = {
        "name": "John Doe",
        "role": "Student",
        "courses": ["Math", "Science", "History"]
    }
    
    # ⬅️ POLYMORPHISM: Different renderer types used with same interface
    renderers = [
        HtmlRenderer(),
        JsonRenderer(),
        XmlRenderer()
    ]
    
    print("=== POLYMORPHISM DEMONSTRATION ===\n")
    
    for renderer in renderers:
        # ⬅️ POLYMORPHISM: Same method call works on all renderer types
        print(f"Renderer Type: {type(renderer).__name__}")
        print(f"Content Type: {renderer.get_content_type()}")
        print("Rendered Output:")
        print(renderer.render(sample_data))
        print("-" * 50)

# Example usage demonstrating polymorphism
if __name__ == "__main__":
    demonstrate_polymorphism()
    
    # ⬅️ POLYMORPHISM: Using factory to create different renderers
    print("\n=== FACTORY PATTERN WITH POLYMORPHISM ===\n")
    
    data = ["Apple", "Banana", "Cherry"]
    
    for format_type in ["html", "json", "xml"]:
        renderer = RendererFactory.get_renderer(format_type)
        print(f"{format_type.upper()} Output:")
        print(renderer.render(data))
        print()
