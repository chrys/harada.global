Help me prepare this Django project for production. Here is what you need to know:
- Server is Ubuntu running nginx/gunicorn
- The domain is harada.global 
- The nginx configuration file is `config_files/harada.global` 
- Help me configure a gunicorn configuration file 
- The source code on server will be /srv/harada/. I already pushed the files.
- I want to use journalctl for logging
- I am using locally sqlite3. I want to use in production postgres. The connection string is in file .env as DATABASE_URL