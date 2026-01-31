class ContextBuilder:
    """Build context from SPARQL results for LLM - Cinema Domain"""
    
    def format_results(self, results, question_type):
        """
        Format SPARQL results into readable context
        
        Args:
            results: SPARQL query results (JSON)
            question_type: Type of question
            
        Returns:
            Formatted string context
        """
        if not results or 'results' not in results:
            return "Aucune information trouvée dans le graphe de connaissances cinéma."
        
        bindings = results['results']['bindings']
        
        if not bindings:
            return "Aucune information trouvée pour cette requête."
        
        # Format based on question type
        formatters = {
            'list_films': self._format_films_list,
            'film_details': self._format_film_details,
            'actors_in_film': self._format_actors_in_film,
            'director_of_film': self._format_director_of_film,
            'films_by_genre': self._format_films_by_genre,
            'films_by_director': self._format_films_by_director,
            'actor_details': self._format_actor_details,
            'genre_details': self._format_genre_details
        }
        
        formatter = formatters.get(question_type, self._format_general)
        return formatter(bindings)
    
    def _format_films_list(self, bindings):
        context = "Liste des films:\n\n"
        for item in bindings:
            titre = item.get('titre', {}).get('value', 'Titre inconnu')
            annee = item.get('anneeSortie', {}).get('value', 'N/A')
            note = item.get('note', {}).get('value', 'N/A')
            context += f"- Film: {titre}\n"
            context += f"  Année: {annee}\n"
            context += f"  Note: {note}/10\n\n"
        return context
    
    def _format_film_details(self, bindings):
        context = "Détails du film:\n\n"
        for item in bindings:
            prop = item.get('property', {}).get('value', '')
            value = item.get('value', {}).get('value', '')
            # Extract property name from URI
            prop_name = prop.split('#')[-1] if '#' in prop else prop
            context += f"- {prop_name}: {value}\n"
        return context
    
    def _format_actors_in_film(self, bindings):
        context = "Acteurs dans le film:\n\n"
        for item in bindings:
            nom = item.get('nom', {}).get('value', 'Nom inconnu')
            context += f"- Acteur: {nom}\n"
        return context
    
    def _format_director_of_film(self, bindings):
        context = "Réalisateur du film:\n\n"
        for item in bindings:
            nom = item.get('nom', {}).get('value', 'Nom inconnu')
            context += f"- Réalisateur: {nom}\n"
        return context
    
    def _format_films_by_genre(self, bindings):
        context = "Films du genre:\n\n"
        for item in bindings:
            titre = item.get('titre', {}).get('value', 'Titre inconnu')
            genre_nom = item.get('genreNom', {}).get('value', 'Genre inconnu')
            context += f"- Film: {titre}\n"
            context += f"  Genre: {genre_nom}\n\n"
        return context
    
    def _format_films_by_director(self, bindings):
        context = "Films réalisés par ce réalisateur:\n\n"
        for item in bindings:
            titre = item.get('titre', {}).get('value', 'Titre inconnu')
            context += f"- Film: {titre}\n"
        return context
    
    def _format_actor_details(self, bindings):
        context = "Détails de l'acteur:\n\n"
        for item in bindings:
            prop = item.get('property', {}).get('value', '')
            value = item.get('value', {}).get('value', '')
            # Extract property name from URI
            prop_name = prop.split('#')[-1] if '#' in prop else prop
            context += f"- {prop_name}: {value}\n"
        return context
    
    def _format_genre_details(self, bindings):
        context = "Détails du genre:\n\n"
        for item in bindings:
            nom = item.get('nom', {}).get('value', 'Nom inconnu')
            description = item.get('description', {}).get('value', 'Description inconnue')
            context += f"- Genre: {nom}\n"
            context += f"  Description: {description}\n"
        return context
    
    def _format_general(self, bindings):
        context = "Informations du graphe de connaissances cinéma:\n\n"
        for item in bindings:
            for key, value in item.items():
                if 'value' in value:
                    context += f"{key}: {value['value']}\n"
            context += "\n"
        return context