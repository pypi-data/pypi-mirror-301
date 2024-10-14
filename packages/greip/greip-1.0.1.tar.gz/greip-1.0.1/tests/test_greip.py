import greip

# Initialize the Greip instance with your API token
greip_instance = greip.Greip("YOUR_API_TOKEN")

# Example: Lookup IP information
response = greip_instance.lookup("1.1.1.1")
print(response)  # Access properties like response.ip, response.country, etc.