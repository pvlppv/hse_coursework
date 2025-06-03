FROM postgres:13

# Install cron
RUN apt-get update && apt-get install -y cron

# Copy the backup script into the container
COPY postgres_backup.sh /usr/local/bin/postgres_backup.sh
RUN chmod +x /usr/local/bin/postgres_backup.sh

# Add the cron job for automatic backup
RUN echo "0 3 * * * postgres /usr/local/bin/postgres_backup.sh >> /var/log/cron.log 2>&1" > /etc/cron.d/postgres_backup

# Apply cron job permissions and crontab
RUN chmod 0644 /etc/cron.d/postgres_backup && crontab /etc/cron.d/postgres_backup

# Start cron in the foreground and run Postgres
CMD ["sh", "-c", "cron -f & exec docker-entrypoint.sh postgres"]
