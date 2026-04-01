import sqlite3

# connect to your database file 
conn = sqlite3.connect('movie_reviews.db')
c = conn.cursor()

print('=' * 50)
print('INSERTING NEW MOVIES')
print('=' * 50)

movies = [
    ('The Prestige', 'Drama', 'Amazing story and twists', 'positive', 8.6, 2006, 'Usman'),
    ('Mad Max: Fury Road', 'Action', 'High speed action and visuals', 'positive', 8.4, 2015, 'Hassan'),
    ('Parasite', 'Drama', 'Deep social message and brilliant acting', 'positive', 9.0, 2019, 'Ayesha'),
    ('The Dark Knight', 'Action', 'Outstanding performance and plot', 'positive', 9.1, 2008, 'Bilal'),
    ('Whiplash', 'Drama', 'Intense and inspiring music journey', 'positive', 8.8, 2014, 'Zain')
]

c.executemany('''
INSERT INTO movie_reviews 
(title, genre, review_text, sentiment, rating, year, reviewer)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', movies)

conn.commit()

print('5 new movies inserted successfully!')


print()
print('=' * 50)

conn.close()


# QUERY 2 - Count all rows

print('=' * 50)
print('QUERY 1 - Count all rows')
print('=' * 50)

c.execute('SELECT COUNT(*) FROM movie_reviews')
print('Total movies:', c.fetchone()[0])

# QUERY 3 - Drama movies with rating > 8.5

print()
print('=' * 50)
print('QUERY 2 - Drama movies with rating > 8.5')
print('=' * 50)

c.execute("""
SELECT title, genre, rating 
FROM movie_reviews
WHERE genre = 'Drama' AND rating > 8.5
""")

for row in c.fetchall():
    print(row)

# QUERY 4 - Reviewer with most reviews

print()
print('=' * 50)
print('QUERY 3 - Reviewer with most reviews')
print('=' * 50)

c.execute("""
SELECT reviewer, COUNT(*) AS total_reviews
FROM movie_reviews
GROUP BY reviewer
ORDER BY total_reviews DESC
LIMIT 1
""")

print(c.fetchone())

# QUERY 4 - (Optional if table exists)
# Accuracy of model v1.0 vs v2.0

print()
print('=' * 50)
print('QUERY 4 - Model Accuracy (if table exists)')
print('=' * 50)

try:
    c.execute("""
    SELECT 
        model_version,
        COUNT(*) AS total,
        SUM(CASE WHEN actual_label = predicted_label THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS accuracy
    FROM model_predictions
    GROUP BY model_version
    """)
    
    for row in c.fetchall():
        print(row)

except:
    print('Table model_predictions does not exist.')



# QUERY 5 - Add is_correct column (if not exists)
import sqlite3

# connect to your database file 
conn = sqlite3.connect('movie_reviews.db')
c = conn.cursor()

print('=' * 50)
print('ADDING COLUMN is_correct')
print('=' * 50)

try:
    c.execute("ALTER TABLE model_predictions ADD COLUMN is_correct INTEGER")
    print('Column is_correct added successfully!')
except:
    print('Column already exists or table not found.')

conn.commit()
conn.close()