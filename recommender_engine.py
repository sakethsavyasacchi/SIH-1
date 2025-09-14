import pandas as pd

def load_and_preprocess_data():
    """
    Loads and preprocesses the internship data.
    """
    try:
        internships_df = pd.read_csv('data/internships.csv')
        
        # Normalize and split skills for internships
        internships_df['Required_Skills'] = internships_df['Required_Skills'].str.lower().str.split(',\s*')
        internships_df['Location'] = internships_df['Location'].str.lower()
        internships_df['Sector'] = internships_df['Sector'].str.lower()
        
        return internships_df

    except FileNotFoundError:
        print("Error: The 'data' folder or 'internships.csv' was not found.")
        return None

def get_recommendations(candidate_skills, candidate_location, candidate_sector, internships_df):
    """
    Recommends internships and returns matched skills for each recommendation.
    """
    # Normalize candidate inputs
    candidate_skills_list = [skill.strip().lower() for skill in candidate_skills.split(',')]
    
    df = internships_df.copy()
    df['score'] = 0

    # Apply location and sector filters if they are not 'None'
    if candidate_location:
        df = df[df['Location'] == candidate_location.lower()]

    if candidate_sector:
        df = df[df['Sector'] == candidate_sector.lower()]

    # If no internships match the location/sector filters, return an empty DataFrame
    if df.empty:
        return pd.DataFrame()

    # Location Match (gives a strong bonus)
    # The bonus is now applied to all remaining internships since they've already been filtered
    if candidate_location:
        df['score'] += 10
    
    # Sector Match (gives a smaller bonus)
    if candidate_sector:
        df['score'] += 5

    # Calculate skill match count and also store the matched skills themselves
    def find_matched_skills(required_skills):
        if not isinstance(required_skills, list): # handle potential non-list values
            return []
        matched = list(set(required_skills).intersection(set(candidate_skills_list)))
        return matched

    df['matched_skills'] = df['Required_Skills'].apply(find_matched_skills)
    df['skill_match_count'] = df['matched_skills'].apply(len)
    
    df['score'] += df['skill_match_count'] * 3

    # A score of 0 can now be a valid result if there are no skills
    # We only want to sort by score and then by skill match count as a tiebreaker
    df['final_score'] = df['score'] + (df['skill_match_count'] * 0.1) # Add a small value to break ties
    
    top_recommendations = df.sort_values(by='final_score', ascending=False).head(5)
    
    return top_recommendations