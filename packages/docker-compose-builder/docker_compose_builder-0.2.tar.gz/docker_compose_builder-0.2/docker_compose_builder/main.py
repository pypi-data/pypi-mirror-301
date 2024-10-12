import os
import typer
from ruamel.yaml import YAML
import pkg_resources
 
app = typer.Typer()
 
@app.command()
def build_docker_compose_file(service_name: str):
    # Initialize ruamel.yaml
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)
 
    # Locate the template file within the package
    template_path = pkg_resources.resource_filename('docker_compose_builder', 'docker-template.yml')
 
    # Read the template file
    if not os.path.exists(template_path):
        print(f"Template file {template_path} does not exist.")
        return
 
    with open(template_path, 'r') as file:
        docker_compose = yaml.load(file)
 
    # Update container names and tags
    for env in ['local', 'stg', 'prod']:
        service = docker_compose['services'][env]
        service['container_name'] = f"{env}-{service_name}"
 
        if 'logging' in service:
            service['logging']['options']['tag'] = f"{env}-{service_name}"
 
    # Write the updated docker-compose file
    output_path = os.path.join(os.getcwd(), 'docker-compose.yml')
    with open(output_path, 'w') as file:
        yaml.dump(docker_compose, file)
 
    print(f"Docker Compose file generated: {output_path}")
 
if __name__ == "__main__":
    app()
