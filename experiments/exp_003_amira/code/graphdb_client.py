from SPARQLWrapper import SPARQLWrapper, JSON


class GraphDBClient:
    """Client to connect to your GraphDB instance - Cinema Knowledge Graph"""
    
    def __init__(self, endpoint="http://localhost:7200/repositories/movie-test"):
        """
        Initialize GraphDB connection
        
        Args:
            endpoint: Your GraphDB SPARQL endpoint
                     Format: http://localhost:7200/repositories/YOUR_REPO_NAME
        """
        self.endpoint = endpoint
        self.sparql = SPARQLWrapper(endpoint)
        self.sparql.setReturnFormat(JSON)
        
        # Define namespace
        self.namespace = "http://exemple.org/cinema#"
    
    def query(self, sparql_query):
        """
        Execute SPARQL query and return results
        
        Args:
            sparql_query: SPARQL query string
            
        Returns:
            Dictionary with query results
        """
        try:
            self.sparql.setQuery(sparql_query)
            results = self.sparql.query().convert()
            return results
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
    
    def get_all_films(self):
        """Get all films with their properties"""
        query = f"""
        PREFIX cinema: <{self.namespace}>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        
        SELECT ?film ?titre ?anneeSortie ?note ?duree
        WHERE {{
          ?film rdf:type cinema:Film .
          OPTIONAL {{ ?film cinema:titre ?titre . }}
          OPTIONAL {{ ?film cinema:anneeSortie ?anneeSortie . }}
          OPTIONAL {{ ?film cinema:note ?note . }}
          OPTIONAL {{ ?film cinema:duree ?duree . }}
        }}
        """
        return self.query(query)
    
    def search_by_keyword(self, keyword):
        """
        Search entities by keyword in their names
        
        Args:
            keyword: Search term
        """
        query = f"""
        PREFIX cinema: <{self.namespace}>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        
        SELECT DISTINCT ?entity ?type ?name ?property ?value
        WHERE {{
          ?entity rdf:type ?type .
          ?entity cinema:nom ?name .
          FILTER(REGEX(?name, "{keyword}", "i"))
          OPTIONAL {{ ?entity ?property ?value . }}
        }}
        LIMIT 50
        """
        return self.query(query)
    
    def get_films_by_genre(self, genre_name):
        """Get films of a specific genre"""
        query = f"""
        PREFIX cinema: <{self.namespace}>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        
        SELECT ?film ?titre ?genre ?genreNom
        WHERE {{
          ?film rdf:type cinema:Film .
          ?film cinema:titre ?titre .
          ?film cinema:genre ?genre .
          ?genre cinema:nom ?genreNom .
          FILTER(REGEX(?genreNom, "{genre_name}", "i"))
        }}
        """
        return self.query(query)
    
    def get_film_details(self, film_title):
        """Get all details about a specific film"""
        query = f"""
        PREFIX cinema: <{self.namespace}>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        
        SELECT ?film ?property ?value
        WHERE {{
          ?film rdf:type cinema:Film .
          ?film cinema:titre ?titre .
          FILTER(REGEX(?titre, "{film_title}", "i"))
          ?film ?property ?value .
        }}
        """
        return self.query(query)
    
    def get_actors_in_film(self, film_title):
        """Get actors in a specific film"""
        query = f"""
        PREFIX cinema: <{self.namespace}>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        
        SELECT ?film ?acteur ?nom
        WHERE {{
          ?film rdf:type cinema:Film .
          ?film cinema:titre ?titre .
          FILTER(REGEX(?titre, "{film_title}", "i"))
          ?film cinema:avecActeur ?acteur .
          ?acteur cinema:nom ?nom .
        }}
        """
        return self.query(query)
    
    def get_director_of_film(self, film_title):
        """Get director of a specific film"""
        query = f"""
        PREFIX cinema: <{self.namespace}>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        
        SELECT ?film ?realisateur ?nom
        WHERE {{
          ?film rdf:type cinema:Film .
          ?film cinema:titre ?titre .
          FILTER(REGEX(?titre, "{film_title}", "i"))
          ?film cinema:realisePar ?realisateur .
          ?realisateur cinema:nom ?nom .
        }}
        """
        return self.query(query)


# Test the connection
if __name__ == "__main__":
    client = GraphDBClient()
    
    # Test query
    print("Testing connection...")
    films = client.get_all_films()
    
    if films:
        print("Connected successfully!")
        print(f"Found {len(films['results']['bindings'])} films")
    else:
        print("Connection failed!")