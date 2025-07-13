import os
import typesense

# client connection
client = typesense.Client({
    'api_key': os.getenv('TYPESENSE_API_KEY'),
    'nodes': [{'host': 'localhost', 'port': '8108', 'protocol': 'http'}],
    'connection_timeout_seconds': 2
})

def create_collection():
    """Create a sample collection if it doesn't exist"""
    try:
        existing_collections = client.collections.retrieve()
        collection_names = [col['name'] for col in existing_collections]
        
        if 'companies' in collection_names:
            print("✅ Collection 'companies' already exists!")
            return
        
        schema = {
            'name': 'companies',
            'fields': [
                {'name': 'company_name', 'type': 'string'},
                {'name': 'num_employees', 'type': 'int32'},
                {'name': 'country', 'type': 'string', 'facet': True}
            ],
            'default_sorting_field': 'num_employees'
        }
        
        client.collections.create(schema)
        print("✅ Collection 'companies' created successfully!")
        
    except Exception as e:
        print(f"❌ Failed to create collection: {e}")

def insert_documents():
    """Insert sample documents"""
    try:
        documents = [
            {
                'id': '1',
                'company_name': 'Stark Industries',
                'num_employees': 5215,
                'country': 'USA'
            },
            {
                'id': '2', 
                'company_name': 'Wayne Enterprises',
                'num_employees': 3200,
                'country': 'USA'
            },
            {
                'id': '3',
                'company_name': 'Oscorp',
                'num_employees': 1500,
                'country': 'USA'
            }
        ]
        
        for doc in documents:
            client.collections['companies'].documents.create(doc)
        
        print("✅ Documents inserted successfully!")
        
    except Exception as e:
        print(f"❌ Failed to insert documents: {e}")

def search_documents():
    """Search for documents"""
    try:
        search_parameters = {
            'q': 'stark',
            'query_by': 'company_name',
            'filter_by': 'num_employees:>2000',
            'sort_by': 'num_employees:desc'
        }
        
        results = client.collections['companies'].documents.search(search_parameters)
        
        print(" Search Results:")
        for hit in results['hits']:
            doc = hit['document']
            print(f"  - {doc['company_name']} ({doc['num_employees']} employees, {doc['country']})")
            
    except Exception as e:
        print(f"❌ Search failed: {e}")

def read_all_documents():
    """Read all documents"""
    try:
        # Get all documents (using wildcard search)
        search_parameters = {
            'q': '*',
            'per_page': 50
        }
        
        results = client.collections['companies'].documents.search(search_parameters)
        
        print("📖 All Documents:")
        for hit in results['hits']:
            doc = hit['document']
            print(f"  - {doc['company_name']} ({doc['num_employees']} employees, {doc['country']})")
            
    except Exception as e:
        print(f"❌ Failed to read documents: {e}")

if __name__ == "__main__":
    print(" Starting Typesense operations...")
    
    # Test connection
    try:
        collections = client.collections.retrieve()
        print(f"✅ Connected! Found {len(collections)} collections")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        exit(1)
    
    # Ensure collection exists
    create_collection()
    
    # Insert documents
    # insert_documents()
    
    # Search documents
    search_documents()
    
    # Read all documents
    read_all_documents()
    
    print("🎉 All operations completed!")