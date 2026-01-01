import xml.etree.ElementTree as ET
from pathlib import Path

NAMESPACE = {"mvn": "http://maven.apache.org/POM/4.0.0"}

def parse_pom_dependencies(pom_path: Path) -> dict:
    tree = ET.parse(pom_path)
    root = tree.getroot()

    deps = []

    for dep in root.findall(".//mvn:dependency", NAMESPACE):
        deps.append({
            "groupId": dep.findtext("mvn:groupId", default="", namespaces=NAMESPACE),
            "artifactId": dep.findtext("mvn:artifactId", default="", namespaces=NAMESPACE),
            "version": dep.findtext("mvn:version", default="", namespaces=NAMESPACE),
            "scope": dep.findtext("mvn:scope", default="compile", namespaces=NAMESPACE)
        })

    return {
        "dependencies": deps,
        "parent": extract_parent(root),
        "java_version": extract_java_version(root)
    }

def extract_parent(root) -> dict | None:
    parent = root.find("mvn:parent", NAMESPACE)
    if parent is None:
        return None

    return {
        "groupId": parent.findtext("mvn:groupId", namespaces=NAMESPACE),
        "artifactId": parent.findtext("mvn:artifactId", namespaces=NAMESPACE),
        "version": parent.findtext("mvn:version", namespaces=NAMESPACE)
    }

def extract_java_version(root) -> str | None:
    props = root.find("mvn:properties", NAMESPACE)
    if props is None:
        return None

    return (
        props.findtext("mvn:maven.compiler.release", namespaces=NAMESPACE)
        or props.findtext("mvn:maven.compiler.target", namespaces=NAMESPACE)
        or props.findtext("mvn:java.version", namespaces=NAMESPACE)
    )
