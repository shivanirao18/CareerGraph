import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from neo4j import GraphDatabase


load_dotenv()

app = Flask(__name__)

uri = os.getenv("COGNODB_URI")
username = os.getenv("COGNODB_USERNAME")
password = os.getenv("COGNODB_PASSWORD")

driver = GraphDatabase.driver(
    uri,
    auth=(username, password)
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/test-db")
def test_db():
    with driver.session() as session:
        result = session.run("RETURN 1 AS test")
        value = result.single()["test"]

    return f"CognoDB connection successful! Result: {value}"



@app.route("/api/recommendations", methods=["POST"])
def recommendations():

    data = request.get_json()

    skills = data.get("skills", [])

    if not skills:
        return jsonify([])

    query = """
MATCH (role:JobRole)-[:REQUIRES]->(skill:Skill)
WHERE skill.name IN $skills

WITH role,
     collect(DISTINCT skill.name) AS matching_skills,
     count(DISTINCT skill) AS matched_count

MATCH (role)-[:REQUIRES]->(required:Skill)

WITH role,
     matching_skills,
     matched_count,
     collect(DISTINCT required.name) AS required_skills,
     count(DISTINCT required) AS required_count

OPTIONAL MATCH (company:Company)-[:OFFERS]->(role)

WITH role,
     matching_skills,
     matched_count,
     required_skills,
     required_count,
     collect(DISTINCT company.name) AS companies

RETURN role.title AS role,
       matching_skills,
       [skill IN required_skills WHERE NOT skill IN matching_skills] AS missing_skills,
       matched_count,
       required_count,
       round(100.0 * matched_count / required_count) AS match_percentage,
       companies

ORDER BY match_percentage DESC
"""

    with driver.session() as session:
        result = session.run(query, skills=skills)

        recommendations = []

        for record in result:
            recommendations.append({
                "role": record["role"],
                "matching_skills": record["matching_skills"],
                "missing_skills": record["missing_skills"],
                "match_percentage": record["match_percentage"],
                "companies": record["companies"]
            })

    return jsonify(recommendations)
if __name__ == "__main__":
    app.run(debug=True)