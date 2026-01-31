# context_builder.py
"""
Context Builder - Formats SPARQL results for LLM consumption
"""

from typing import List, Dict, Any


class ContextBuilder:
    """Formats SPARQL results into readable context for LLM"""
    
    def format_results(self, bindings: List[Dict[str, Any]], explanation: str = "") -> str:
        """
        Format SPARQL results as readable context
        
        Args:
            bindings: List of result bindings from SPARQL query
            explanation: Optional explanation of the query
            
        Returns:
            Formatted context string
        """
        if not bindings:
            return "Aucune donnée trouvée dans le graphe de connaissances."
        
        context = ""
        
        if explanation:
            context += f"Contexte de la requête: {explanation}\n\n"
        
        context += f"Données trouvées ({len(bindings)} résultats):\n\n"
        
        for i, binding in enumerate(bindings, 1):
            context += f"Résultat {i}:\n"
            for key, value in binding.items():
                if 'value' in value:
                    display_value = value['value']
                    # Shorten URIs to just the ID
                    if display_value.startswith('http://'):
                        display_value = display_value.split('#')[-1].split('/')[-1]
                    context += f"  - {key}: {display_value}\n"
            context += "\n"
        
        return context
    
    def format_for_display(self, bindings: List[Dict[str, Any]]) -> str:
        """Format results for terminal display"""
        if not bindings:
            return "Aucun résultat"
        
        output = f"\n{'='*80}\n"
        output += f" {len(bindings)} résultat(s) trouvé(s)\n"
        output += f"{'='*80}\n\n"
        
        for i, binding in enumerate(bindings, 1):
            output += f"Résultat {i}:\n"
            for key, value in binding.items():
                if 'value' in value:
                    output += f"  {key}: {value['value']}\n"
            output += "\n"
        
        return output


if __name__ == "__main__":
    # Test
    test_bindings = [
        {
            "horse": {"value": "http://example.org/Horse123"},
            "name": {"value": "Thunder"},
            "race": {"value": "Arabian"}
        }
    ]
    
    builder = ContextBuilder()
    context = builder.format_results(test_bindings, "Test query")
    print(context)
