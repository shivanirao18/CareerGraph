import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

uri = os.getenv("COGNODB_URI")
username = os.getenv("COGNODB_USERNAME")
password = os.getenv("COGNODB_PASSWORD")

driver = GraphDatabase.driver(
    uri,
    auth=(username, password)
)


def create_skills(tx):
    query = """
    UNWIND $skills AS skill
    MERGE (s:Skill {name: skill.name})
    SET s.category = skill.category
    """

    tx.run(
        query,
        skills=[
            {"name": "Python", "category": "Programming"},
            {"name": "SQL", "category": "Database"},
            {"name": "Excel", "category": "Data"},
            {"name": "Power BI", "category": "Visualization"},
            {"name": "Statistics", "category": "Data"},
        ]
    )


def create_job_roles(tx):
    query = """
    UNWIND $roles AS role
    MERGE (r:JobRole {title: role.title})
    SET r.category = role.category
    """

    tx.run(
        query,
        roles=[
            {"title": "Data Analyst", "category": "Data"},
            {"title": "Data Scientist", "category": "Data"},
            {"title": "Business Analyst", "category": "Business"},
            {"title": "Python Developer", "category": "Software"},
            {"title": "ML Engineer", "category": "Machine Learning"},
        ]
    )
    
def create_role_skill_relationships(tx):
    query = """
    UNWIND $requirements AS requirement

    MATCH (role:JobRole {title: requirement.role})
    MATCH (skill:Skill {name: requirement.skill})

    MERGE (role)-[r:REQUIRES]->(skill)
    SET r.importance = requirement.importance
    """

    tx.run(
        query,
        requirements=[
            {"role": "Data Analyst", "skill": "SQL", "importance": "essential"},
            {"role": "Data Analyst", "skill": "Excel", "importance": "essential"},
            {"role": "Data Analyst", "skill": "Power BI", "importance": "important"},
            {"role": "Data Analyst", "skill": "Statistics", "importance": "important"},

            {"role": "Data Scientist", "skill": "Python", "importance": "essential"},
            {"role": "Data Scientist", "skill": "SQL", "importance": "important"},
            {"role": "Data Scientist", "skill": "Statistics", "importance": "essential"},

            {"role": "Business Analyst", "skill": "Excel", "importance": "essential"},
            {"role": "Business Analyst", "skill": "SQL", "importance": "important"},
            {"role": "Business Analyst", "skill": "Power BI", "importance": "important"},

            {"role": "Python Developer", "skill": "Python", "importance": "essential"},

            {"role": "ML Engineer", "skill": "Python", "importance": "essential"},
            {"role": "ML Engineer", "skill": "Statistics", "importance": "important"},
        ]
    )

def create_students(tx):
    query = """
    UNWIND $students AS student

    MERGE (s:Student {email: student.email})
    SET s.name = student.name
    """

    tx.run(
        query,
        students=[
            {
                "name": "Shivani",
                "email": "shivani@example.com",
            },
            {
                "name": "Rahul",
                "email": "rahul@example.com",
            },
            {
                "name": "Ananya",
                "email": "ananya@example.com",
            },
        ]
    )
    
def create_student_skills(tx):
    query = """
    UNWIND $student_skills AS item

    MATCH (s:Student {email: item.email})
    MATCH (skill:Skill {name: item.skill})

    MERGE (s)-[:HAS_SKILL]->(skill)
    """

    tx.run(
        query,
        student_skills=[
            {"email": "shivani@example.com", "skill": "Python"},
            {"email": "shivani@example.com", "skill": "SQL"},
            {"email": "shivani@example.com", "skill": "Excel"},

            {"email": "rahul@example.com", "skill": "Python"},
            {"email": "rahul@example.com", "skill": "Statistics"},

            {"email": "ananya@example.com", "skill": "SQL"},
            {"email": "ananya@example.com", "skill": "Power BI"},
            {"email": "ananya@example.com", "skill": "Excel"},
        ]
    )

def create_companies(tx):
    query = """
    UNWIND $companies AS company

    MERGE (c:Company {name: company.name})
    SET c.industry = company.industry
    """

    tx.run(
        query,
        companies=[
            {
                "name": "Cognizant",
                "industry": "Technology",
            },
            {
                "name": "Infosys",
                "industry": "Technology",
            },
            {
                "name": "TCS",
                "industry": "Technology",
            },
            {
                "name": "Deloitte",
                "industry": "Consulting",
            },
            {
                "name": "Accenture",
                "industry": "Consulting",
            },
            {
                "name": "Microsoft",
                "industry": "Technology",
            },
            {
                "name": "Amazon",
                "industry": "Technology",
            },
            {
                "name": "IBM",
                "industry": "Technology",
            },
            {
                "name": "EY",
                "industry": "Consulting",
            },
            {
                "name": "Google",
                "industry": "Technology",
            },
        ]
    )
    
def create_company_roles(tx):
    query = """
    UNWIND $offers AS offer

    MATCH (company:Company {name: offer.company})
    MATCH (role:JobRole {title: offer.role})

    MERGE (company)-[:OFFERS]->(role)
    """

    tx.run(
        query,
        offers=[
            {"company": "Cognizant", "role": "Python Developer"},
            {"company": "Infosys", "role": "Python Developer"},
            {"company": "TCS", "role": "Python Developer"},

            {"company": "Deloitte", "role": "Data Analyst"},
            {"company": "Accenture", "role": "Data Analyst"},
            {"company": "TCS", "role": "Data Analyst"},

            {"company": "Microsoft", "role": "Data Scientist"},
            {"company": "Amazon", "role": "Data Scientist"},
            {"company": "IBM", "role": "Data Scientist"},

            {"company": "Deloitte", "role": "Business Analyst"},
            {"company": "Accenture", "role": "Business Analyst"},
            {"company": "EY", "role": "Business Analyst"},

            {"company": "Google", "role": "ML Engineer"},
            {"company": "Microsoft", "role": "ML Engineer"},
            {"company": "Amazon", "role": "ML Engineer"},
        ]
    )

with driver.session() as session:
    session.execute_write(create_skills)
    session.execute_write(create_job_roles)
    session.execute_write(create_role_skill_relationships)
    session.execute_write(create_students)
    session.execute_write(create_student_skills)
    session.execute_write(create_companies)
    session.execute_write(create_company_roles)

print("CareerGraph seed completed successfully!")

driver.close()