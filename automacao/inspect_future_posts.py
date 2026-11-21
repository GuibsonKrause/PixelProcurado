import subprocess
import json

sql = '''
SELECT id, state, "publishDate", settings, image 
FROM "Post" 
WHERE "integrationId" = 'cmvsctfgl0001jncj932ovibv'
ORDER BY "publishDate" ASC;
'''

out = subprocess.check_output([
    'docker', 'exec', 'postiz-postgres', 'psql', '-U', 'postiz-user', '-d', 'postiz-db-local', '-c', sql
], text=True)

print(out)
