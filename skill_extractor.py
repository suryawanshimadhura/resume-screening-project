def extract_skills(text, skills_list):

    skills_found = []

    for skill in skills_list:
        if skill in text:
            skills_found.append(skill)

    return skills_found